
#!/bin/bash

# Exit if any command fails
set -e

echo "Starting Student Application Deployment"

# Move to project directory
cd ~/student-management-system

# Download latest code
git pull origin main

echo "Building new Docker image..."

# Build updated image
docker build -f docker/Dockerfile \
  -t student-management:1.0 .

echo "Removing old container if it exists..."

# Remove previous container
docker rm -f student-app 2>/dev/null || true

echo "Starting new container..."

# Run updated container
docker run -d \
  --name student-app \
  -p 80:5000 \
  -v student-data:/data \
  --restart unless-stopped \
  student-management:1.0

echo "Deployment completed successfully!"

# Display running container
docker ps

