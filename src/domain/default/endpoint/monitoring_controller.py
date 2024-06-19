from fastapi import APIRouter, Response
from prometheus_client import generate_latest

router = APIRouter(prefix="/monitoring")


@router.get("/metrics")
async def get_metrics():
    return Response(generate_latest(), media_type="text/plain")
