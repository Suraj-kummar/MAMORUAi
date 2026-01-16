FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Slither
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Solidity compiler
RUN curl -fsSL https://github.com/ethereum/solidity/releases/download/v0.8.24/solc-static-linux -o /usr/local/bin/solc && \
    chmod +x /usr/local/bin/solc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Slither dependencies
RUN pip install --no-cache-dir slither-analyzer

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
