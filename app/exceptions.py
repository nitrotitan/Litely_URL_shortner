from fastapi import HTTPException


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_url_not_found(request):
    message = f"URL '{request.url}' doesn't exist or disabled"
    raise HTTPException(status_code=404, detail=message, headers=request.headers)


def raise_key_not_found(key):
    message = f"Info for key '{key}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def not_authorized(message):
    raise HTTPException(status_code=401, detail=message)
