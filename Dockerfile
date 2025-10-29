# Start with a Python base image
FROM python:3.8-slim

# Set the working directory, all subsequent commands are relative to this
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r "requirements.txt"

# --- SIMPLIFIED COPY ---
# Copy the contents of the local 'app' folder (main.py, train.py, etc.)
# directly into the container's /app directory.
COPY ./app .

# Copy the data into a 'data' subdirectory within /app
COPY ./data ./data

# --- BUILD-TIME TRAINING STEP ---
# The path is now simple and correct: train.py is in the current directory (/app)
RUN echo "--- Starting model training inside the container ---" && \
    python train.py

# --- DIAGNOSTIC STEP ---
# Verify that the training was successful and the files exist.
RUN echo "--- Verifying contents of the created model_store ---" && \
    ls -R .

# Expose the port for the web service
EXPOSE 8080

# The command to run the application. 'main' refers to main.py.
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8080", "main:app"]