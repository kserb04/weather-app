# My Weather App
My Weather App is a web application that allows users to track weather data for various cities.

Users can add or remove cities they want to see the weather data for.

The app provides a bar chart and a pie chart for a comparison of weather conditions and temperature in all tracked cities.

There is also a line chart for each city that provides a preview of the predicted temperatures for the next 3 days.
The app uses [OpenWeatherMap API](https://openweathermap.org/).

## Tech Stack
Frontend:
-[React](https://react.dev/)
-[Recharts](https://recharts.org/) for plotting
-[React Bootstrap](https://react-bootstrap.netlify.app/) for frontend components

Backend:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/) for data validation
- [hishel](https://hishel.com/) for caching

Deployment:
- [Docker Compose](https://docs.docker.com/compose/) for easy deployment

## Preview
### Home page
![Home page](/images/home_page.png "Home page")
### Interactive components
![Dropdown menu](/images/dropdown_menu.png "Dropdown menu")
### Detailed weather statistics for specific city
![Weather details page](/images/details.png "Weather details")

## How to use it
### Adding new city
Enter the name of the city in the input field and click the "Add city" button. The city will be added to the list of tracked cities and displayed on the main page.

### Removing city
Click the "X" button next to the city's name to remove it from the list of tracked cities.

### Detailed city weather information
Choose the city name from the dropdown menu or click on a city card to view its detailed weather information.

## Deployment
Run `make up` to build and start the app.
Run `make down` to stop the app.
By default, frontend runs on port 3000 and backend on port 8000.