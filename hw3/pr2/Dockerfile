FROM python:3.10-slim

WORKDIR /app

# Copy only requirements.txt first and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app