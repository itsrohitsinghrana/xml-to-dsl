# Use official Python image as a base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY backend /app/backend
COPY frontend/templates /app/frontend/templates
COPY frontend/static /app/frontend/static

# Create necessary upload directories inside the container
RUN mkdir -p /app/uploads/uploads_XML /app/uploads/convert_DSL

# Ensure Flask can find templates and modules
ENV FLASK_APP=backend.app
ENV PYTHONPATH=/app

# Expose the Flask app port
EXPOSE 9000

# Run the Flask application
CMD ["python", "/app/backend/app.py"]

