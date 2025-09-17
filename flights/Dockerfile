# Use the official Python 3.8 image as the base image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /python-docker

# Copy the requirements file into the container
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

# Install the required dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

ENV OPENTELEMETRY_DISTRO_VERSION=0.54b0
RUN pip install --no-cache-dir "opentelemetry-distro[otlp]==$OPENTELEMETRY_DISTRO_VERSION"
RUN opentelemetry-bootstrap -a install


# Copy the rest of your application code into the container
COPY . .

# Expose port 5001
EXPOSE 5001

# Specify the command to run your Flask app
CMD ["opentelemetry-instrument", "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]
