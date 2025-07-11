import os
import pandas as pd

# Caminhos
DIRETORIO_CERTIFICADOS = 'certificados_final'
ARQUIVO_CSV = 'equipes_participantes.csv'

# Função de limpeza igual à usada na geração dos certificados
def limpar_nome(nome):
    return "".join([c for c in str(nome) if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

# Lê os nomes dos times da planilha e aplica a limpeza
df = pd.read_csv(ARQUIVO_CSV)
nomes_times_planilha = df['nome'].astype(str).apply(limpar_nome)

# Lê os nomes dos certificados no diretório
nomes_certificados = []
for arquivo in os.listdir(DIRETORIO_CERTIFICADOS):
    if arquivo.startswith('Certificado -'):
        nome_time = arquivo.replace('Certificado -', '').replace('.pdf', '').strip()
        nomes_certificados.append(nome_time)

# Converte em set para comparação rápida
nomes_certificados = set(nomes_certificados)

# Compara e pega os que não têm certificado
faltando = [nome_original for nome_original, nome_limpo in zip(df['nome'], nomes_times_planilha)
            if nome_limpo not in nomes_certificados]

# Mostra os resultados
print("Times sem certificado:")
for nome in faltando:
    print(nome)
