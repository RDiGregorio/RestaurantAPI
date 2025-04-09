FROM python:3.9

# Set the working directory
WORKDIR /RestaurantAPI

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Run the unit tests
CMD ["python", "manage.py", "test"]