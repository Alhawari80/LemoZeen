# LemoZeen

## Overview

LemoZeen is a web-based application inspired by Uber, enabling users to select a car and driver from an available pool, specify a pickup point and destination, and book trips seamlessly. The application integrates with the Google Maps API for real-time mapping, route calculation, and location services. It features distinct interfaces for users, drivers, and admins to manage bookings, vehicles, and personnel.

## Features





User Authentication: Secure login for users, drivers, and admins.



Trip Booking: Users can browse available cars and drivers, select pickup and destination points using Google Maps integration, and confirm bookings.



Driver Management: Drivers can view and accept assigned trips.



Admin Controls: Admins can add, view, and manage cars, drivers, and all trips.



Real-time Mapping: Powered by Google Maps API for accurate location handling and route visualization.



Database Management: Stores user data, trip details, car/driver information using SQL.

Technologies Used





Backend: Django (Python web framework for handling server-side logic, authentication, and API endpoints).



Frontend: HTML and CSS for structure and styling, JavaScript for dynamic interactions and integrating Google Maps API.



Database: SQL for persistent storage of users, trips, cars, and drivers.



APIs: Google Maps API for geolocation, mapping, and routing.

Screenshots

Login Page



User Page



Driver Page



Admin Page



Add Car Page



Add Driver Page



All Cars Page



All Drivers Page



Book Trip Page



Confirmed Trip Page



All Trips Page



Live Demo

Live Demo

Installation





Clone the repository: git clone https://github.com/yourusername/lemozeen.git



Install dependencies: pip install -r requirements.txt



Set up the database: python manage.py migrate



Run the server: python manage.py runserver

Note: Ensure you have a Google Maps API key configured in the settings.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

