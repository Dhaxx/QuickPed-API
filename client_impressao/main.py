import os
import time
import sys
import logging

import requests
from dotenv import load_dotenv

try:
    from escpos.printer import Usb

    ESCPOS_DISPONIVEL = True
except ImportError:
    ESCPOS_DISPONIVEL = False
    print("AVISO: Biblioteca escpos não instalada. Modo simulação ativado.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

load_dotenv()

print(f"DEBUG - API_URL: {os.getenv('API_URL')}")
print(f"DEBUG - USUARIO: {os.getenv('USUARIO')}")
print(f"DEBUG - SENHA: {os.getenv('SENHA')}")


class ImpressoraClient:
    def __init__(self):
        self.api_url = os.getenv("API_URL", "http://localhost:8000")
        self.usuario = os.getenv("USUARIO")
        self.senha = os.getenv("SENHA")
        self.intervalo = int(os.getenv("INTERVALO_POLLS", "5"))

        self.token = None
        self.pedidos_impressos = set()
        self.tested = False

        self.configurar_impressora()

    def configurar_impressora(self):
        """Configura a impressora USB"""
        vendor_id = os.getenv("USB_VENDOR_ID")
        product_id = os.getenv("USB_PRODUCT_ID")

        if vendor_id and product_id and ESCPOS_DISPONIVEL:
            try:
                vendor_id = int(vendor_id, 16)
                product_id = int(product_id, 16)
                self.impressora = Usb(vendor_id, product_id, timeout=5)
                logger.info(
                    f"Impressora USB conectada (VID: {vendor_id:04x}, PID: {product_id:04x})"
                )
            except Exception as e:
                logger.error(f"Erro ao conectar impressora USB: {e}")
                logger.info("Executando em modo SIMULAÇÃO (apenas logs)")
                self.impressora = None
        else:
            logger.info("Modo SIMULAÇÃO (sem impressora USB)")
            self.impressora = None

    def login(self):
        """Faz login na API e obtém token JWT"""
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/admin/autenticacao/login",
                data={"username": self.usuario, "password": self.senha},
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                logger.info("Login realizado com sucesso!")
                return True
            else:
                logger.error(f"Erro no login: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Erro ao conectar na API: {e}")
            return False

    def buscar_pedidos_pendentes(self):
        """Busca pedidos pendentes na API"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.api_url}/api/v1/admin/pedido/pendentes"
            logger.info(f"Buscando pedidos pendentes em: {url}")
            response = requests.get(url, headers=headers)
            logger.info(f"Response status: {response.status_code}")
            if response.status_code == 401:
                logger.warning("Token expirado, fazendo login novamente...")
                if self.login():
                    return self.buscar_pedidos_pendentes()
                return []

            if response.status_code == 200:
                pedidos = response.json()
                logger.info(f"Encontrados {len(pedidos)} pedidos pendentes")
                return pedidos
            else:
                logger.error(
                    f"Erro ao buscar pedidos: {response.status_code} - {response.text}"
                )
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar pedidos: {e}")
            return []

            if response.status_code == 200:
                pedidos = response.json()
                return pedidos
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar pedidos: {e}")
            return []

    def testar_conexao(self):
        """Testa se a API está acessível"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.api_url}/api/v1/admin/Impressao/test"
            response = requests.get(url, headers=headers)
            logger.info(f"Teste conexão - Status: {response.status_code}")
            if response.status_code == 200:
                logger.info(f"Response: {response.json()}")
                return True
            else:
                logger.error(f"Erro no teste: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False

    def chamar_endpoint_impressao(self, pedido_id: int):
        """Chama o endpoint de impressão da API e retorna o texto formatado"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}

            if not self.tested:
                self.testar_conexao()
                self.tested = True

            url = f"{self.api_url}/api/v1/admin/Impressao/pedido/{pedido_id}"
            logger.info(f"Chamando: {url}")
            response = requests.post(url, headers=headers)
            logger.info(f"Response status: {response.status_code}")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"Erro ao chamar endpoint impressão: {response.status_code} - {response.text}"
                )
                return None
        except Exception as e:
            logger.error(f"Erro ao chamar endpoint: {e}")
            return None

    def imprimir_texto(self, texto: str, pedido_id: int):
        """Envia texto para a impressora USB"""
        if self.impressora:
            try:
                self.impressora.text(texto + "\n")
                self.impressora.cut()
                logger.info(f"Pedido #{pedido_id} impresso com sucesso!")
            except Exception as e:
                logger.error(f"Erro ao imprimir: {e}")
        else:
            logger.info(f"[SIMULAÇÃO] Conteúdo a imprimir:\n{texto}")

    def run(self):
        """Loop principal do client"""
        logger.info("Iniciando Client de Impressão...")
        logger.info(f"API: {self.api_url}")
        logger.info(f"Intervalo de polling: {self.intervalo} segundos")

        if not self.login():
            logger.error("Não foi possível fazer login. Encerrando.")
            return

        logger.info("Cliente pronto! Aguardando novos pedidos...")

        while True:
            try:
                pedidos = self.buscar_pedidos_pendentes()

                for pedido in pedidos:
                    pedido_id = pedido.get("id")

                    if pedido_id not in self.pedidos_impressos:
                        logger.info(f"Novo pedido detectado: #{pedido_id}")

                        resultado = self.chamar_endpoint_impressao(pedido_id)

                        if resultado and resultado.get("texto"):
                            self.imprimir_texto(resultado["texto"], pedido_id)
                            self.pedidos_impressos.add(pedido_id)

                time.sleep(self.intervalo)

            except KeyboardInterrupt:
                logger.info("Encerrando cliente...")
                break
            except Exception as e:
                logger.error(f"Erro no loop principal: {e}")
                time.sleep(self.intervalo)


if __name__ == "__main__":
    client = ImpressoraClient()
    client.run()
