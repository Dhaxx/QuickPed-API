# app/services/correios_client.py
from httpx import AsyncClient, HTTPError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from pydantic import BaseModel
from typing import Optional

class CepResponse(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    uf: str

client = AsyncClient(timeout=10.0)

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), retry=retry_if_exception_type(HTTPError))
async def _call(url: str, params: dict = None) -> dict:
    resp = await client.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

async def buscar_cep(cep: str) -> Optional[CepResponse]:
    # exemplo usando ViaCEP (REST) — se usar Correios SOAP, adapte com zeep
    url = f"https://viacep.com.br/ws/{cep}/json/"
    data = await _call(url)
    if data.get("erro"):
        return None
    return CepResponse(
        cep=data["cep"],
        logradouro=data.get("logradouro", ""),
        bairro=data.get("bairro", ""),
        cidade=data.get("localidade", ""),
        uf=data.get("uf", ""),
    )