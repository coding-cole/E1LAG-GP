# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Flask default is 5000)
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]