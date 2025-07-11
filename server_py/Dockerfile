# 1. Base Image (Python)
FROM python:3.12-slim

# 2. Install git, Node.js, npm, and gemini-cli
RUN apt-get update && \
    apt-get install -y git curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @google/gemini-cli

# 3. Setup app directory
WORKDIR /app
COPY . .

# 4. Install server dependencies
RUN pip install -r requirements.txt

# 5. Expose port and set API Key placeholder
EXPOSE 8000

# 6. Default command to run the server in http mode
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 