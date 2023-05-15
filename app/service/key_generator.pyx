from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from cpython.bytes cimport PyBytes_FromStringAndSize
from libc.stdlib cimport rand


cdef char[63] alphanum

def generate_key(str url):
    cdef unsigned int crc_hash = 0
    cdef int i, j, length
    cdef char* base_hash

    # Initialize the alphanum array using memcpy
    memcpy(&alphanum[0], "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", sizeof(alphanum))

    length = len(url)
    base_hash = <char*>malloc(9)

    for i in range(length):
        crc_hash = (crc_hash << 8) | (ord(url[i]) & 0xFF)

        if (crc_hash & 0xFF000000):
            crc_hash = crc_hash ^ (crc_hash >> 24)
            crc_hash = crc_hash ^ (crc_hash >> 16)
            crc_hash = crc_hash ^ (crc_hash >> 8)

    crc_hash &= 0xFFFFFFFF

    for i in range(8):
        crc_hash, j = divmod(crc_hash, 62)
        base_hash[i] = alphanum[j]

    base_hash[8] = b'\0'

    result_bytes = PyBytes_FromStringAndSize(base_hash, 8)
    result = result_bytes.decode()

    free(base_hash)

    return result

def generate_random_key():
    cdef int i
    cdef char random_hash[9]
    cdef str result

    for i in range(8):
        random_hash[i] = alphanum[rand() % 62]

    random_hash[8] = b'\0'

    result = random_hash.decode()

    return result
