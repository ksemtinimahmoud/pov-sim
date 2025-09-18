# Step 1: Use an official Gradle image to build the application
FROM gradle:8.3.0-jdk17 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project to the container
COPY . .

# Build the application
RUN gradle clean bootJar

# Step 2: Use a lightweight JDK image for running the app
FROM openjdk:17-jdk-slim

# Set the working directory for the runtime container
WORKDIR /app

# OTel Java agent
ADD https://github.com/grafana/grafana-opentelemetry-java/releases/download/v2.19.0/grafana-opentelemetry-java.jar /otel/grafana-opentelemetry-java.jar

# Pyroscope Java Agent
ADD https://github.com/grafana/pyroscope-java/releases/download/v2.1.2/pyroscope.jar /otel/pyroscope.jar

# Copy the JAR file from the build stage
COPY --from=build /app/build/libs/*.jar app.jar

# Expose the port the application runs on
EXPOSE 8080

# Set the command to run the application
ENTRYPOINT ["java","-javaagent:/otel/grafana-opentelemetry-java.jar", "-javaagent:/otel/pyroscope.jar", "-jar", "app.jar"]
