"""Aviso de chave grátis, sem rede: troca o urlopen por um falso."""

import io
import json

import pytest

import fakeforge.client as cliente
from fakeforge import FakeForge

AVISO = "Sem chave: 100 itens por dia. Pegue em 1 minuto: https://fakeforge.com.br/chave?de=sdk-python"


class _RespostaFalsa(io.BytesIO):
    def __init__(self, com_aviso: bool) -> None:
        super().__init__(json.dumps({"data": ["123.456.789-09"]}).encode())
        self.status = 200
        self.headers = {"X-FakeForge-Aviso": AVISO} if com_aviso else {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@pytest.fixture
def api_falsa(monkeypatch):
    pedidos = []

    def urlopen(req, timeout=None):
        pedidos.append(req)
        return _RespostaFalsa(com_aviso=not req.get_header("X-api-key"))

    monkeypatch.setattr(cliente.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(cliente, "_avisou", False)
    monkeypatch.delenv("FAKEFORGE_SILENCIAR", raising=False)
    return pedidos


def test_sem_chave_avisa_uma_vez(api_falsa, capsys):
    ff = FakeForge(api_key="")
    ff.cpf(1)
    ff.cpf(1)
    FakeForge(api_key="").cnpj(1)
    erro = capsys.readouterr().err
    assert erro.count(AVISO) == 1
    assert erro.strip().count("\n") == 0
    assert api_falsa[0].get_header("User-agent") == "fakeforge-python-sdk/0.5.0"


def test_com_chave_nao_avisa(api_falsa, capsys):
    FakeForge(api_key="ff_teste").cpf(1)
    assert capsys.readouterr().err == ""


def test_silenciar_esconde(api_falsa, capsys, monkeypatch):
    monkeypatch.setenv("FAKEFORGE_SILENCIAR", "1")
    FakeForge(api_key="").cpf(1)
    assert capsys.readouterr().err == ""
