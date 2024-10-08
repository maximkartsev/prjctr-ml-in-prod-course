# Use Python official image as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8000
EXPOSE 8000

# Start Uvicorn server
CMD ["uvicorn", "app.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
