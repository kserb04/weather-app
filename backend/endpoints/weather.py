from fastapi import APIRouter
from typing import List
from service import weatherService
from models.city import City, Cities, CityInfo, SummaryInfo, TimeSeries, MomentWeather
from pydantic import BaseModel

router = APIRouter(
    prefix='/api/weather',
    tags=['api-weather']
)

@router.get("/summary")
async def summ() -> List[CityInfo]:
    """
    Retrieve summary data for a list of cities.

    Returns:
        summary_info (List[CityInfo]): A list of weather information for all tracked cities.
    """
    summary_info = weatherService.get_summary()
    return summary_info

@router.get("/city/{city}")
def read_city(city: str) -> CityInfo:
    """
    Get weather data for a specified city.

    Args:
        city (str): The name of the city.

    Returns:
        city_info (CityInfo): Weather information for the specified city.
    """
    city_info = weatherService.get_city_info(city)
    return city_info

@router.post("/city/{city}")
async def update_cities(city: str) -> Cities:
    """
    Add a city to the list of tracked cities.

    Args:
        city (str): The name of the city to add.

    Returns:
        cities (Cities): Updated list of tracked cities.
    """
    cities = weatherService.add_city(city)
    return cities

@router.get("/timeseries/{city}")
async def time_city(city: str) -> List[MomentWeather]:
    """
    Retrieve time series weather data for a specific city.

    Args:
        city (str): The name of the city.

    Returns:
        time_data (List[MomentWeather]): Time series weather data for the specified city.
    """
    time_data = weatherService.timeseries_data(city)
    return time_data

@router.get("/coordinates/{city}")
async def get_coordinates(city: str) -> City:
    """
    Retrieve city coordinates and country code for specified city.

    Args:
        city (str): The name of the specified city.

    Returns:
        city_full (City): City object for specified city.
    """
    city_full = weatherService.get_city_coordinates(city)
    return city_full

@router.post("/delete/{city}")
async def remove_city(city: str) -> Cities:
    """
    Delete a city from a list of tracked cities.

    Args:
        city (str): The name of the city to delete.

    Returns:
        cities (Cities): Updated list of tracked cities.
    """
    city_name, country_code = city.split(',')

    cities = weatherService.remove_city(city_name, country_code)
    return cities
