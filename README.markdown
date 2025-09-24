# LemoZeen

## Overview

LemoZeen is a web-based application inspired by Uber, enabling users to select a car and driver from an available pool, specify a pickup point and destination, and book trips seamlessly. The application integrates with the Google Maps API for real-time mapping, route calculation, and location services. It features distinct interfaces for users, drivers, and admins to manage bookings, vehicles, and personnel.

## Features

- **User Authentication**: Secure login for users, drivers, and admins.
- **Trip Booking**: Users can browse available cars and drivers, select pickup and destination points using Google Maps integration, and confirm bookings.
- **Driver Management**: Drivers can view and accept assigned trips.
- **Admin Controls**: Admins can add, view, and manage cars, drivers, and all trips.
- **Real-time Mapping**: Powered by Google Maps API for accurate location handling and route visualization.
- **Database Management**: Stores user data, trip details, car/driver information using SQL.

## Technologies Used

- **Backend**: Django (Python web framework for handling server-side logic, authentication, and API endpoints).
- **Frontend**: HTML and CSS for structure and styling, JavaScript for dynamic interactions and integrating Google Maps API.
- **Database**: SQL for persistent storage of users, trips, cars, and drivers.
- **APIs**: Google Maps API for geolocation, mapping, and routing.

## Screenshots

### Login Page
![Login Page](path/to/login-page.png)

### User Page
![User Page](path/to/user-page.png)

### Driver Page
![Driver Page](path/to/driver-page.png)

### Admin Page
![Admin Page](path/to/admin-page.png)

### Add Car Page
![Add Car Page](path/to/add-car-page.png)

### Add Driver Page
![Add Driver Page](path/to/add-driver-page.png)

### All Cars Page
![All Cars Page](path/to/all-cars-page.png)

### All Drivers Page
![All Drivers Page](path/to/all-drivers-page.png)

### Book Trip Page
![Book Trip Page](path/to/book-trip-page.png)

### Confirmed Trip Page
![Confirmed Trip Page](path/to/confirmed-trip-page.png)

### All Trips Page
![All Trips Page](path/to/all-trips-page.png)

## Live Demo

[Live Demo](https://your-deployment-link.com)

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/lemozeen.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Run the server: `python manage.py runserver`

Note: Ensure you have a Google Maps API key configured in the settings.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.