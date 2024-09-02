
from flask import Flask, request, jsonify
import os
from pdfminer.high_level import extract_text

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração do diretório de upload
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para processar o texto do PDF sem NLTK e spaCy
def simple_process_text(text):
    # Aqui, vamos apenas dividir o texto em palavras e contar as ocorrências de termos-chave
    words = text.split()
    return {"word_count": len(words)}

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

        # Processamento do texto simplificado
        processed_text = simple_process_text(text)

        return jsonify({
            'message': 'File processed successfully',
            'word_count': processed_text['word_count'],
            'text_excerpt': text[:500]
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
