import os
from datetime import UTC, datetime, timedelta
from typing import List

from core.client import client
from fastapi import HTTPException
from httpx import HTTPError
from models.city import Cities, City, CityInfo, MomentWeather, SummaryInfo, TimeSeries


class WeatherService:
    query_URL_city_all = "https://api.openweathermap.org/data/2.5/weather"
    query_URL_forecast = "https://api.openweathermap.org/data/2.5/forecast"
    query_URL_coordinates = "http://api.openweathermap.org/geo/1.0/direct"
    default_cities = [
        "Taipei",
        "Koprivnica",
        "Prague",
        "Boston",
        "Sydney",
    ]
    
    def __init__(self):
        with open(os.environ["APIKEY"], "r") as f:
            self.APIKey = f.read().split("\n")[0].strip()
        self.cities = Cities()

        for city in self.default_cities:
            self.add_city(city)

    def add_city(self, name: str) -> Cities:
        """
        After clicking the button 'Add city' add inputed city to the list of tracked cities if it already isn't.

        Args:
            name (str): The name of the city to add.

        Returns:
            self.cities (Cities): Updated list of tracked cities.
        """
        try:
            new_city = self.get_city_coordinates(city=name)
            if new_city not in self.cities:
                self.cities.add_city(new_city)
            return self.cities
        except Exception as e:
            raise e


    def remove_city(self, name: str, country_code: str) -> Cities:
        """
        After clicking the 'X' button remove the city from the list of tracked cities.

        Args:
            name (str): The name of the city to remove.
            country_code (str): The code of a country the specified city is in.

        Returns:
            self.cities (Cities): Updated list of tracked cities.
        """
        name = name.title()
        self.cities.remove_city(name, country_code)
        return self.cities

    def get_city_info(self, city: str, country_code: str | None = None) -> CityInfo:
        """
        Retrieve all information about the specified city.

        Args:
            city (str): The name of the city.
            country_code (str): The code of a country the specified city is in.

        Returns:
            info (CityInfo): The information about the city.
        """
        if "," in city:
            city, country_code = city.split(",")[:2]

        if country_code is not None:
            q = city + "," + country_code
        else:
            q = city
        params = {
            "q": q,
            "appid": self.APIKey,
            "units": "metric",
        }
        try:
            city = city.title()
            res = client.get(self.query_URL_city_all, params=params)
            res.raise_for_status()
            cityInfo = res.json()
            lon = round(cityInfo["coord"]["lon"], 2)
            if lon >= 0:
                lon = str(lon) + "°E"
            else:
                lon = str(-lon) + "°W"
            lat = round(cityInfo["coord"]["lat"], 2)
            if lat >= 0:
                lat = str(lat) + "°N"
            else:
                lat = str(-lat) + "°S"
            tz_shift = timedelta(seconds=cityInfo["timezone"])
            dt = cityInfo["dt"]
            dt_obj = datetime.fromtimestamp(dt, UTC) + tz_shift
            dt_readable = dt_obj.strftime("%H:%M %d.%m.%Y")
            dt_sunset = cityInfo["sys"]["sunset"]
            dt_sunrise = cityInfo["sys"]["sunrise"]
            dt_sunset_obj = datetime.fromtimestamp(dt_sunset, UTC) + tz_shift
            dt_sunset_str = dt_sunset_obj.strftime("%H:%M")
            dt_sunrise_obj = datetime.fromtimestamp(dt_sunrise, UTC) + tz_shift
            dt_sunrise_str = dt_sunrise_obj.strftime("%H:%M")
            if dt > dt_sunrise and dt < dt_sunset:
                is_day = True
            else:
                is_day = False
            icon_id = cityInfo["weather"][0]["icon"]
            icon = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
            info = CityInfo(
                name=city,
                lon=lon,
                lat=lat,
                dt=cityInfo["dt"],
                temperature=round(cityInfo["main"]["temp"], 1),
                feels_like=round(cityInfo["main"]["feels_like"], 1),
                humidity=cityInfo["main"]["humidity"],
                wind_speed=round(cityInfo["wind"]["speed"], 1),
                main=cityInfo["weather"][0]["main"],
                description=cityInfo["weather"][0]["description"],
                current_time=dt_readable,
                sunrise_dt=dt_sunset,
                sunset_dt=dt_sunrise,
                sunrise_readable=dt_sunrise_str,
                sunset_readable=dt_sunset_str,
                is_day=is_day,
                icon=icon,
                country_code=cityInfo["sys"]["country"],
            )

        except HTTPError as e:
            error_message = f"Error fetching data for {city}: {str(e)}"
            raise HTTPException(status_code=res.status_code, detail=error_message)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unexpected error ocurred: {str(e)}"
            )
        return info

    def get_city_coordinates(self, city: str) -> City:
        """
        Retrieve city coordinates and country code for the specified city.

        Args:
            city (str): The name of the city.

        Returns:
            city_found (City): City object that contains name, coordinates and country code for the specified city.
        """
        params = {"q": city, "limit": 5, "appid": self.APIKey}
        try:
            res = client.get(self.query_URL_coordinates, params=params)
            city_candidates = res.json()
            if "," in city:
                city, country_code_given = city.split(",")[:2]
            else:
                country_code_given = None
            city_found = False
            for city_iter in city_candidates:
                country_code = city_iter["country"]
                if country_code_given is not None:
                    if country_code_given.lower() != country_code.lower():
                        continue
                city_name = city_iter["name"]
                if city.lower() != city_name.lower():
                    local_names = [i.lower() for i in city_iter["local_names"].values()]
                    if city.lower() not in local_names:
                        continue
                city_name_found = city_name
                city_lat_found = city_iter["lat"]
                city_lon_found = city_iter["lon"]
                country_code_found = country_code
                city_found = True
                break

            if city_found:
                city_found = City(
                    name=city_name_found,
                    country_code=country_code_found,
                    lat=city_lat_found,
                    lon=city_lon_found,
                )
                return city_found
            else:
                raise HTTPException(status_code=400, detail="Could not find city.")
        except HTTPError as e:
            error_message = f"Error fetching data for {city}: {str(e)}"
            raise HTTPException(status_code=res.status_code, detail=error_message)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unexpected error ocurred: {str(e)}"
            )

    def get_summary(self) -> List[CityInfo]:
        """
        Retrieve all data about all tracked cities.

        Returns:
            data.data (List[CityInfo]): A list of data for all tracked cities.
        """
        data = SummaryInfo()
        for city in self.cities:
            try:
                city_info = self.get_city_info(city.name, city.country_code)
                data.data.append(city_info)
            except Exception as e:
                pass
        return data.data

    def timeseries_data(self, city: str) -> List[MomentWeather]:
        """
        Retrieve timeseries data for the specified city.

        Args:
            city (str): The name of the city.

        Returns:
            time_series.data (List[MomentWeather]): A list of time series weather data for the specified city.
        """
        params = {
            "q": city,
            "appid": self.APIKey,
            "units": "metric",
            "cnt": 24,
        }  # cnt -> 3 hour interval
        time_series = TimeSeries()

        try:
            res = client.get(self.query_URL_forecast, params=params)
            res.raise_for_status()
            cityInfoTime = res.json()
            tz_shift = timedelta(seconds=cityInfoTime["city"]["timezone"])
            for timeStamp in cityInfoTime["list"]:
                dt_obj = datetime.fromtimestamp(timeStamp["dt"]) + tz_shift
                dt_readable = dt_obj.strftime("%d.%m.%Y %H:%M:%S")
                dt_for_chart = dt_obj.strftime("%d.%m.%Y %H:%M")
                time_stamp = MomentWeather(
                    date=dt_readable.split(" ")[0],
                    time=dt_for_chart.split(" ")[1],
                    temperature=timeStamp["main"]["temp"],
                )
                time_series.data.append(time_stamp)
        except HTTPError as e:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Error fetching data for {city}: {str(e)}",
            )
        return time_series.data

    def get_all_cities(self) -> Cities:
        """
        Retrieve a list of all tracked cities.

        Returns:
            self.cities (Cities): A list of all tracked cities.
        """
        return self.cities


weatherService = WeatherService()
