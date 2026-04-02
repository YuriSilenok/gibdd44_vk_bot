from functools import wraps
import asyncio
from fastapi import HTTPException, status


def handle_http_errors(func):
    """Декоратор для обработки HTTP ошибок"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return (
                await func(*args, **kwargs)
                if asyncio.iscoroutinefunction(func)
                else func(*args, **kwargs)
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e))
    return wrapper
