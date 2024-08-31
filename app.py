from flask import Flask, request, jsonify
import os
from pdfminer.high_level import extract_text
import nltk
import spacy
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.llms import Ollama
import requests

# Função para baixar o PDF
def download_pdf(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded successfully: {save_path}")
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

# Exemplo de uso
pdf_url = 'https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:d70c8dbc-c869-40d4-983c-2702dc945560.pdf'
save_path = 'uploads/Politica_de_privacidade.pdf'
download_pdf(pdf_url, save_path)

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configurações do NLTK e spaCy
nltk.download('punkt')
spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

# Configuração do diretório de upload
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuração do ChromaDB
vectorstore = Chroma(persist_directory=os.getenv('PERSIST_DIRECTORY', 'chroma_store'))
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="path_to_model")
langchain = LLMChain(llm=llm)

# Função para processar o texto do PDF
def process_text(text):
    tokens = nltk.word_tokenize(text)
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return {"tokens": tokens, "entities": entities}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extração do texto do PDF
        try:
            text = extract_text(filepath)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        # Processamento do texto
        processed_text = process_text(text)

        # Treinamento do modelo com LangChain (simplificado)
        trained_model = langchain.run(inputs={"text": text})

        # Armazenamento dos vetores no ChromaDB
        vectorstore.add_texts([text], embeddings.embed_text([text]))

        return jsonify({
            'message': 'File processed successfully',
            'tokens': processed_text['tokens'][:10],  
            'entities': processed_text['entities']
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
