import os

def gerar_arquivo_grande(nome_arquivo="arquivo_gigante.txt", tamanho_mb=50):
    frase = "Computação Distribuída é o futuro do processamento de dados em larga escala.\n"
    bytes_frase = frase.encode('utf-8')
    repeticoes = (tamanho_mb * 1024 * 1024) // len(bytes_frase)

    print(f"Gerando arquivo de {tamanho_mb}MB... Aguarde.")
    
    with open(nome_arquivo, "wb") as f:
        for _ in range(int(repeticoes)):
            f.write(bytes_frase)
            
    print(f"Sucesso! Arquivo '{nome_arquivo}' gerado com {os.path.getsize(nome_arquivo) / (1024*1024):.2f} MB.")

if __name__ == "__main__":
    gerar_arquivo_grande()