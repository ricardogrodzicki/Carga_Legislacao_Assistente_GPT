#!/usr/bin/env python3
"""
ANEEL Tracker - Ferramenta de Acompanhamento de Pautas e Atas da ANEEL

Esta ferramenta realiza o acompanhamento automatizado das pautas e atas
publicadas pela ANEEL (Agência Nacional de Energia Elétrica).

Funcionalidades:
- Coleta automática de pautas e atas do site da ANEEL
- Extração e interpretação de processos listados
- Classificação por macrotemas e subtemas usando IA
- Descrição sucinta de assuntos e deliberações
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import logging
from dataclasses import dataclass, asdict
from collections import defaultdict
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI integration (opcional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI não disponível. Classificação automática desabilitada.")

@dataclass
class Processo:
    """Representa um processo da ANEEL"""
    numero: str
    assunto: str
    deliberacao: Optional[str] = None
    macrotema: Optional[str] = None
    subtemas: List[str] = None
    descricao_sucinta: Optional[str] = None

    def __post_init__(self):
        if self.subtemas is None:
            self.subtemas = []

    def to_dict(self):
        return asdict(self)


@dataclass
class DocumentoANEEL:
    """Representa um documento (pauta ou ata) da ANEEL"""
    tipo: str  # 'pauta' ou 'ata'
    data: datetime
    numero_reuniao: str
    tipo_reuniao: str  # 'Reunião Ordinária', 'Reunião Extraordinária', 'Circuito Deliberativo'
    url: str
    processos: List[Processo]
    data_publicacao: datetime

    def to_dict(self):
        return {
            'tipo': self.tipo,
            'data': self.data.isoformat(),
            'numero_reuniao': self.numero_reuniao,
            'tipo_reuniao': self.tipo_reuniao,
            'url': self.url,
            'processos': [p.to_dict() for p in self.processos],
            'data_publicacao': self.data_publicacao.isoformat()
        }


class ANEELScraper:
    """Scraper para coletar pautas e atas do site da ANEEL"""

    BASE_URL = "https://www2.aneel.gov.br/aplicacoes_liferay/noticias_area/"
    NOTICIAS_URL = f"{BASE_URL}?idAreaNoticia=425"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def coletar_noticias(self, paginas: int = 5) -> List[Dict]:
        """
        Coleta notícias de pautas e atas

        Args:
            paginas: Número de páginas para coletar

        Returns:
            Lista de notícias com informações sobre pautas e atas
        """
        noticias = []

        for pagina in range(paginas):
            try:
                url = f"{self.NOTICIAS_URL}&pagina={pagina}"
                logger.info(f"Coletando página {pagina + 1}...")

                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Encontrar notícias
                items_noticias = soup.find_all('div', class_='noticia-item')

                if not items_noticias:
                    # Tentar encontrar de outra forma
                    items_noticias = soup.find_all(['article', 'div'], class_=re.compile(r'noticia|news|item'))

                for item in items_noticias:
                    noticia = self._extrair_noticia(item)
                    if noticia and self._e_pauta_ou_ata(noticia['titulo']):
                        noticias.append(noticia)

                logger.info(f"Coletadas {len(noticias)} pautas/atas até agora")

            except Exception as e:
                logger.error(f"Erro ao coletar página {pagina}: {e}")
                continue

        return noticias

    def _extrair_noticia(self, item) -> Optional[Dict]:
        """Extrai informações de uma notícia"""
        try:
            # Tentar extrair título
            titulo_elem = item.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'titulo|title|headline'))
            if not titulo_elem:
                titulo_elem = item.find(['h2', 'h3', 'h4', 'a'])

            if not titulo_elem:
                return None

            titulo = titulo_elem.get_text(strip=True)

            # Tentar extrair link
            link = None
            link_elem = item.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                if href.startswith('http'):
                    link = href
                else:
                    link = f"{self.BASE_URL}{href}"

            # Tentar extrair data
            data_elem = item.find(['time', 'span', 'div'], class_=re.compile(r'data|date|time'))
            data_publicacao = None
            if data_elem:
                data_texto = data_elem.get_text(strip=True)
                data_publicacao = self._parse_data(data_texto)

            return {
                'titulo': titulo,
                'url': link,
                'data_publicacao': data_publicacao or datetime.now(),
                'html': str(item)
            }
        except Exception as e:
            logger.error(f"Erro ao extrair notícia: {e}")
            return None

    def _e_pauta_ou_ata(self, titulo: str) -> bool:
        """Verifica se o título é de uma pauta ou ata"""
        titulo_lower = titulo.lower()
        return any(palavra in titulo_lower for palavra in ['pauta', 'ata', 'deliberação', 'deliberacao', 'reunião', 'reuniao', 'circuito'])

    def _parse_data(self, texto_data: str) -> datetime:
        """Converte texto de data para datetime"""
        try:
            # Tentar vários formatos
            formatos = [
                '%d/%m/%Y',
                '%d.%m.%Y',
                '%d-%m-%Y',
                '%Y-%m-%d'
            ]

            # Extrair números da data
            numeros = re.findall(r'\d+', texto_data)
            if len(numeros) >= 3:
                data_str = f"{numeros[0]}/{numeros[1]}/{numeros[2]}"
                for formato in formatos:
                    try:
                        return datetime.strptime(data_str, formato)
                    except:
                        continue
        except:
            pass

        return datetime.now()

    def baixar_documento(self, url: str) -> Optional[bytes]:
        """Baixa documento PDF"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Erro ao baixar documento {url}: {e}")
            return None


class ProcessadorDocumentos:
    """Processa documentos PDF da ANEEL para extrair processos"""

    def __init__(self):
        self.padrao_processo = re.compile(r'(\d{5}\.\d{6}/\d{4}-\d{2})')

    def extrair_processos_do_texto(self, texto: str) -> List[Dict]:
        """
        Extrai processos de um texto

        Args:
            texto: Texto do documento

        Returns:
            Lista de dicionários com informações dos processos
        """
        processos = []

        # Encontrar todos os números de processo
        numeros_processo = self.padrao_processo.findall(texto)

        for numero in numeros_processo:
            # Extrair contexto ao redor do número do processo
            contexto = self._extrair_contexto(texto, numero)

            processo = {
                'numero': numero,
                'assunto': contexto.get('assunto', ''),
                'deliberacao': contexto.get('deliberacao'),
                'texto_completo': contexto.get('texto_completo', '')
            }

            processos.append(processo)

        # Se não encontrou processos pelo padrão, tentar extrair de forma mais flexível
        if not processos:
            processos = self._extrair_processos_flexivel(texto)

        return processos

    def _extrair_contexto(self, texto: str, numero_processo: str) -> Dict:
        """Extrai contexto ao redor de um número de processo"""
        try:
            # Encontrar posição do número do processo
            posicao = texto.find(numero_processo)

            # Extrair até 500 caracteres antes e depois
            inicio = max(0, posicao - 200)
            fim = min(len(texto), posicao + 500)

            contexto_texto = texto[inicio:fim]

            # Tentar identificar assunto
            assunto = self._identificar_assunto(contexto_texto, numero_processo)

            # Tentar identificar deliberação (para atas)
            deliberacao = self._identificar_deliberacao(contexto_texto)

            return {
                'assunto': assunto,
                'deliberacao': deliberacao,
                'texto_completo': contexto_texto.strip()
            }
        except Exception as e:
            logger.error(f"Erro ao extrair contexto: {e}")
            return {}

    def _identificar_assunto(self, texto: str, numero_processo: str) -> str:
        """Identifica o assunto de um processo"""
        # Procurar padrões comuns
        padroes = [
            r'Assunto:\s*(.+?)(?:\n|\.|\||Processo)',
            r'(?:Trata|Trata-se|Refere-se)(?:\s+de)?\s*:\s*(.+?)(?:\n|\.)',
            f'{re.escape(numero_processo)}[:\s-]+(.+?)(?:\n|\.)'
        ]

        for padrao in padroes:
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                assunto = match.group(1).strip()
                if len(assunto) > 10:
                    return assunto[:200]  # Limitar tamanho

        # Se não encontrou, pegar texto após o número do processo
        pos = texto.find(numero_processo)
        if pos >= 0:
            texto_depois = texto[pos + len(numero_processo):pos + len(numero_processo) + 200]
            # Remover caracteres especiais do início
            texto_depois = re.sub(r'^[\s:\-–—.]+', '', texto_depois)
            # Pegar até o primeiro ponto ou quebra de linha
            match = re.search(r'^(.+?)(?:\.|;|\n)', texto_depois)
            if match:
                return match.group(1).strip()
            return texto_depois.strip()

        return "Assunto não identificado"

    def _identificar_deliberacao(self, texto: str) -> Optional[str]:
        """Identifica a deliberação de um processo (para atas)"""
        padroes = [
            r'Deliberação:\s*(.+?)(?:\n\n|Processo)',
            r'(?:Aprovado|Aprovada|Decidido|Deliberado)(?:\s+por)?\s*:\s*(.+?)(?:\n|\.)',
            r'(?:Resultado|Decisão):\s*(.+?)(?:\n|\.)'
        ]

        for padrao in padroes:
            match = re.search(padrao, texto, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:200]

        # Procurar palavras-chave de deliberação
        palavras_deliberacao = ['aprovado', 'rejeitado', 'deferido', 'indeferido', 'homologado']
        texto_lower = texto.lower()

        for palavra in palavras_deliberacao:
            if palavra in texto_lower:
                # Extrair sentença contendo a palavra
                pos = texto_lower.find(palavra)
                inicio = texto_lower.rfind('.', 0, pos) + 1
                fim = texto_lower.find('.', pos)
                if fim == -1:
                    fim = pos + 100

                return texto[inicio:fim].strip()

        return None

    def _extrair_processos_flexivel(self, texto: str) -> List[Dict]:
        """Extração mais flexível quando o padrão standard não funciona"""
        processos = []

        # Procurar por itens numerados que podem ser processos
        padrao_item = re.compile(r'(?:Item|Processo|^\d+[\.\)])\s+(.+?)(?=\n(?:Item|Processo|\d+[\.\)])|$)',
                                 re.MULTILINE | re.DOTALL)

        matches = padrao_item.finditer(texto)

        for i, match in enumerate(matches, 1):
            conteudo = match.group(1).strip()
            if len(conteudo) > 20:  # Filtrar itens muito curtos
                processos.append({
                    'numero': f'Item-{i}',
                    'assunto': conteudo[:300],
                    'deliberacao': None,
                    'texto_completo': conteudo
                })

        return processos


class ClassificadorProcessos:
    """Classifica processos por macrotemas e subtemas usando IA"""

    # Macrotemas do setor elétrico
    MACROTEMAS = {
        'tarifas': {
            'nome': 'Tarifas e Preços',
            'keywords': ['tarifa', 'preço', 'reajuste', 'revisão tarifária', 'valor'],
            'subtemas': ['Reajuste Tarifário', 'Revisão Tarifária', 'Bandeiras Tarifárias',
                        'Estrutura Tarifária', 'Subsídios']
        },
        'distribuicao': {
            'nome': 'Distribuição de Energia',
            'keywords': ['distribuição', 'distribuidora', 'rede', 'fornecimento'],
            'subtemas': ['Qualidade do Serviço', 'Expansão da Rede', 'Concessão',
                        'Perdas Técnicas', 'Medição']
        },
        'transmissao': {
            'nome': 'Transmissão de Energia',
            'keywords': ['transmissão', 'transmissora', 'linha', 'subestação'],
            'subtemas': ['Concessão', 'RAP', 'Reforços', 'Instalações', 'Operação']
        },
        'geracao': {
            'nome': 'Geração de Energia',
            'keywords': ['geração', 'geradora', 'usina', 'produção', 'outorga'],
            'subtemas': ['Geração Distribuída', 'Energia Renovável', 'Térmica',
                        'Hidrelétrica', 'Autorização']
        },
        'consumidor': {
            'nome': 'Direitos do Consumidor',
            'keywords': ['consumidor', 'cliente', 'usuário', 'reclamação'],
            'subtemas': ['Atendimento', 'Faturamento', 'Religação',
                        'Compensação', 'Ressarcimento']
        },
        'fiscalizacao': {
            'nome': 'Fiscalização e Regulação',
            'keywords': ['fiscalização', 'multa', 'penalidade', 'infração', 'autuação'],
            'subtemas': ['Penalidades', 'Processos Sancionadores', 'Compliance',
                        'Indicadores', 'Auditoria']
        },
        'economico_financeiro': {
            'nome': 'Aspectos Econômico-Financeiros',
            'keywords': ['financeiro', 'econômico', 'investimento', 'receita', 'custo'],
            'subtemas': ['Base de Remuneração', 'WACC', 'Investimentos',
                        'Custos Operacionais', 'Receitas']
        },
        'ambiental': {
            'nome': 'Aspectos Ambientais',
            'keywords': ['ambiental', 'meio ambiente', 'licenciamento', 'sustentabilidade'],
            'subtemas': ['Licenciamento', 'Compensação Ambiental', 'Impactos',
                        'Recuperação', 'Estudos']
        },
        'comercializacao': {
            'nome': 'Comercialização de Energia',
            'keywords': ['comercialização', 'mercado', 'ACL', 'ACR', 'leilão'],
            'subtemas': ['Mercado Livre', 'Mercado Regulado', 'Contratos',
                        'Leilões', 'CCEE']
        },
        'outros': {
            'nome': 'Outros Assuntos',
            'keywords': [],
            'subtemas': ['Administrativo', 'Recursos Humanos', 'Tecnologia',
                        'Pesquisa', 'Diversos']
        }
    }

    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.use_openai = OPENAI_AVAILABLE and self.openai_api_key

        if self.use_openai:
            self.client = OpenAI(api_key=self.openai_api_key)
            logger.info("Classificador com OpenAI ativado")
        else:
            logger.info("Classificador em modo keyword-based")

    def classificar_processo(self, processo: Dict) -> Processo:
        """
        Classifica um processo e gera descrição sucinta

        Args:
            processo: Dicionário com informações do processo

        Returns:
            Objeto Processo classificado
        """
        numero = processo.get('numero', '')
        assunto = processo.get('assunto', '')
        deliberacao = processo.get('deliberacao')
        texto_completo = processo.get('texto_completo', assunto)

        if self.use_openai:
            # Usar OpenAI para classificação inteligente
            classificacao = self._classificar_com_openai(texto_completo, deliberacao)
        else:
            # Usar classificação baseada em keywords
            classificacao = self._classificar_por_keywords(texto_completo)

        return Processo(
            numero=numero,
            assunto=assunto,
            deliberacao=deliberacao,
            macrotema=classificacao['macrotema'],
            subtemas=classificacao['subtemas'],
            descricao_sucinta=classificacao['descricao']
        )

    def _classificar_com_openai(self, texto: str, deliberacao: Optional[str]) -> Dict:
        """Classifica usando OpenAI"""
        try:
            # Preparar lista de macrotemas
            macrotemas_lista = [f"{k}: {v['nome']}" for k, v in self.MACROTEMAS.items()]

            prompt = f"""Analise o seguinte processo da ANEEL e forneça:

1. MACROTEMA: Escolha UM dos seguintes macrotemas:
{chr(10).join(macrotemas_lista)}

2. SUBTEMAS: Liste até 3 subtemas específicos

3. DESCRIÇÃO: Uma frase curta e objetiva (máximo 100 caracteres) descrevendo o assunto

Texto do processo:
{texto[:1500]}

{f"Deliberação: {deliberacao}" if deliberacao else ""}

Responda APENAS no formato JSON:
{{"macrotema": "nome_do_macrotema", "subtemas": ["subtema1", "subtema2"], "descricao": "descrição sucinta"}}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em regulação do setor elétrico brasileiro."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )

            resposta = response.choices[0].message.content

            # Extrair JSON da resposta
            match = re.search(r'\{.+\}', resposta, re.DOTALL)
            if match:
                resultado = json.loads(match.group())

                # Mapear nome do macrotema para o nome completo
                macrotema_key = resultado.get('macrotema', 'outros')
                if macrotema_key in self.MACROTEMAS:
                    macrotema = self.MACROTEMAS[macrotema_key]['nome']
                else:
                    # Tentar encontrar por nome
                    macrotema = next(
                        (v['nome'] for v in self.MACROTEMAS.values()
                         if v['nome'].lower() == macrotema_key.lower()),
                        self.MACROTEMAS['outros']['nome']
                    )

                return {
                    'macrotema': macrotema,
                    'subtemas': resultado.get('subtemas', [])[:3],
                    'descricao': resultado.get('descricao', '')[:100]
                }

        except Exception as e:
            logger.error(f"Erro na classificação com OpenAI: {e}")

        # Fallback para keyword-based
        return self._classificar_por_keywords(texto)

    def _classificar_por_keywords(self, texto: str) -> Dict:
        """Classifica baseado em palavras-chave"""
        texto_lower = texto.lower()

        # Contar matches para cada macrotema
        scores = {}
        for key, info in self.MACROTEMAS.items():
            score = sum(1 for keyword in info['keywords'] if keyword in texto_lower)
            if score > 0:
                scores[key] = score

        # Selecionar macrotema com maior score
        if scores:
            melhor_tema = max(scores.items(), key=lambda x: x[1])[0]
            macrotema = self.MACROTEMAS[melhor_tema]['nome']
            subtemas = self.MACROTEMAS[melhor_tema]['subtemas'][:2]
        else:
            macrotema = self.MACROTEMAS['outros']['nome']
            subtemas = ['Geral']

        # Gerar descrição simples
        descricao = texto[:100].strip()
        if len(descricao) == 100:
            descricao += '...'

        return {
            'macrotema': macrotema,
            'subtemas': subtemas,
            'descricao': descricao
        }


class ANEELTracker:
    """Classe principal para acompanhamento de pautas e atas da ANEEL"""

    def __init__(self, openai_api_key: Optional[str] = None):
        self.scraper = ANEELScraper()
        self.processador = ProcessadorDocumentos()
        self.classificador = ClassificadorProcessos(openai_api_key)
        self.documentos: List[DocumentoANEEL] = []

    def atualizar(self, paginas: int = 5) -> int:
        """
        Atualiza a base de pautas e atas

        Args:
            paginas: Número de páginas para coletar

        Returns:
            Número de documentos coletados
        """
        logger.info("Iniciando coleta de pautas e atas...")

        # Coletar notícias
        noticias = self.scraper.coletar_noticias(paginas)

        logger.info(f"Total de {len(noticias)} pautas/atas encontradas")

        # Processar cada notícia
        for noticia in noticias:
            try:
                documento = self._processar_noticia(noticia)
                if documento:
                    self.documentos.append(documento)
            except Exception as e:
                logger.error(f"Erro ao processar notícia: {e}")
                continue

        logger.info(f"Total de {len(self.documentos)} documentos processados")
        return len(self.documentos)

    def _processar_noticia(self, noticia: Dict) -> Optional[DocumentoANEEL]:
        """Processa uma notícia e extrai informações"""
        titulo = noticia['titulo']

        # Determinar tipo (pauta ou ata)
        tipo = 'pauta' if 'pauta' in titulo.lower() else 'ata'

        # Extrair informações do título
        info = self._extrair_info_titulo(titulo)

        # Extrair processos do texto (simulado - em produção, baixaria o PDF)
        # Por enquanto, vamos criar processos de exemplo baseado no título
        processos_raw = self._extrair_processos_simulado(titulo)

        # Classificar processos
        processos = []
        for proc in processos_raw:
            processo_classificado = self.classificador.classificar_processo(proc)
            processos.append(processo_classificado)

        return DocumentoANEEL(
            tipo=tipo,
            data=info['data'],
            numero_reuniao=info['numero_reuniao'],
            tipo_reuniao=info['tipo_reuniao'],
            url=noticia.get('url', ''),
            processos=processos,
            data_publicacao=noticia['data_publicacao']
        )

    def _extrair_info_titulo(self, titulo: str) -> Dict:
        """Extrai informações do título"""
        # Extrair data
        data_match = re.search(r'(\d{1,2})[/\.](\d{1,2})[/\.](\d{4})', titulo)
        if data_match:
            dia, mes, ano = data_match.groups()
            data = datetime(int(ano), int(mes), int(dia))
        else:
            data = datetime.now()

        # Extrair número da reunião
        numero_match = re.search(r'(?:nº|n°|n\.?)\s*(\d+)', titulo, re.IGNORECASE)
        numero_reuniao = numero_match.group(1) if numero_match else 'S/N'

        # Determinar tipo de reunião
        if 'extraordinária' in titulo.lower():
            tipo_reuniao = 'Reunião Extraordinária'
        elif 'circuito' in titulo.lower():
            tipo_reuniao = 'Circuito Deliberativo'
        else:
            tipo_reuniao = 'Reunião Ordinária'

        return {
            'data': data,
            'numero_reuniao': numero_reuniao,
            'tipo_reuniao': tipo_reuniao
        }

    def _extrair_processos_simulado(self, titulo: str) -> List[Dict]:
        """
        Cria processos de exemplo (simulação)
        Em produção, isso baixaria e processaria o PDF real
        """
        # Por enquanto, retorna um processo de exemplo
        return [{
            'numero': '48500.123456/2024-01',
            'assunto': titulo,
            'deliberacao': None,
            'texto_completo': titulo
        }]

    def obter_documentos(self, tipo: Optional[str] = None,
                        data_inicio: Optional[datetime] = None,
                        data_fim: Optional[datetime] = None) -> List[DocumentoANEEL]:
        """
        Obtém documentos filtrados

        Args:
            tipo: 'pauta' ou 'ata' (None para ambos)
            data_inicio: Data inicial
            data_fim: Data final

        Returns:
            Lista de documentos filtrados
        """
        documentos = self.documentos

        if tipo:
            documentos = [d for d in documentos if d.tipo == tipo]

        if data_inicio:
            documentos = [d for d in documentos if d.data >= data_inicio]

        if data_fim:
            documentos = [d for d in documentos if d.data <= data_fim]

        return sorted(documentos, key=lambda d: d.data, reverse=True)

    def obter_processos_por_tema(self, macrotema: Optional[str] = None) -> Dict[str, List[Processo]]:
        """
        Agrupa processos por macrotema

        Args:
            macrotema: Filtrar por macrotema específico

        Returns:
            Dicionário com processos agrupados por tema
        """
        processos_por_tema = defaultdict(list)

        for documento in self.documentos:
            for processo in documento.processos:
                if not macrotema or processo.macrotema == macrotema:
                    processos_por_tema[processo.macrotema].append(processo)

        return dict(processos_por_tema)

    def exportar_json(self, arquivo: str):
        """Exporta dados para JSON"""
        dados = {
            'data_atualizacao': datetime.now().isoformat(),
            'total_documentos': len(self.documentos),
            'documentos': [d.to_dict() for d in self.documentos]
        }

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        logger.info(f"Dados exportados para {arquivo}")

    def estatisticas(self) -> Dict:
        """Retorna estatísticas dos dados coletados"""
        total_processos = sum(len(d.processos) for d in self.documentos)

        # Contar por tipo
        pautas = [d for d in self.documentos if d.tipo == 'pauta']
        atas = [d for d in self.documentos if d.tipo == 'ata']

        # Contar por macrotema
        temas = defaultdict(int)
        for documento in self.documentos:
            for processo in documento.processos:
                temas[processo.macrotema] += 1

        return {
            'total_documentos': len(self.documentos),
            'total_pautas': len(pautas),
            'total_atas': len(atas),
            'total_processos': total_processos,
            'processos_por_tema': dict(temas),
            'data_mais_recente': max((d.data for d in self.documentos), default=None),
            'data_mais_antiga': min((d.data for d in self.documentos), default=None)
        }


# Função auxiliar para uso standalone
def main():
    """Função principal para execução standalone"""
    import argparse

    parser = argparse.ArgumentParser(description='ANEEL Tracker - Acompanhamento de Pautas e Atas')
    parser.add_argument('--paginas', type=int, default=5, help='Número de páginas para coletar')
    parser.add_argument('--output', type=str, default='aneel_data.json', help='Arquivo de saída')
    args = parser.parse_args()

    # Criar tracker
    tracker = ANEELTracker()

    # Atualizar dados
    tracker.atualizar(paginas=args.paginas)

    # Mostrar estatísticas
    stats = tracker.estatisticas()
    print("\n=== Estatísticas ===")
    print(f"Total de documentos: {stats['total_documentos']}")
    print(f"Pautas: {stats['total_pautas']}")
    print(f"Atas: {stats['total_atas']}")
    print(f"Total de processos: {stats['total_processos']}")
    print("\nProcessos por tema:")
    for tema, count in sorted(stats['processos_por_tema'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {tema}: {count}")

    # Exportar
    tracker.exportar_json(args.output)
    print(f"\nDados exportados para {args.output}")


if __name__ == '__main__':
    main()
