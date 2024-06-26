# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# This sets the PYTHONPATH to include the libcatsume directory
ENV PYTHONPATH /app/libcatsume

# Define the command to run the app
CMD ["python", "-m", "libcatsume", "--cats", "--server"]