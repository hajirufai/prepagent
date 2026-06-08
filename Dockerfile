FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use Vertex AI (not free API key) for production
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV GOOGLE_CLOUD_LOCATION=us-central1

EXPOSE 8080

CMD ["python", "-m", "prepagent.web.app"]
