FROM python:3.12-slim

WORKDIR /workspace

# Prevent python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
