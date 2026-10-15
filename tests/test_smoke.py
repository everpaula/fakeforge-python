"""Smoke tests - roda com `pytest tests/` após instalar o package."""

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


def test_preset_customer_correlacionado():
    ff = FakeForge()
    customers = ff.preset("customer", 1)
    assert len(customers) == 1
    c = customers[0]
    assert "name" in c
    assert "cpf" in c
    assert "email" in c
    assert "phone" in c


def test_rate_limit_hit_raises_error():
    ff = FakeForge()
    # Tenta pedir mais items do que o cap Free permite (100)
    with pytest.raises(FakeForgeError) as exc_info:
        ff.cpf(500)
    assert exc_info.value.status >= 400
