#!/usr/bin/env python3
"""
Servidor Web para ANEEL Tracker

Fornece uma interface web amigável para visualização e interação
com pautas e atas da ANEEL.
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime, timedelta
from aneel_tracker import ANEELTracker
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Inicializar tracker global
tracker = ANEELTracker()

# Flag para indicar se já foi carregado
dados_carregados = False


def carregar_dados_iniciais():
    """Carrega dados iniciais ao iniciar o servidor"""
    global dados_carregados

    if not dados_carregados:
        logger.info("Carregando dados iniciais...")

        # Tentar carregar de arquivo JSON se existir
        if os.path.exists('aneel_data.json'):
            try:
                with open('aneel_data.json', 'r', encoding='utf-8') as f:
                    dados = json.load(f)

                logger.info(f"Dados carregados de arquivo: {dados['total_documentos']} documentos")

                # TODO: Reconstruir objetos do tracker a partir do JSON
                # Por enquanto, vamos atualizar diretamente
            except Exception as e:
                logger.error(f"Erro ao carregar dados de arquivo: {e}")

        # Atualizar dados (com menos páginas para ser mais rápido)
        try:
            tracker.atualizar(paginas=2)
            dados_carregados = True
            logger.info("Dados iniciais carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")


@app.route('/')
def index():
    """Página principal"""
    return render_template('aneel_index.html')


@app.route('/api/status')
def get_status():
    """Retorna status do sistema"""
    stats = tracker.estatisticas()

    return jsonify({
        'success': True,
        'status': 'online',
        'dados_carregados': dados_carregados,
        'estatisticas': stats
    })


@app.route('/api/documentos')
def get_documentos():
    """
    Retorna lista de documentos (pautas e atas)

    Query params:
        - tipo: 'pauta' ou 'ata'
        - data_inicio: YYYY-MM-DD
        - data_fim: YYYY-MM-DD
        - limite: número de documentos (padrão: 50)
    """
    try:
        # Parâmetros de filtro
        tipo = request.args.get('tipo')
        limite = int(request.args.get('limite', 50))

        # Datas
        data_inicio = None
        data_fim = None

        if request.args.get('data_inicio'):
            data_inicio = datetime.fromisoformat(request.args.get('data_inicio'))

        if request.args.get('data_fim'):
            data_fim = datetime.fromisoformat(request.args.get('data_fim'))

        # Obter documentos
        documentos = tracker.obter_documentos(tipo=tipo, data_inicio=data_inicio, data_fim=data_fim)

        # Limitar
        documentos = documentos[:limite]

        # Converter para dict
        documentos_dict = [d.to_dict() for d in documentos]

        return jsonify({
            'success': True,
            'total': len(documentos_dict),
            'documentos': documentos_dict
        })

    except Exception as e:
        logger.error(f"Erro ao obter documentos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/documento/<tipo>/<numero>')
def get_documento_detalhes(tipo, numero):
    """Retorna detalhes de um documento específico"""
    try:
        # Buscar documento
        documentos = tracker.obter_documentos(tipo=tipo)
        documento = next((d for d in documentos if d.numero_reuniao == numero), None)

        if not documento:
            return jsonify({
                'success': False,
                'error': 'Documento não encontrado'
            }), 404

        return jsonify({
            'success': True,
            'documento': documento.to_dict()
        })

    except Exception as e:
        logger.error(f"Erro ao obter detalhes do documento: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/temas')
def get_temas():
    """Retorna processos agrupados por tema"""
    try:
        macrotema = request.args.get('macrotema')
        processos_por_tema = tracker.obter_processos_por_tema(macrotema=macrotema)

        # Converter para formato serializável
        resultado = {}
        for tema, processos in processos_por_tema.items():
            resultado[tema] = {
                'total': len(processos),
                'processos': [p.to_dict() for p in processos[:20]]  # Limitar a 20 por tema
            }

        return jsonify({
            'success': True,
            'temas': resultado
        })

    except Exception as e:
        logger.error(f"Erro ao obter temas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/processos')
def get_processos():
    """
    Retorna lista de processos com filtros

    Query params:
        - macrotema: filtrar por macrotema
        - subtema: filtrar por subtema
        - tipo_documento: 'pauta' ou 'ata'
        - limite: número de processos (padrão: 100)
    """
    try:
        macrotema = request.args.get('macrotema')
        subtema = request.args.get('subtema')
        tipo_documento = request.args.get('tipo_documento')
        limite = int(request.args.get('limite', 100))

        # Coletar todos os processos
        processos = []

        documentos = tracker.obter_documentos(tipo=tipo_documento)

        for documento in documentos:
            for processo in documento.processos:
                # Aplicar filtros
                if macrotema and processo.macrotema != macrotema:
                    continue

                if subtema and subtema not in processo.subtemas:
                    continue

                # Adicionar informações do documento
                processo_dict = processo.to_dict()
                processo_dict['documento'] = {
                    'tipo': documento.tipo,
                    'data': documento.data.isoformat(),
                    'numero_reuniao': documento.numero_reuniao,
                    'tipo_reuniao': documento.tipo_reuniao
                }

                processos.append(processo_dict)

        # Limitar
        processos = processos[:limite]

        return jsonify({
            'success': True,
            'total': len(processos),
            'processos': processos
        })

    except Exception as e:
        logger.error(f"Erro ao obter processos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/atualizar', methods=['POST'])
def atualizar_dados():
    """Atualiza os dados do tracker"""
    try:
        data = request.json or {}
        paginas = data.get('paginas', 5)

        logger.info(f"Atualizando dados com {paginas} páginas...")

        # Atualizar
        total = tracker.atualizar(paginas=paginas)

        # Salvar em arquivo
        tracker.exportar_json('aneel_data.json')

        global dados_carregados
        dados_carregados = True

        stats = tracker.estatisticas()

        return jsonify({
            'success': True,
            'total_documentos': total,
            'estatisticas': stats
        })

    except Exception as e:
        logger.error(f"Erro ao atualizar dados: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/pesquisar')
def pesquisar():
    """
    Pesquisa em processos

    Query params:
        - q: termo de pesquisa
        - campo: 'numero', 'assunto', 'deliberacao', 'descricao_sucinta' (padrão: todos)
        - limite: número de resultados (padrão: 50)
    """
    try:
        query = request.args.get('q', '').lower()
        campo = request.args.get('campo')
        limite = int(request.args.get('limite', 50))

        if not query:
            return jsonify({
                'success': False,
                'error': 'Termo de pesquisa não fornecido'
            }), 400

        # Pesquisar em todos os processos
        resultados = []

        for documento in tracker.documentos:
            for processo in documento.processos:
                # Verificar se o termo está presente
                encontrado = False

                if not campo or campo == 'numero':
                    if query in processo.numero.lower():
                        encontrado = True

                if not campo or campo == 'assunto':
                    if query in processo.assunto.lower():
                        encontrado = True

                if not campo or campo == 'deliberacao':
                    if processo.deliberacao and query in processo.deliberacao.lower():
                        encontrado = True

                if not campo or campo == 'descricao_sucinta':
                    if processo.descricao_sucinta and query in processo.descricao_sucinta.lower():
                        encontrado = True

                if encontrado:
                    processo_dict = processo.to_dict()
                    processo_dict['documento'] = {
                        'tipo': documento.tipo,
                        'data': documento.data.isoformat(),
                        'numero_reuniao': documento.numero_reuniao
                    }
                    resultados.append(processo_dict)

        # Limitar
        resultados = resultados[:limite]

        return jsonify({
            'success': True,
            'total': len(resultados),
            'query': query,
            'resultados': resultados
        })

    except Exception as e:
        logger.error(f"Erro na pesquisa: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/relatorio')
def gerar_relatorio():
    """Gera relatório consolidado"""
    try:
        # Parâmetros
        data_inicio_str = request.args.get('data_inicio')
        data_fim_str = request.args.get('data_fim')
        macrotema = request.args.get('macrotema')

        # Filtrar documentos
        data_inicio = datetime.fromisoformat(data_inicio_str) if data_inicio_str else None
        data_fim = datetime.fromisoformat(data_fim_str) if data_fim_str else None

        documentos = tracker.obter_documentos(data_inicio=data_inicio, data_fim=data_fim)

        # Estatísticas
        total_pautas = len([d for d in documentos if d.tipo == 'pauta'])
        total_atas = len([d for d in documentos if d.tipo == 'ata'])

        # Processos por tema
        processos_tema = {}
        total_processos = 0

        for documento in documentos:
            for processo in documento.processos:
                if macrotema and processo.macrotema != macrotema:
                    continue

                total_processos += 1

                if processo.macrotema not in processos_tema:
                    processos_tema[processo.macrotema] = {
                        'total': 0,
                        'subtemas': {}
                    }

                processos_tema[processo.macrotema]['total'] += 1

                for subtema in processo.subtemas:
                    if subtema not in processos_tema[processo.macrotema]['subtemas']:
                        processos_tema[processo.macrotema]['subtemas'][subtema] = 0
                    processos_tema[processo.macrotema]['subtemas'][subtema] += 1

        return jsonify({
            'success': True,
            'relatorio': {
                'periodo': {
                    'inicio': data_inicio.isoformat() if data_inicio else None,
                    'fim': data_fim.isoformat() if data_fim else None
                },
                'totais': {
                    'documentos': len(documentos),
                    'pautas': total_pautas,
                    'atas': total_atas,
                    'processos': total_processos
                },
                'por_tema': processos_tema
            }
        })

    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/exportar/<formato>')
def exportar(formato):
    """
    Exporta dados em diferentes formatos

    Formatos suportados: json, csv
    """
    try:
        if formato == 'json':
            tracker.exportar_json('aneel_export.json')
            return send_from_directory('.', 'aneel_export.json', as_attachment=True)

        elif formato == 'csv':
            # TODO: Implementar exportação CSV
            return jsonify({
                'success': False,
                'error': 'Formato CSV ainda não implementado'
            }), 501

        else:
            return jsonify({
                'success': False,
                'error': 'Formato não suportado'
            }), 400

    except Exception as e:
        logger.error(f"Erro ao exportar: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.before_request
def before_first_request():
    """Executado antes da primeira requisição"""
    carregar_dados_iniciais()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'

    logger.info(f"Iniciando ANEEL Tracker Server na porta {port}...")

    app.run(host='0.0.0.0', port=port, debug=debug)
