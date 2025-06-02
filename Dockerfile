# Use any Node.js base image that you want (as long as it's Alpine)!
FROM python:3.11-slim AS build

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the working directory before copying the rest 
COPY requirements.txt /app

# Install the dependencies
RUN pip install --target=/app/dependencies -r requirements.txt

# Copy the rest of the files into the working directory
COPY . /app
# Run Distroless Image for Python
FROM gcr.io/distroless/python3

# Use non root user
USER 65532:65532

# Set workdir
WORKDIR /app

# Copying the application files from the previous step
COPY --from=build --chown=65532:65532 /app /app
COPY --from=build --chown=65532:65532 /app/dependencies /app/dependencies

# Setting an environment variable so Python knows where to find the dependencies
ENV PYTHONPATH=/app/dependencies

# Enviroment Variables for database connection
ENV DATABASE_HOST=
ENV DATABASE_NAME=
ENV DATABASE_USER=
ENV DATABASE_PASSWORD=
ENV DATABASE_PORT=

# חשיפת הפורט הדרוש
EXPOSE 8000

# Setting the entry point to run the application
ENTRYPOINT ["python3", "-m", "uvicorn", "web_app:app", "--host=0.0.0.0", "--port=8000"]

