
# Use Python as the base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Create a directory for database storage
RUN mkdir -p /data

# Set database location
ENV DB_PATH=/data/students.db

# Expose Flask application port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]

