import os
import sys
import requests
import zipfile
import shutil
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup
import re

# CONFIG de caminhos

USUARIO = os.environ.get("USERNAME") or os.getlogin()
PASTA_BASE = fr"C:\Users\{USUARIO}\Downloads"

CAMINHO_DRIVER = os.path.join(PASTA_BASE, "chromedriver.exe")
CAMINHO_LOG = os.path.join(PASTA_BASE, "chromedriver.log")

os.makedirs(PASTA_BASE, exist_ok=True)

# LOGss

def log(msg: str):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{timestamp}] {msg}"
        with open(CAMINHO_LOG, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    except Exception as e:
        print("Erro no log:", e)


log("==============================================")
log("ChromeDriver Agent iniciado")
log(f"Pasta base: {PASTA_BASE}")
log("==============================================")

# ver o chromedriver atual

def obter_versao_instalada():
    if not os.path.exists(CAMINHO_DRIVER):
        log("ChromeDriver não encontrado")
        return None

    try:
        saida = subprocess.check_output(
            [CAMINHO_DRIVER, "--version"],
            stderr=subprocess.STDOUT,
            text=True
        ).strip()

        versao = saida.split()[1]
        log(f"Versão instalada: {versao}")
        return versao

    except Exception as e:
        log(f"Erro ao obter versão instalada: {e}")
        return None


def obter_ultima_versao():
    try:
        log("Consultando página oficial do ChromeDriver")

        resp = requests.get(
            "https://chromedriver.chromium.org/downloads",
            timeout=30
        )
        resp.raise_for_status()

        texto = resp.text

        # Regex baseada apenas em texto
        matches = re.findall(r"ChromeDriver\s+([\d.]+)", texto)

        if not matches:
            log("Nenhuma versão encontrada via scraping textual")
            return None, None

        # Remover duplicidades
        versoes = list(set(matches))

        # Ordenando
        versoes.sort(
            key=lambda s: list(map(int, s.split("."))),
            reverse=True
        )

        ultima = versoes[0]
        log(f"Última versão encontrada: {ultima}")

        # url de dowload
        url = f"https://chromedriver.storage.googleapis.com/{ultima}/chromedriver_win32.zip"

        log(f"URL montada: {url}")

        return ultima, url

    except Exception as e:
        log(f"Erro ao consultar versão oficial: {e}")
        return None, None


def atualizar_chromedriver(url: str):
    log("Atualizando ChromeDriver")

    zip_path = os.path.join(PASTA_BASE, "chromedriver.zip")
    temp_dir = os.path.join(PASTA_BASE, "_temp")

    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists(zip_path):
            os.remove(zip_path)
    except Exception:
        pass

    os.makedirs(temp_dir, exist_ok=True)

    # Download
    try:
        log("Baixando nova versão")

        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for bloco in r.iter_content(8192):
                    if bloco:
                        f.write(bloco)

        log("Download concluído")

    except Exception as e:
        log(f"Erro no download: {e}")
        return

    # Extraindo o zip
    try:
        log("Extraindo pacote")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

    except Exception as e:
        log(f"Erro ao extrair zip: {e}")
        return

    # Substituindo/trocando driver
    try:
        log("Substituindo executável")

        for raiz, _, arquivos in os.walk(temp_dir):
            if "chromedriver.exe" in arquivos:
                origem = os.path.join(raiz, "chromedriver.exe")

                try:
                    if os.path.exists(CAMINHO_DRIVER):
                        os.remove(CAMINHO_DRIVER)
                except PermissionError:
                    log("Chromedriver em uso. Feche o navegador.")
                    return

                shutil.move(origem, CAMINHO_DRIVER)
                log("ChromeDriver atualizado com sucesso")
                return

        log("chromedriver.exe não encontrado no pacote")

    finally:
        try:
            shutil.rmtree(temp_dir)
            os.remove(zip_path)
        except Exception:
            pass


def verificar_e_atualizar():
    instalada = obter_versao_instalada()
    ultima, url = obter_ultima_versao()

    if not ultima or not url:
        log("Não foi possível obter versão oficial")
        return

    if instalada == ultima:
        log("ChromeDriver já está atualizado")
        return

    log(f"Atualização necessária ({instalada} → {ultima})")
    atualizar_chromedriver(url)


# iniciando funções

def main():
    try:
        verificar_e_atualizar()
        log("Execução finalizada")
    except Exception as e:
        log(f"Erro geral: {e}")


if __name__ == "__main__":
    main()
