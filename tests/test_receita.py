"""receita() (0.5.0). Os testes sem rede trocam o urlopen por um falso. O de determinismo chama a API de
verdade e só roda com FAKEFORGE_API_KEY e FAKEFORGE_RECEITA (o nome de uma receita da sua conta)."""

import io
import json
import os
import urllib.error

import pytest

import fakeforge.client as cliente
from fakeforge import FakeForge, FakeForgeError


class _Resposta(io.BytesIO):
    def __init__(self, corpo: dict) -> None:
        super().__init__(json.dumps(corpo).encode())
        self.status = 200
        self.headers = {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@pytest.fixture
def api_falsa(monkeypatch):
    pedidos = []

    def urlopen(req, timeout=None):
        pedidos.append(req)
        if "nao-existe" in req.full_url:
            corpo = io.BytesIO(json.dumps({"error": "not_found", "message": "Receita não encontrada."}).encode())
            raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {}, corpo)
        return _Resposta({"data": ["12.345.678/0001-95"]})

    monkeypatch.setattr(cliente.urllib.request, "urlopen", urlopen)
    return pedidos


def test_chama_a_receita_com_a_chave(api_falsa):
    dados = FakeForge(api_key="ff_teste").receita("cnpj-fornecedores")
    assert dados == ["12.345.678/0001-95"]
    assert api_falsa[0].full_url == "https://fakeforge.com.br/api/r/cnpj-fornecedores?formato=json"
    assert api_falsa[0].get_header("X-api-key") == "ff_teste"


def test_n_variar_e_versao(api_falsa):
    ff = FakeForge(api_key="ff_teste")
    ff.receita("clientes-sp", n=3, variar=True)
    ff.receita("clientes-sp", versao=1)
    assert api_falsa[0].full_url == "https://fakeforge.com.br/api/r/clientes-sp?formato=json&n=3&variar=1"
    assert api_falsa[1].full_url == "https://fakeforge.com.br/api/r/clientes-sp%40v1?formato=json"


def test_receita_que_nao_existe_vira_erro_404(api_falsa):
    with pytest.raises(FakeForgeError) as erro:
        FakeForge(api_key="ff_teste").receita("nao-existe")
    assert erro.value.status == 404
    assert "não encontrada" in str(erro.value)


@pytest.mark.skipif(not (os.environ.get("FAKEFORGE_API_KEY") and os.environ.get("FAKEFORGE_RECEITA")), reason="precisa de chave e receita")
def test_determinismo_contra_a_api():
    ff = FakeForge()
    nome = os.environ["FAKEFORGE_RECEITA"]
    primeira = ff.receita(nome)
    for _ in range(4):
        assert ff.receita(nome) == primeira
    assert ff.receita(nome, variar=True) != primeira
