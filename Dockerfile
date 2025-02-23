# Use official Python image as a base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . /app

# Ensure Flask can find templates
ENV FLASK_APP=backend.app
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 9000

# Run the Flask application
CMD ["python", "backend/app.py"]

