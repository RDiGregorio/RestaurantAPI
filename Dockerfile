FROM python:3.9

# Set the working directory
WORKDIR /RestaurantAPI

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Load the restaurant data
RUN python manage.py migrate
RUN python manage.py load_restaurants

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]