# # Use the official Python image from the Docker Hub
# FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set the working directory
# WORKDIR /app

# # Copy the requirements file and Install the dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . /app/

# # Expose the port the app runs on
# EXPOSE 8081

# # Run the FastAPI app with Uvicorn
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081"]
