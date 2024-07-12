import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import LineChartComponent from "./charts/LineChart";

const fetchTimeSeries = async (city) => {
    try {
        const response = await fetch(`http://localhost:8000/api/weather/timeseries/${encodeURIComponent(city)}`, {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (!response.ok) {
            return { status: response.status };
        }
        const data = await response.json();
        return data;
    } catch (error) {
            console.error("Error fetching data: ", error);
            return null;
    }
};

const Details = ({ currCity, response, setIsHome }) => {
    const [data, setData] = useState([]); // timeseries data for specific city
    const cityData = response.find(city => city["name"] === currCity.split(',')[0] && city["country_code"] === currCity.split(',')[1]); // full data for specific city
    let isDay = cityData["is_day"];
    let day = isDay ? "Day" : "Night"

    useEffect(() => {
        fetchTimeSeries(currCity).then((data) => setData(data));
    }, [currCity]);

    if (!data || !cityData) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container-details">
            <div className="container-details-header">
                <Button className="btn-custom-back" onClick={() => setIsHome(true)}>Back to home page</Button>
                <h2>Detailed weather statistics for {currCity.split(',').join(', ')}</h2>
            </div>
            <div className="container-details-body">
                <div className="container-details-text">
                    <p className="description">
                        {day}, {cityData["description"]}
                        <img src={cityData["icon"]} />
                    </p>
                    <hr />
                    <p>Temperature: {cityData["temperature"]}°C </p>
                    <p>Feels like: {cityData["feels_like"]}°C </p>
                    <p>Humidity: {cityData["humidity"]}% </p>
                    <p>Wind speed: {cityData["wind_speed"]}m/s </p>
                    <hr />
                    <p>Current local time: {cityData["current_time"]} </p>
                    <p>Sunrise time: {cityData["sunrise_readable"]} </p>
                    <p>Sunset time: {cityData["sunset_readable"]} </p>
                    <hr />
                    <p>Coordinates: {cityData["lat"]} {cityData["lon"]}</p>
                    <p>Country code: {cityData["country_code"]}</p>
                </div>
                <div className="container-details-chart">
                    <h4> Predicted temperature for the next 3 days </h4>
                    <LineChartComponent data={data} />
                </div>
            </div>

        </div>
    );
};

export default Details;
