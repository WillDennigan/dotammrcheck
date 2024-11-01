# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the app files to the container
COPY . .

# Install required Python packages
RUN pip install -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 80

# Run the Flask app
CMD ["python", "app.py"]
