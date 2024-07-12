from fastapi import APIRouter
import requests as re
from service import weatherService as wS

router = APIRouter(
    prefix='/api/info',
    tags=['api-info']
)

@router.get("/get-all-cities")
async def getAllCities():
    return wS.get_all_cities()
