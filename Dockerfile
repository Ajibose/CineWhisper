# Use an official Python runtime as a parent image.
FROM python:3.12-slim

# Prevent Python from writing pyc files and enable unbuffered output.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory.
WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copy requirements file and install Python dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project.
COPY . /app/

# Collect static files (if you have them).
RUN python manage.py collectstatic --noinput

# Expose port 8000.
EXPOSE 8000

# Command to run Gunicorn.
CMD ["gunicorn", "cinewhisper.wsgi:application", "--bind", "0.0.0.0:8000"]

