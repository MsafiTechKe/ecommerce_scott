# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (enables Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose the port Render will use
EXPOSE 10000

# Start the app using gunicorn (Render-friendly)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
