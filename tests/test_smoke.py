"""Smoke tests - roda com `pytest tests/` após instalar o package."""

import json
import urllib.request

import pytest
from fakeforge import FakeForge, FakeForgeError


def test_gera_5_cpfs():
    ff = FakeForge()
    cpfs = ff.cpf(5)
    assert len(cpfs) == 5
    for cpf in cpfs:
        assert len(cpf) == 14  # formato XXX.XXX.XXX-XX
        assert cpf[3] == "." and cpf[7] == "." and cpf[11] == "-"


def test_gera_cnpj_alfanumerico():
    ff = FakeForge()
    cnpjs = ff.cnpj_alfa(1)
    assert len(cnpjs) == 1
    # CNPJ tem 14 caracteres úteis (letras + números)
    cleaned = "".join(c for c in cnpjs[0] if c.isalnum())
    assert len(cleaned) == 14


def test_preset_customer_mesma_pessoa():
    ff = FakeForge()
    customers = ff.preset("customer", 1)
    assert len(customers) == 1
    c = customers[0]
    assert c["nome"]
    assert c["cpf"]
    assert c["email"]
    assert c["telefone"]
    assert c["endereco"]["cep"]


def test_customer_atalho():
    assert len(FakeForge().customer(2)) == 2


class _FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps({"data": ["x"]}).encode()


def test_le_chave_do_ambiente(monkeypatch):
    sent = {}

    def fake_urlopen(req, timeout=None):
        sent["key"] = req.get_header("X-api-key")
        return _FakeResponse()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    monkeypatch.setenv("FAKEFORGE_API_KEY", "ff_teste_env")
    FakeForge().cpf(1)
    assert sent["key"] == "ff_teste_env"

    FakeForge(api_key="ff_explicita").cpf(1)
    assert sent["key"] == "ff_explicita"

    monkeypatch.delenv("FAKEFORGE_API_KEY")
    FakeForge().cpf(1)
    assert sent["key"] is None


def test_rate_limit_hit_raises_error():
    ff = FakeForge()
    # Pede mais itens do que o teto sem chave (50) e o do Free (100)
    with pytest.raises(FakeForgeError) as exc_info:
        ff.cpf(500)
    assert exc_info.value.status >= 400
