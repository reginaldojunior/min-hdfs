import requests
import os
import json

NODES = ["http://localhost:5001", "http://localhost:5002"]
METADADOS_FILE = "metadados.json"
# Este mapa simula o "NameNode" do Hadoop: guarda onde cada pedaço está
file_metadata = {} 
# Ex: {"meu_video.mp4": ["http://localhost:5001/parte_0", ...]}

def carregar_metadados():
    global file_metadata
    if os.path.exists(METADADOS_FILE):
        with open(METADADOS_FILE, "r") as f:
            file_metadata = json.load(f)

def salvar_metadados():
    with open(METADADOS_FILE, "w") as f:
        json.dump(file_metadata, f, indent=2)

def fazer_upload_distribuido(caminho_arquivo):
    nome_base = os.path.basename(caminho_arquivo)
    file_metadata[nome_base] = []
    
    with open(caminho_arquivo, "rb") as f:
        part_idx = 0
        while True:
            chunk = f.read(1024 * 1024) # 1MB
            if not chunk: break
            
            nome_parte = f"{nome_base}_part_{part_idx}"
            no_alvo = NODES[part_idx % len(NODES)]
            
            # Envia a parte para o nó
            requests.post(f"{no_alvo}/upload/{nome_parte}", data=chunk)
            
            # Guarda o link da parte nos metadados
            file_metadata[nome_base].append(f"{no_alvo}/download/{nome_parte}")
            part_idx += 1
    salvar_metadados()
    print(f"✅ Upload de '{nome_base}' concluído em {part_idx} partes.")

def fazer_download_e_remontar(nome_arquivo):
    if nome_arquivo not in file_metadata:
        carregar_metadados()
    if nome_arquivo not in file_metadata:
        print("Arquivo não encontrado nos metadados!")
        return

    print(f"🔄 Remontando arquivo '{nome_arquivo}' a partir dos nós...")
    
    with open(f"recuperado_{nome_arquivo}", "wb") as f_final:
        for url_parte in file_metadata[nome_arquivo]:
            print(f"Baixando parte de: {url_parte}")
            res = requests.get(url_parte)
            if res.status_code == 200:
                f_final.write(res.content)
            else:
                print(f"❌ Erro crítico: Falha ao baixar parte {url_parte}")
    
    print(f"🏁 Arquivo 'recuperado_{nome_arquivo}' remontado com sucesso!")

# Primeiro enviamos para as pastas serem criadas e o mapa ser preenchido
# fazer_upload_distribuido("arquivo_gigante.txt")

# Agora o download funcionará porque o mapa terá as URLs exatas
# (carrega metadados.json automaticamente se o mapa em memória estiver vazio)
fazer_download_e_remontar("arquivo_gigante.txt")