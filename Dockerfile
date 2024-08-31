FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install chromadb sentence-transformers langchain-chroma langchain-huggingface

# Copy the rest of the application
COPY . .

# Run the application
CMD ["python", "app.py"]
