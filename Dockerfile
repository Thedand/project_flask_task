FROM python:3.8.6-buster

# Make a directory for you application
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy our source code
COPY ./ .

# Run the application
CMD ["python", "main.py"]
