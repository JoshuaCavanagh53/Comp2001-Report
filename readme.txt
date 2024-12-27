# Trail Management API

## Project Overview
This project is a RESTful API for managing hiking trails, built using Flask and SQL Server. It allows users to create, update, view, and delete trail information securely, with user authentication handled via an API.

## Features
- Authentication: Validates users based on an external authenticator API.
- CRUD operations: Each endpoint  uses a CRUD operation to manipulate the trails. Viewing trails uses GET, Creating trails uses POST, Updating trails uses PUT and Deleting trails uses DELETE.
- Swagger implementation: Provides an interactive API documentation that makes it easy for testing API endpoints.
- Database designs: Azure Studio has been used to create tables for the trails. These tables store the trails attributes. Trails data is linked across multiple tables.

## Technology stack
- Backend: Flask with Connexion
- Database: Azure Studio (SQL)
- API Documentation: Swagger (OpenAPI)
- Libraries: pyodbc for database connectivity, Flask-RESTful for API development.