# Dockerfile
FROM python:3.13.3

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Copy project files
COPY . .

# Default command can be overridden by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
