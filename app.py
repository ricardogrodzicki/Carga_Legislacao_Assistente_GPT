from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegulationThemeAnalyzer:
    def __init__(self):
        # Portuguese stopwords
        self.portuguese_stopwords = set(stopwords.words('portuguese'))
        # Add specific electrical sector stopwords
        self.portuguese_stopwords.update([
            'artigo', 'parágrafo', 'inciso', 'alínea', 'lei', 'decreto', 'resolução',
            'normativo', 'instrução', 'portaria', 'seção', 'capítulo', 'título',
            'poder', 'público', 'nacional', 'federal', 'brasileiro', 'energia'
        ])
        
    def preprocess_text(self, text):
        """Preprocess text for analysis"""
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-záàâãéêíóôõúçñ\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text, language='portuguese')
        
        # Remove stopwords and short words
        filtered_tokens = [
            token for token in tokens 
            if token not in self.portuguese_stopwords and len(token) > 2
        ]
        
        return ' '.join(filtered_tokens)
    
    def extract_themes(self, documents, n_clusters=8):
        """Extract themes from documents using clustering"""
        if not documents:
            return []
        
        # Preprocess documents
        processed_docs = [self.preprocess_text(doc) for doc in documents]
        processed_docs = [doc for doc in processed_docs if doc.strip()]
        
        if len(processed_docs) < 2:
            return [{"theme": "Regulamentação Geral", "keywords": ["energia", "elétrica"], "documents": documents}]
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.8
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(processed_docs)
            
            # Clustering
            n_clusters = min(n_clusters, len(processed_docs))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)
            
            # Extract themes
            feature_names = vectorizer.get_feature_names_out()
            themes = []
            
            for cluster_id in range(n_clusters):
                # Get documents in this cluster
                cluster_docs = [documents[i] for i, label in enumerate(cluster_labels) if label == cluster_id]
                
                # Get top keywords for this cluster
                cluster_center = kmeans.cluster_centers_[cluster_id]
                top_indices = cluster_center.argsort()[-10:][::-1]
                keywords = [feature_names[i] for i in top_indices]
                
                # Generate theme name based on keywords
                theme_name = self.generate_theme_name(keywords)
                
                themes.append({
                    "theme": theme_name,
                    "keywords": keywords,
                    "documents": cluster_docs,
                    "size": len(cluster_docs)
                })
            
            return sorted(themes, key=lambda x: x['size'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error in theme extraction: {e}")
            return [{"theme": "Regulamentação Geral", "keywords": ["energia", "elétrica"], "documents": documents}]
    
    def generate_theme_name(self, keywords):
        """Generate a meaningful theme name from keywords"""
        # Mapping of common electrical sector terms
        theme_mapping = {
            'tarifa': 'Tarifas e Preços',
            'distribuição': 'Distribuição de Energia',
            'transmissão': 'Transmissão de Energia',
            'geração': 'Geração de Energia',
            'consumidor': 'Direitos do Consumidor',
            'qualidade': 'Qualidade do Serviço',
            'segurança': 'Segurança Elétrica',
            'ambiental': 'Aspectos Ambientais',
            'renovável': 'Energia Renovável',
            'solar': 'Energia Solar',
            'eólica': 'Energia Eólica',
            'hidrelétrica': 'Energia Hidrelétrica',
            'nuclear': 'Energia Nuclear',
            'térmica': 'Energia Térmica',
            'regulatório': 'Marco Regulatório',
            'concessão': 'Concessões e Autorizações',
            'fiscalização': 'Fiscalização',
            'penalidade': 'Penalidades e Multas'
        }
        
        for keyword in keywords[:3]:
            for term, theme in theme_mapping.items():
                if term in keyword.lower():
                    return theme
        
        # Default theme name based on first keyword
        if keywords:
            return f"Regulamentação - {keywords[0].title()}"
        
        return "Regulamentação Geral"

# Global analyzer instance
analyzer = RegulationThemeAnalyzer()

# Sample data for demonstration
SAMPLE_REGULATIONS = [
    "Resolução sobre tarifas de energia elétrica e reajuste de preços para consumidores residenciais",
    "Normativo sobre qualidade do fornecimento de energia elétrica e indicadores de continuidade",
    "Regulamentação sobre geração distribuída fotovoltaica e compensação de energia elétrica",
    "Instrução sobre segurança em instalações elétricas e proteção de trabalhadores",
    "Decreto sobre concessões de transmissão de energia elétrica e leilões públicos",
    "Portaria sobre fiscalização de distribuidoras de energia elétrica e penalidades",
    "Resolução sobre direitos e deveres dos consumidores de energia elétrica",
    "Normativo sobre energia renovável e incentivos para geração limpa",
    "Regulamentação sobre medição inteligente e modernização do sistema elétrico",
    "Instrução sobre aspectos ambientais da geração de energia elétrica"
]

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/themes')
def get_themes():
    """Get theme analysis"""
    try:
        # For demo, use sample data. In production, this would load from vector DB or files
        themes = analyzer.extract_themes(SAMPLE_REGULATIONS)
        return jsonify({
            'success': True,
            'themes': themes,
            'total_documents': len(SAMPLE_REGULATIONS)
        })
    except Exception as e:
        logger.error(f"Error getting themes: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/theme/<theme_name>')
def get_theme_details(theme_name):
    """Get detailed information about a specific theme"""
    try:
        themes = analyzer.extract_themes(SAMPLE_REGULATIONS)
        theme = next((t for t in themes if t['theme'] == theme_name), None)
        
        if not theme:
            return jsonify({'success': False, 'error': 'Theme not found'}), 404
        
        # For each document in the theme, extract sub-themes
        sub_themes = analyzer.extract_themes(theme['documents'], n_clusters=min(4, len(theme['documents'])))
        
        return jsonify({
            'success': True,
            'theme': theme,
            'sub_themes': sub_themes
        })
    except Exception as e:
        logger.error(f"Error getting theme details: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_documents():
    """Upload and analyze custom documents"""
    try:
        data = request.json
        documents = data.get('documents', [])
        
        if not documents:
            return jsonify({'success': False, 'error': 'No documents provided'}), 400
        
        themes = analyzer.extract_themes(documents)
        return jsonify({
            'success': True,
            'themes': themes,
            'total_documents': len(documents)
        })
    except Exception as e:
        logger.error(f"Error uploading documents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)