from pydantic import BaseModel

class City(BaseModel):
    name: str
    country_code: str
    lon: float
    lat: float

class Cities(BaseModel):
    cities: list[City] = []
    
    def add_city(self, city: City):
        self.cities.append(city)
    
    def __contains__(self, city: City):
        return any(c.name == city.name and c.country_code == city.country_code for c in self.cities)

    def remove_city(self, city_name: str, country_code: str):
        print(city_name, country_code, "1")
        self.cities = [city for city in self.cities if not (city.name == city_name and city.country_code == country_code)]

    def __iter__(self):
        for city in self.cities:
            yield city

class CityInfo(BaseModel):
    name: str
    lon: str
    lat: str
    dt: int
    temperature: float
    feels_like: float
    humidity: float
    wind_speed: float
    main: str
    description: str
    current_time: str
    sunrise_dt: int
    sunset_dt: int
    sunrise_readable: str
    sunset_readable: str
    is_day: bool
    icon: str
    country_code: str

class SummaryInfo(BaseModel):
    data: list[CityInfo] = []

class MomentWeather(BaseModel):
    date: str
    time: str
    temperature: float

class TimeSeries(BaseModel):
    data: list[MomentWeather] = []