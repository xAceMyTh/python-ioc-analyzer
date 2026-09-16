import re
import ipaddress
from collections import Counter
from pathlib import Path

def extrair_iocs(conteudo):
    padrao_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    padrao_dominio = r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"
    padrao_url = r"https?://[^\s]+"
    padrao_md5 = r"\b[a-fA-F0-9]{32}\b"
    padrao_sha256 = r"\b[a-fA-F0-9]{64}\b"
    ips_encontrados = re.findall(padrao_ip, conteudo)
    dominios_encontrados = re.findall(padrao_dominio, conteudo)
    urls_encontradas = re.findall(padrao_url, conteudo)
    md5_encontrados = re.findall(padrao_md5, conteudo)
    sha256_encontrados = re.findall(padrao_sha256, conteudo)
  
    dominios_filtrados = []

    for dominio in dominios_encontrados:
        if not dominio.lower().endswith((".exe", ".dll", ".zip", ".pdf", ".js")):
            dominios_filtrados.append(dominio)

    ips_validos = []

    for ip in ips_encontrados:
        try:
            ipaddress.ip_address(ip)
            ips_validos.append(ip)
        except ValueError:
            pass

    contagem_ips = Counter(ips_validos)
    contagem_dominios = Counter(dominios_filtrados)
    contagem_urls = Counter(urls_encontradas)
    contagem_md5 = Counter(md5_encontrados)
    contagem_sha256 = Counter(sha256_encontrados)

    return (
    contagem_ips,
    contagem_dominios,
    contagem_urls,
    contagem_md5,
    contagem_sha256
)

def gerar_relatorio(ips, dominios, urls, md5, sha256, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as relatorio:
        relatorio.write("IOC Analysis Report\n")
        relatorio.write("===================\n\n")
        total_iocs = len(ips) + len(dominios) + len(urls) + len(md5) + len(sha256)
        relatorio.write(f"Total de IOCs únicos: {total_iocs}\n")
        relatorio.write(f"IPs únicos: {len(ips)}\n")
        relatorio.write(f"Domínios únicos: {len(dominios)}\n")
        relatorio.write(f"URLs únicas: {len(urls)}\n")
        relatorio.write(f"Hashes MD5 únicos: {len(md5)}\n")
        relatorio.write(f"Hashes SHA-256 únicos: {len(sha256)}\n\n")
        relatorio.write("IPs encontrados:\n")
      
        for ip, quantidade in sorted(ips.items()):
            relatorio.write(f"- {ip} - {quantidade} ocorrência(s)\n")

        relatorio.write("\nDomínios encontrados:\n")
        for dominio, quantidade in sorted(dominios.items()):
            relatorio.write(f"- {dominio} - {quantidade} ocorrência(s)\n")

        relatorio.write("\nURLs encontradas:\n")
        for url, quantidade in sorted(urls.items()):
            relatorio.write(f"- {url} - {quantidade} ocorrência(s)\n")

        relatorio.write("\nHashes MD5 encontrados:\n")
        for hash_md5, quantidade in sorted(md5.items()):
            relatorio.write(f"- {hash_md5} - {quantidade} ocorrência(s)\n")

        relatorio.write("\nHashes SHA-256 encontrados:\n")
        for hash_sha256, quantidade in sorted(sha256.items()):
            relatorio.write(f"- {hash_sha256} - {quantidade} ocorrência(s)\n")


nome_arquivo = input("Digite o nome do arquivo que deseja analisar: ")
nome_base = Path(nome_arquivo).stem
caminho_relatorio = f"output/{nome_base}_ioc_report.txt"

caminho_arquivo = f"input/{nome_arquivo}"

try:
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    raise SystemExit

ips, dominios, urls, md5, sha256 = extrair_iocs(conteudo)
total_iocs = len(ips) + len(dominios) + len(urls) + len(md5) + len(sha256)

print("IPs encontrados:")
for ip, quantidade in sorted(ips.items()):
    print(f"{ip} - {quantidade} ocorrência(s)")

print("\nDomínios encontrados:")
for dominio, quantidade in sorted(dominios.items()):
    print(f"{dominio} - {quantidade} ocorrência(s)")

print("\nURLs encontradas:")
for url, quantidade in sorted(urls.items()):
    print(f"{url} - {quantidade} ocorrência(s)")

print("\nHashes MD5 encontrados:")
for hash_md5, quantidade in sorted(md5.items()):
    print(f"{hash_md5} - {quantidade} ocorrência(s)")

print("\nHashes SHA-256 encontrados:")
for hash_sha256, quantidade in sorted(sha256.items()):
    print(f"{hash_sha256} - {quantidade} ocorrência(s)")

total_iocs = len(ips) + len(dominios) + len(urls) + len(md5) + len(sha256)

print(f"\nTotal de IOCs únicos encontrados: {total_iocs}")

gerar_relatorio(ips, dominios, urls, md5, sha256, caminho_relatorio)

print(f"\nRelatório gerado em: {caminho_relatorio}")
