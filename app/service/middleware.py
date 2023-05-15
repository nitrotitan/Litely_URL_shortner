import asyncio
from datetime import datetime, timedelta
from typing import List, Tuple, Any
from queue import PriorityQueue
from fastapi import Request
from starlette.responses import JSONResponse

RATE_LIMIT = 10
DURATION = timedelta(minutes=1)
BATCH_DURATION = timedelta(seconds=10)
NUM_SHARDS = 5

request_counts = [PriorityQueue() for _ in range(NUM_SHARDS)]
last_request_time = [{} for _ in range(NUM_SHARDS)]


class TokenBucket:
    def __init__(self, capacity: int, rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill_time = datetime.now()
        self.token_rate = rate

    def consume(self, tokens: int) -> bool:
        self.refill_tokens()
        if tokens <= self.tokens:
            self.tokens -= tokens
            return True
        return False

    def refill_tokens(self):
        now = datetime.now()
        time_since_last_refill = now - self.last_refill_time
        tokens_to_add = int(time_since_last_refill.total_seconds() * self.token_rate)
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now


token_buckets = [TokenBucket(RATE_LIMIT, RATE_LIMIT / DURATION.total_seconds()) for _ in range(NUM_SHARDS)]


async def rate_limiter(request: Request, call_next):
    ip_address = request.client.host

    shard_index = hash(ip_address) % NUM_SHARDS

    # Validate shard_index and adjust if it exceeds the range
    if shard_index >= NUM_SHARDS:
        shard_index %= NUM_SHARDS

    token_bucket = token_buckets[shard_index]
    request_count_queue = request_counts[shard_index]
    last_request_dict = last_request_time[shard_index]

    # Consume tokens from the token bucket
    if not token_bucket.consume(1):
        return JSONResponse(
            status_code=429,
            content={"Err": "Possible DDoS detected"},
            headers={"Retry-After": str(DURATION.seconds) + " seconds"},
        )

    # Update request count and last request time
    request_count_queue.put(ip_address)
    last_request_dict[ip_address] = datetime.now()

    response = await call_next(request)
    return response


def process_batch_requests(batch: List[Tuple[str, int]]):
    for ip_address, count in batch:
        shard_index = hash(ip_address) % NUM_SHARDS
        token_bucket = token_buckets[shard_index]
        request_count_queue = request_counts[shard_index]
        last_request_dict = last_request_time[shard_index]

        # Remove tokens from the token bucket
        if not token_bucket.consume(count):
            return JSONResponse(status_code=429, content={"Err": "Possible DDoS detected"})

        # Update request count and last request time
        request_count_queue.put(ip_address)
        last_request_dict[ip_address] = datetime.now()


def get_accumulated_batch() -> List[Tuple[str, int]]:
    batch = []

    for shard_index in range(NUM_SHARDS):
        request_count_queue = request_counts[shard_index]
        last_request_dict = last_request_time[shard_index]

        current_time = datetime.now()

        while not request_count_queue.empty():
            ip_address = request_count_queue.get()
            last_time = last_request_dict[ip_address]
            elapsed_time = current_time - last_time

            if elapsed_time <= DURATION:
                count = elapsed_time.total_seconds()
                batch.append((ip_address, count))
            else:
                # Skip the IP address if it has exceeded the DURATION
                del last_request_dict[ip_address]

    return batch


async def batch_processing_task():
    while True:
        batch = get_accumulated_batch()
        print("Batch processing Running")
        if batch:
            process_batch_requests(batch)
        await asyncio.sleep(BATCH_DURATION.total_seconds())
