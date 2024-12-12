FROM python:3.11
WORKDIR /ticketing
COPY . .
RUN pip install -r requirements.txt

# Update the port to 8000 to match the exposed port
CMD ["gunicorn", "ticketing.wsgi:application", "--bind", "0.0.0.0:8000"]


# # Base image
# FROM python:3.9-slim

# # Set environment variables
# ENV PYTHONUNBUFFERED 1

# # Set working directory
# WORKDIR /app

# # Install Git
# RUN apt-get update && apt-get install -y git && apt-get clean

# # Copy requirements and install dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy the rest of the application code
# COPY . /app/

# # Expose the port
# EXPOSE 8000

# # Default command to run the server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
