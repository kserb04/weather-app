import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import Header from "./Header";
import Home from "./Home"
import Details  from './Details';

const fetchFromApi = async () => {
    try {
        const response = await fetch("http://localhost:8000/api/weather/summary", {
            method: "get",
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
        console.error("Error fetching data:", error);
        return null;
    }   
};

function App() {
    const [isHome, setIsHome] = useState(true);
    const [currCity, setCurrCity] = useState('');
    const [response, setResponse] = useState(null);

    useEffect(() => {
        fetchFromApi().then((data) => setResponse(data));
    }, []);

    if (response === null ) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            {isHome ? (
                <div>
                    <Header />
                    <Home setIsHome={setIsHome} setCurrCity={setCurrCity} response={response} setResponse={setResponse} />
                </div>
            ) : (
                <Details currCity={currCity} response={response} setIsHome={setIsHome} />
            )}
        </div>
    );
}

export default App;

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);