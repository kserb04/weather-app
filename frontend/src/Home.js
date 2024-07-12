import React, { useEffect, useState } from "react";
import { Button, Dropdown } from "react-bootstrap";
import PieChartComponent from "./charts/PieChart";
import BarChartComponent from "./charts/BarChart";

const fetchFromApi = async () => {
    try {
        const response = await fetch("http://localhost:8000/api/weather/summary", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            return response.json();
        } else {
            return {status: response.status};
        }
    } catch (error) {
        console.error("Error fetching data: ", error);
        return null;
    }
};

const getCityData = async (cityName) => {
    try {
        const response = await fetch(`http://localhost:8000/api/weather/coordinates/${encodeURIComponent(cityName)}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (response.ok) {
            return response.json();
        } else {
            return {status: response.status};
        }
    } catch (error) {
        console.error("Error fetching data: ", error);
        return null;
    }
};

const addCity = async (cityName) => {
    try {
        const response = await fetch(`http://localhost:8000/api/weather/city/${encodeURIComponent(cityName)}`, {
            method: "POST"
        });
        if (response.ok) {
            const data = await response.json();
            return data;
        } 
    } catch (error) {
        console.error("Error adding city: ", error);
        throw new Error(`Error adding city:'${cityName}'`);
    }
};


const removeCity = async (city, country_code) => {
    try {
        const response = await fetch(`http://localhost:8000/api/weather/delete/${encodeURIComponent(city+','+country_code)}`, {
            method: "POST"
        });
        if (response.ok) {
            const citiesDeleted = await response.json()
            return citiesDeleted;
        } else {
            console.error(`Failed to remove city ${city}: `, response.statusText);
        }
    } catch (error) {
        console.error("Error removing city: ", error);
    }
}

const Home = ({ setIsHome, setCurrCity, response, setResponse }) => {
    const [newCity, setNewCity] = useState('');
    let citiesPreDef = []
    response.forEach((city) => {
        citiesPreDef.push(city.name + ',' + city.country_code);
    });
    let [cities, setCities] = useState(citiesPreDef);

    useEffect(() => {
        const fetchData = async() => {
            const data = await fetchFromApi();
            if (data) {
                setResponse(data);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        if (response) {
            const cityNames = response.map(city => city.name);
            setCities(cityNames);
        }
    }, [response]);

    const addCityToList = async (event) => {
        event.preventDefault();
        const newTitle = newCity.split(',')[0].toLowerCase().split(' ').map(word => word.charAt(0).toUpperCase() + word.substring(1)).join(' ');
        try {
            const geoData = await getCityData(newTitle);
            const newCity = geoData.name + ',' + geoData.country_code;
        } catch (error) {
            setNewCity('');
            alert(`Failed to add city '${newCity}', wrong input!`);
        }
        if (!cities.includes(newCity)) {
            try {
                const newCities = await addCity(newCity);
                if (cities.length === newCities.cities.length) {
                    alert("City already exists!");
                }
                setCities(newCities);
                setNewCity('');
                response = await fetchFromApi();
                setResponse(response);
            } catch (error) {
                setNewCity('');
                alert(`Failed to add city '${newCity}', wrong input!`);
                console.error("Error adding city: ", error);
            }
        } else {
            setNewCity('');
            alert("City already exists!");
        }
    }

    const removeCityFromList = async (event, city, country_code) => {
        event.stopPropagation();
        try {
            const citiesDeleted = await removeCity(city, country_code);
            setCities(citiesDeleted);
            cities = citiesDeleted;
            response = await fetchFromApi();
            setResponse(response);
        } catch (error) {
            console.error("Error removing city: ", error);
        }
        return;
    }

    const goToCity = (city, country_code) => {
        setCurrCity(city + ',' + country_code);
        setIsHome(false);
    };

    return (
        <div className="container-main">
            <div className="container-btns">
                <form onSubmit={addCityToList}>
                    <input
                        id="inputCity"
                        placeholder="City name"
                        type="text"
                        onChange={(e) => setNewCity(e.target.value)}
                        value={newCity}
                        required
                    />
                    <Button type="submit" className="btn-custom">Add city</Button>
                </form>
                <Dropdown>
                    <Dropdown.Toggle id="dropdown-basic" className="dd-custom">
                        Choose a city from dropdown menu
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                        {response.map((city) => (
                            <Dropdown.Item key={city.name+city.country_code} onClick={() => goToCity(city.name, city["country_code"])}>{city.name},{city.country_code}</Dropdown.Item>
                        ))}
                    </Dropdown.Menu>
                </Dropdown>
            </div>
            <div className="container-cities">
                <div className="row">
                    {response.map((city) => (
                        <div className={city["is_day"] ? "day" : "night"} key={city["name"]+city["country_code"]}
                            onClick={() => goToCity(city["name"], city["country_code"])}
                            >
                            <Button type="submit" className="btn-delete" onClick={(event) => removeCityFromList(event, city["name"], city["country_code"])}>X</Button>
                            <h2>
                                <img src={city["icon"]} alt="weather icon" />
                                {city["name"]}, {city["country_code"]}
                            </h2>
                            <p>{city["main"]}</p>
                            <p>Temperature: {city["temperature"]}°C</p>
                            <p>Feels like: {city["feels_like"]}°C </p>
                            <p>Humidity: {city["humidity"]}% </p>
                            <p>Wind speed: {city["wind_speed"]}m/s </p>
                            <p>Local time: {city["current_time"].split(" ")[0]}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className="container-chart">
                <BarChartComponent data={response} />
                <PieChartComponent data={response} />
            </div>
        </div>
    );

};

export default Home;
