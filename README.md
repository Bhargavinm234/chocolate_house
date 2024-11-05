The Chocolate House inventory management system is a web-based application for managing chocolate-related ingredients, customer suggestions, and allergy issues related to flavors of the season. Allows users to add and control ingredients used in chocolates for submission of suggestions to improve upon the chocolates offered. Check any allergens in seasonal flavor to ensure safety for a customer. 
Features Ingredient inventory: It keeps track of all the ingredients with its name and quantity. Customer Suggestion: Collect feedback from customers so that the product can be improved.
Allergy Issues: Input allergens such as peanuts or milk, and it will notify you if the seasonal flavors have that allergy.

Clone the Repository: Download or clone the project files to your local machine.
https://github.com/Bhargavinm234/chocolate_house.git

Install Dependencies: Run pip install -r requirements.txt to install the necessary packages.
pip install flask

Requirements
Python 3.7+: Ensure Python is installed.
Flask: For web framework handling.
Flask-SQLAlchemy: For ORM and database management.
SQLite: As a lightweight database for storing data locally.

Tech Stack
Frontend: HTML, CSS for styling and layout.
Backend: Flask for application logic and routing.
Database: SQLAlchemy ORM with SQLite database.

[if not intsalled] REQUIREMENTS / LIBRARIES TO BE INSTALLED
Flask==2.1.1
Flask-SQLAlchemy==2.5.1
SQLAlchemy==1.4.29
Werkzeug==2.1.1
Use pip install command and install all the necessary packages.

Then, Run the application.
Use python main.py

Open your web browser and go to http://127.0.0.1:5000 to start using the system.

DOCKER INSTRUCTIONS
# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "main.py"]

Build the Docker image
Open a terminal, navigate to your project directory, and run the following command to build the Docker image:
docker build -t chocolate-house-app .

Run the Docker container
After building the image, run the following command to start the container:
docker run -p 5000:5000 chocolate-house-app

This command maps port 5000 on your local machine to port 5000 in the container, allowing you to access the app at http://localhost:5000.

