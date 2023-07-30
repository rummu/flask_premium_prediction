# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

RUN chmod +x entrypoint.sh
# Expose port 5000 for the Flask app
EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
