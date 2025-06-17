import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
import os

# --- CONFIGURAÇÕES ---
ARQUIVO_CSV = 'equipes.csv'
IMAGEM_FUNDO = os.path.abspath('certificado.png')

COLUNA_TIME = 'nome'
COLUNA_INSTITUICAO = 'instituicao'
COLUNA_ALUNO_1 = 'Nome do Integrante #1 do time:'
COLUNA_ALUNO_2 = 'Nome do Integrante #2 do time:'
COLUNA_ALUNO_3 = 'Nome do Integrante #3 do time:'
COLUNA_COACH = 'Nome do técnico (coach)'

def gerar_pdf(dados_time, pasta_destino):
    """Gera um único certificado em PDF para uma equipe."""
    nome_time = dados_time[COLUNA_TIME]
    instituicao = dados_time[COLUNA_INSTITUICAO]
    alunos = f"{dados_time[COLUNA_ALUNO_1]}, {dados_time[COLUNA_ALUNO_2]} e {dados_time[COLUNA_ALUNO_3]}"
    coach = dados_time[COLUNA_COACH]

    # Cria um nome de arquivo seguro para evitar erros
    nome_arquivo_seguro = "".join([c for c in str(nome_time) if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    nome_arquivo_pdf = os.path.join(pasta_destino, f"Certificado - {nome_arquivo_seguro}.pdf")

    c = canvas.Canvas(nome_arquivo_pdf, pagesize=landscape(letter))
    largura, altura = landscape(letter)

    # Adiciona a imagem de fundo
    try:
        fundo = ImageReader(IMAGEM_FUNDO)
        c.drawImage(fundo, 0, 0, width=largura, height=altura, preserveAspectRatio=True, anchor='c')
    except Exception as e:
        print(f"[ERRO] Falha ao carregar imagem de fundo: {e}")

    # Define o texto do certificado
    texto_completo = (
        f"Certificamos que o time <b>{str(nome_time).upper()}</b> "
        f"da instituição/universidade <b>{str(instituicao).upper()}</b>, "
        f"composto pelos alunos <b>{alunos}</b>, "
        f"tendo como coach/técnico <b>{coach}</b>, "
        "participou da FASE ZERO da MARATONA SBC DE PROGRAMAÇÃO 2025."
    )

    # Estiliza e posiciona o parágrafo
    estilos = getSampleStyleSheet()
    estilo_paragrafo = ParagraphStyle(
        'estilo_certificado',
        parent=estilos['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=24,
        alignment=TA_CENTER,
    )

    paragrafo = Paragraph(texto_completo, estilo_paragrafo)
    
    # Ajusta as margens e a posição do texto
    largura_util = largura - (12 * cm) # Margem esquerda + direita
    posicao_x = 6 * cm # Margem esquerda
    
    w, h = paragrafo.wrap(largura_util, altura)
    posicao_y = altura * 0.45 # Posição vertical
    paragrafo.drawOn(c, posicao_x, posicao_y)

    c.save()
    print(f"[OK] Certificado gerado para o time: {nome_time}")

def main():
    """Lê o arquivo CSV e gera os certificados para as equipes válidas."""
    try:
        df_equipes = pd.read_csv(ARQUIVO_CSV)
        if 'Unnamed: 0' in df_equipes.columns:
            df_equipes = df_equipes.drop('Unnamed: 0', axis=1)

        pasta_destino = "certificados_validos"
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        print("Iniciando a geração de certificados...")
        for indice, linha in df_equipes.iterrows():
            # Pula a linha se o nome do time estiver vazio
            if pd.isna(linha[COLUNA_TIME]):
                continue
            
            # ✅ NOVA VERIFICAÇÃO: Pula a linha se a instituição estiver vazia
            if pd.isna(linha[COLUNA_INSTITUICAO]) or str(linha[COLUNA_INSTITUICAO]).strip() == '':
                print(f"[AVISO] Time '{linha[COLUNA_TIME]}' ignorado por não ter uma instituição definida.")
                continue

            # Se passou em todas as verificações, gera o PDF
            gerar_pdf(linha, pasta_destino)

        print("\n✅ Processo concluído! Certificados salvos na pasta 'certificados'.")

    except FileNotFoundError:
        print(f"ERRO: O arquivo '{ARQUIVO_CSV}' não foi encontrado.")
    except KeyError as e:
        print(f"ERRO: A coluna {e} não foi encontrada no arquivo CSV. Verifique os nomes das colunas.")
    except Exception as e:
        print(f"ERRO inesperado: {e}")

if __name__ == "__main__":
    main()