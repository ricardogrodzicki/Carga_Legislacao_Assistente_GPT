#!/usr/bin/env python3
"""
Simple HTTP server for the Theme Navigator application using only built-in Python libraries.
This provides a basic theme analysis and visualization tool for Brazilian electrical regulations.
Now integrated with OpenAI Vector Store for dynamic document retrieval.
"""

import http.server
import socketserver
import json
import re
import os
import urllib.parse
from collections import Counter
import random
import math

# OpenAI integration imports (optional - falls back to sample data if not available)
try:
    from dotenv import load_dotenv
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai or python-dotenv not installed. Using sample data only.")
    print("Install with: pip install openai python-dotenv")

# Load environment variables
if OPENAI_AVAILABLE:
    load_dotenv()

def fetch_documents_from_vector_store(query="energia elétrica", max_results=20):
    """
    Fetch documents from OpenAI Vector Store based on a search query.
    
    Args:
        query: Search query for finding relevant documents
        max_results: Maximum number of documents to retrieve
        
    Returns:
        List of document texts, or None if API is not configured
    """
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = os.getenv('OPENAI_API_KEY')
    vector_store_id = os.getenv('VECTOR_STORE_ID')
    
    if not api_key or not vector_store_id:
        print("Warning: OPENAI_API_KEY or VECTOR_STORE_ID not set in .env file")
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Get files from the vector store
        files_response = client.beta.vector_stores.files.list(
            vector_store_id=vector_store_id,
            limit=max_results
        )
        
        documents = []
        for file_obj in files_response.data:
            try:
                # Retrieve file content
                file_id = file_obj.id
                file_content = client.files.content(file_id)
                content_text = file_content.text
                
                # Extract meaningful text (limit to first few lines or summary)
                lines = content_text.split('\n')
                # Get first non-empty lines
                relevant_lines = []
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 20:  # Skip very short lines
                        relevant_lines.append(line)
                        if len(relevant_lines) >= 3:  # Get up to 3 lines per document
                            break
                
                if relevant_lines:
                    documents.append(' '.join(relevant_lines))
                    
            except Exception as e:
                print(f"Error retrieving file {file_obj.id}: {e}")
                continue
        
        if documents:
            print(f"Successfully fetched {len(documents)} documents from Vector Store")
            return documents
        else:
            print("No documents found in Vector Store")
            return None
            
    except Exception as e:
        print(f"Error accessing Vector Store: {e}")
        return None


class RegulationThemeAnalyzer:
    def __init__(self):
        # Portuguese stopwords (basic set)
        self.stopwords = {
            'a', 'o', 'e', 'de', 'do', 'da', 'em', 'para', 'com', 'por', 'ao', 'aos',
            'das', 'dos', 'na', 'no', 'nas', 'nos', 'se', 'que', 'ou', 'mas', 'como',
            'artigo', 'parágrafo', 'inciso', 'alínea', 'lei', 'decreto', 'resolução',
            'normativo', 'instrução', 'portaria', 'seção', 'capítulo', 'título',
            'poder', 'público', 'nacional', 'federal', 'brasileiro', 'energia', 'é', 'são'
        }
        
        # Theme keywords mapping for Brazilian electrical sector
        self.theme_keywords = {
            'tarifa': ['Tarifas e Preços', ['tarifa', 'preço', 'reajuste', 'valor', 'custo']],
            'distribuição': ['Distribuição de Energia', ['distribuição', 'distribuidora', 'rede', 'fornecimento']],
            'transmissão': ['Transmissão de Energia', ['transmissão', 'transmissora', 'linha', 'subestação']],
            'geração': ['Geração de Energia', ['geração', 'geradora', 'usina', 'produção']],
            'consumidor': ['Direitos do Consumidor', ['consumidor', 'cliente', 'usuário', 'direito']],
            'qualidade': ['Qualidade do Serviço', ['qualidade', 'continuidade', 'interrupção', 'indicador']],
            'segurança': ['Segurança Elétrica', ['segurança', 'proteção', 'acidente', 'risco']],
            'ambiental': ['Aspectos Ambientais', ['ambiental', 'meio', 'ambiente', 'impacto']],
            'renovável': ['Energia Renovável', ['renovável', 'limpa', 'sustentável', 'verde']],
            'solar': ['Energia Solar', ['solar', 'fotovoltaica', 'sol']],
            'eólica': ['Energia Eólica', ['eólica', 'vento', 'aerogerador']],
            'fiscalização': ['Fiscalização', ['fiscalização', 'multa', 'penalidade', 'infração']]
        }
    
    def preprocess_text(self, text):
        """Basic text preprocessing"""
        if not text:
            return ""
        
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-záàâãéêíóôõúçñ\s]', '', text.lower())
        
        # Split into words and filter
        words = [word for word in text.split() 
                if word not in self.stopwords and len(word) > 2]
        
        return words
    
    def extract_themes_simple(self, documents, n_clusters=8):
        """Simple theme extraction using keyword matching"""
        if not documents:
            return []
        
        # Count keywords across all documents
        theme_counts = {theme: 0 for theme in self.theme_keywords}
        theme_docs = {theme: [] for theme in self.theme_keywords}
        unclassified_docs = []
        
        for doc in documents:
            words = self.preprocess_text(doc)
            doc_themes = []
            
            # Check for theme keywords
            for theme_key, (theme_name, keywords) in self.theme_keywords.items():
                for keyword in keywords:
                    if keyword in ' '.join(words):
                        theme_counts[theme_key] += 1
                        theme_docs[theme_key].append(doc)
                        doc_themes.append(theme_key)
                        break
            
            if not doc_themes:
                unclassified_docs.append(doc)
        
        # Build themes
        themes = []
        for theme_key, count in theme_counts.items():
            if count > 0:
                theme_name, keywords = self.theme_keywords[theme_key]
                themes.append({
                    'theme': theme_name,
                    'keywords': keywords,
                    'documents': theme_docs[theme_key],
                    'size': count
                })
        
        # Add general theme for unclassified documents
        if unclassified_docs:
            themes.append({
                'theme': 'Regulamentação Geral',
                'keywords': ['energia', 'elétrica', 'regulamentação'],
                'documents': unclassified_docs,
                'size': len(unclassified_docs)
            })
        
        # Sort by size and limit to n_clusters
        themes.sort(key=lambda x: x['size'], reverse=True)
        return themes[:n_clusters]

class ThemeNavigatorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Sample regulations data (fallback when Vector Store is not available)
        self.sample_regulations = [
            "Resolução ANEEL sobre tarifas de energia elétrica e reajuste de preços para consumidores residenciais e comerciais",
            "Normativo sobre qualidade do fornecimento de energia elétrica e indicadores de continuidade do serviço",
            "Regulamentação sobre geração distribuída fotovoltaica e compensação de energia elétrica solar",
            "Instrução sobre segurança em instalações elétricas e proteção de trabalhadores do setor",
            "Decreto sobre concessões de transmissão de energia elétrica e leilões públicos de linhas",
            "Portaria sobre fiscalização de distribuidoras de energia elétrica e aplicação de penalidades",
            "Resolução sobre direitos e deveres dos consumidores de energia elétrica residencial",
            "Normativo sobre energia renovável eólica e incentivos para geração limpa sustentável",
            "Regulamentação sobre medição inteligente e modernização do sistema elétrico nacional",
            "Instrução sobre aspectos ambientais da geração de energia elétrica e impactos ao meio ambiente"
        ]
        
        # Try to fetch documents from Vector Store, fallback to sample data
        vector_store_docs = fetch_documents_from_vector_store(query="energia elétrica")
        if vector_store_docs:
            self.regulations = vector_store_docs
            self.using_vector_store = True
            print(f"Using {len(self.regulations)} documents from OpenAI Vector Store")
        else:
            self.regulations = self.sample_regulations
            self.using_vector_store = False
            print(f"Using {len(self.regulations)} sample documents (Vector Store not available)")
        
        self.analyzer = RegulationThemeAnalyzer()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_index()
        elif parsed_path.path == '/api/themes':
            self.serve_themes()
        elif parsed_path.path.startswith('/api/theme/'):
            theme_name = urllib.parse.unquote(parsed_path.path.split('/')[-1])
            self.serve_theme_details(theme_name)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/upload':
            self.handle_upload()
        else:
            self.send_error(404)
    
    def serve_index(self):
        """Serve the main HTML page"""
        try:
            # Try to serve the local version first (no external dependencies)
            try:
                with open('templates/index_local.html', 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback to original version
                with open('templates/index.html', 'r', encoding='utf-8') as f:
                    content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Template not found")
    
    def serve_themes(self):
        """Serve themes API"""
        try:
            themes = self.analyzer.extract_themes_simple(self.regulations)
            response = {
                'success': True,
                'themes': themes,
                'total_documents': len(self.regulations),
                'source': 'vector_store' if self.using_vector_store else 'sample_data'
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_theme_details(self, theme_name):
        """Serve theme details API"""
        try:
            themes = self.analyzer.extract_themes_simple(self.regulations)
            theme = next((t for t in themes if t['theme'] == theme_name), None)
            
            if not theme:
                self.send_error(404, "Theme not found")
                return
            
            # Create sub-themes by further dividing the documents
            sub_themes = []
            if len(theme['documents']) > 1:
                # Simple subdivision: split documents into smaller groups
                docs = theme['documents']
                chunk_size = max(1, len(docs) // 3)
                
                for i in range(0, len(docs), chunk_size):
                    chunk = docs[i:i + chunk_size]
                    sub_themes.append({
                        'theme': f"{theme['theme']} - Parte {i//chunk_size + 1}",
                        'keywords': theme['keywords'][:3],
                        'documents': chunk,
                        'size': len(chunk)
                    })
            else:
                sub_themes = [theme]
            
            response = {
                'success': True,
                'theme': theme,
                'sub_themes': sub_themes
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_upload(self):
        """Handle document upload"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            documents = data.get('documents', [])
            if not documents:
                self.send_error(400, "No documents provided")
                return
            
            themes = self.analyzer.extract_themes_simple(documents)
            response = {
                'success': True,
                'themes': themes,
                'total_documents': len(documents)
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_error(500, str(e))
    
    def send_json_response(self, data):
        """Send JSON response"""
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))

def main():
    """Start the server"""
    PORT = 8000
    
    print(f"Starting Theme Navigator Server...")
    print(f"Server will be available at: http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", PORT), ThemeNavigatorHandler) as httpd:
            print(f"Server started successfully on port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()