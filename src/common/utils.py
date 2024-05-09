from .exception import InternalServerError


async def verify_int(*, obj) -> int:
    if obj is None:
        raise InternalServerError
    try:
        verified_obj = int(obj)
    except Exception:
        raise InternalServerError
    return verified_obj
