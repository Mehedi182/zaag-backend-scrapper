# Start with an official Python image.
FROM python:3.11-slim

# Set the working directory in the container to /backend
WORKDIR /backend

# Copy the requirements.txt file to the container from the parent directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI project code to the working directory in the container
COPY ./backend/ .
# Copy the .env file from one directory above
COPY ../.env .
# Expose the port the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
