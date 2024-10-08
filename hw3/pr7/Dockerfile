# Use Python official image as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy only requirements.txt first and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose port 8000
EXPOSE 8000

# Start Uvicorn server
CMD ["uvicorn", "app.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
