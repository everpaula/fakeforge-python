"""
fakeforge - SDK oficial pra gerar dados brasileiros válidos.

Gere CPFs, CNPJs, CEPs, chaves PIX e cartões de crédito com validação
real (mod-11, Luhn, ANATEL) para testes de software, seed de banco e
fixture de QA.

Uso rápido:

    from fakeforge import FakeForge

    ff = FakeForge()
    cpfs = ff.cpf(10)                          # 10 CPFs válidos
    customers = ff.preset("customer", 100)     # 100 pessoas correlacionadas

Para volumes maiores, use API key do plano Dev:

    ff = FakeForge(api_key="sua_key")
    cpfs = ff.cpf(10000)  # até 10.000 por chamada

Homepage: https://fakeforge.com.br
"""

from fakeforge.client import FakeForge
from fakeforge.exceptions import FakeForgeError

__version__ = "0.2.1"
__all__ = ["FakeForge", "FakeForgeError"]
