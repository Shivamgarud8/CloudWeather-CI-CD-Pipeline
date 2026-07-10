# ---- Base image ----
FROM python:3.12-slim

# Prevents Python from writing .pyc files & buffers stdout (good for logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install only what's needed to build wheels, then clean up
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .
COPY templates/ templates/
COPY images/ images/

# Flask default port
EXPOSE 5000

# Use gunicorn in prod instead of flask's dev server
RUN pip install --no-cache-dir gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
