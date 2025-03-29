# Use a temporary builder image to install dependencies
FROM python:3.10-slim AS builder

WORKDIR /app
COPY Real-Estate-/requirements.txt .  
RUN pip install --no-cache-dir --user -r requirements.txt  

# Create a smaller final image
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local  
COPY Real-Estate-/ .  

ENV PATH="/root/.local/bin:$PATH"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
