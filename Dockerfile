# Use official Python image as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask app
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "app.py"]