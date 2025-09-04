# Use Python 3.12 slim image (small base)
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install OS-level dependencies only if needed
# (comment this out first, only add back if pip fails on some libs)
# RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose the port Azure App Service will use (usually 8000)
EXPOSE 8000

# Run your app
CMD ["python", "app.py"]
