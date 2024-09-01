
# RAG Challenge

This project is a Python-based application that processes PDF files, extracts and analyzes text using NLP tools, and integrates with ChromaDB for vector storage and retrieval. The application is built with Flask and utilizes various libraries including `spacy`, `nltk`, `pdfminer.six`, and `langchain`.

## Features

- **PDF Processing**: Download and extract text from PDF files.
- **NLP Analysis**: Tokenization and entity recognition using `nltk` and `spacy`.
- **Vector Storage**: Store and retrieve text vectors using ChromaDB.
- **RESTful API**: A simple API for uploading PDFs and returning processed text and entities.

## Project Structure

- **Dockerfile**: Configuration for building the Docker image of the application.
- **docker-compose.yml**: Configuration for running the application and ChromaDB service using Docker Compose.
- **app.py**: The main application file containing the Flask server and core logic.
- **requirements.txt**: Lists the dependencies required for the project.

## Requirements

- Docker and Docker Compose installed on your system.
- Python 3.9 or higher if running locally.

## Setup Instructions

### Running with Docker Compose

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/rag_challenge.git
   cd rag_challenge
