# fakeforge

SDK oficial do [FakeForge](https://fakeforge.com.br) para Python — gera dados brasileiros válidos (CPF, CNPJ, CEP, PIX, cartão de crédito) para testes de software.

- ✅ **Zero dependências runtime** (usa `urllib` nativo)
- ✅ **Type hints completos** (compatível com mypy strict)
- ✅ **Python 3.8+**
- ✅ **Validação real** — todos os documentos passam mod-11 da Receita Federal, Luhn, ANATEL
- ✅ **Presets correlacionados** — pessoa completa com CPF + email + endereço + telefone em 1 chamada
- ✅ **CNPJ alfanumérico 2026** — cobertura do novo formato (IN RFB 2.229)
- ✅ **Grátis** — 50 chamadas/dia sem API key, ou 10.000/dia com plano Dev (R$29/mês)

## Instalação

```bash
pip install fakeforge-br
```

```bash
poetry add fakeforge
```

```bash
uv add fakeforge
```

## Uso rápido

```python
from fakeforge import FakeForge

ff = FakeForge()

# CPFs válidos (mod-11 da Receita Federal)
cpfs = ff.cpf(10)
# ['123.456.789-09', '987.654.321-00', ...]

# CNPJs válidos (mod-11)
cnpjs = ff.cnpj(5)

# Chave PIX no formato BACEN
pix = ff.pix_key(3)

# Cartão de crédito com Luhn válido
cards = ff.credit_card(5)
# [{'number': '...', 'brand': 'visa', 'cvv': '123', 'expiry': '12/28'}, ...]

# Pessoa completa correlacionada
[pessoa] = ff.person(1)
print(pessoa["name"], pessoa["cpf"], pessoa["email"])
```

## Presets: dados correlacionados em 1 chamada

Presets retornam objetos com múltiplos campos que se relacionam — email deriva do nome, DDD bate com o estado do endereço, etc.

```python
customers = ff.preset("customer", 100)

for c in customers:
    print({
        "name": c["name"],
        "cpf": c["cpf"],
        "email": c["email"],
        "phone": c["phone"],
        "address": c["address"],
    })
```

Presets disponíveis:

| Preset | Retorna |
|---|---|
| `customer` | pessoa + endereço + email + telefone + PIX |
| `employee` | pessoa + conta bancária + PIX |
| `company` | empresa + endereço + contato |
| `ecommerce_order` | cliente + cartão + entrega |
| `contact_list` | nome + email + telefone |

## Comparação com as bibliotecas populares do PyPI

| Recurso | fakeforge-br | [pycpfcnpj](https://pypi.org/project/pycpfcnpj/) | [brutils-py](https://pypi.org/project/brutils/) | [mkfbr](https://pypi.org/project/mkfbr/) | faker (pt-BR) | python-brasilidades |
|---|---|---|---|---|---|---|
| CPF com mod-11 válido | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| CNPJ com mod-11 válido | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| CNPJ alfanumérico 2026 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Cartão com Luhn + bandeira | ✅ | ❌ | ❌ | ❌ | ⚠️ (genérico) | ❌ |
| PIX BACEN (4 formatos) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| QR Code PIX EMV BR Code | ✅ (via API) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Correlação nome ↔ email ↔ DDD ↔ CEP | ✅ | ❌ | ❌ | ⚠️ parcial | ❌ | ❌ |
| DDDs oficiais ANATEL | ✅ (67 DDDs) | ❌ | ⚠️ parcial | ❌ | ❌ | ⚠️ parcial |
| 17 bancos brasileiros com DV | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Presets bundle (customer, fintech, ecommerce) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export CSV / SQL direto | ✅ (via API) | ❌ | ❌ | ❌ | ❌ | ❌ |
| API HTTP (sem precisar instalar) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Zero dependências runtime | ✅ | ✅ | ✅ | ⚠️ (requer) | ❌ | ✅ |

**Quando escolher cada uma:**

- **pycpfcnpj** se você só precisa de CPF+CNPJ validação/geração puros, lib leve e madura. Sem features extras.
- **brutils-py** se você quer uma lib standalone cobrindo mais docs BR (CPF, CNPJ, RG, CEP, CNH) sem chamar API externa. Nenhuma correlação ou preset.
- **mkfbr** se você quer gerar uma pessoa fictícia completa standalone (nome, endereço, CPF, CNPJ, idade), mas sem presets avançados nem PIX/cartão.
- **python-brasilidades** biblioteca histórica com cobertura média, dev community estabelecida.
- **fakeforge-br** se você precisa de **pessoas correlacionadas** (customer, fintech, ecommerce_order), **PIX BACEN**, **cartão com Luhn+bandeira**, **CNPJ alfanumérico 2026**, ou **API HTTP** pra consumir de outras linguagens do stack sem instalar dep. Também é o único com export SQL direto pra seed em volume.

**Resumo:** se seu uso é "quero 1 CPF válido em Python puro", qualquer uma funciona — use pycpfcnpj ou brutils-py. Se seu uso é "quero popular banco de staging com 10K customers com nome+email+CPF+endereço+PIX coerentes, direto em SQL, sem gastar 2h escrevendo código de glue", fakeforge-br é a única que entrega isso em 1 chamada.

## Uso com pytest

### Fixture reutilizável

```python
# conftest.py
import pytest
from fakeforge import FakeForge

@pytest.fixture(scope="session")
def customers():
    """100 customers correlacionados. Escopo session pra reutilizar entre testes."""
    ff = FakeForge()
    return ff.preset("customer", 100)


@pytest.fixture(scope="session")
def cpfs_validos():
    """1000 CPFs válidos pra teste de load."""
    ff = FakeForge()
    return ff.cpf(1000)
```

```python
# test_checkout.py
def test_checkout_aceita_cpf_valido(customers, client):
    for customer in customers[:20]:
        response = client.post("/checkout", json={
            "cpf": customer["cpf"],
            "email": customer["email"],
        })
        assert response.status_code == 200
```

### Django ORM seed

```python
# management/commands/seed_customers.py
from django.core.management.base import BaseCommand
from fakeforge import FakeForge
from myapp.models import Customer

class Command(BaseCommand):
    help = "Popula banco com 1000 customers via FakeForge"

    def handle(self, *args, **options):
        ff = FakeForge(api_key="sua_key_dev")  # 10.000/dia no Dev
        customers = ff.preset("customer", 1000)

        Customer.objects.bulk_create([
            Customer(
                cpf=c["cpf"],
                name=c["name"],
                email=c["email"],
                phone=c["phone"],
            )
            for c in customers
        ])

        self.stdout.write(f"✓ {len(customers)} customers inseridos")
```

### FastAPI mock

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from fakeforge import FakeForge

@pytest.fixture
def fake_customer():
    ff = FakeForge()
    return ff.preset("customer", 1)[0]

@pytest.mark.asyncio
async def test_signup(fake_customer, client: AsyncClient):
    response = await client.post("/signup", json=fake_customer)
    assert response.status_code == 201
```

## API key opcional (plano Dev/Team)

Sem API key: 50 chamadas/dia por IP, até 100 items por chamada. Perfeito pra dev local.

Com API key do plano [Dev (R$29/mês)](https://fakeforge.com.br/pricing?plan=dev): 10.000 chamadas/dia, até 10.000 items por chamada. Ideal pra CI/CD, seed em produção, load test.

```python
import os
from fakeforge import FakeForge

ff = FakeForge(api_key=os.environ["FAKEFORGE_API_KEY"])
cpfs = ff.cpf(10_000)  # no Dev, cabe em 1 chamada
```

Pegue sua API key em [fakeforge.com.br/dashboard](https://fakeforge.com.br/dashboard).

## Tratamento de erros

```python
from fakeforge import FakeForge, FakeForgeError

ff = FakeForge()

try:
    cpfs = ff.cpf(1000)
except FakeForgeError as e:
    if e.status == 429:
        print(f"Rate limit: {e.used_today}/{e.daily_limit}")
        print(f"Upgrade: {e.upgrade_url}")
    else:
        raise
```

## API completa

### Documentos pessoais

- `cpf(quantity=1, formatted=True) -> list[str]`
- `cnpj(quantity=1, formatted=True) -> list[str]`
- `cnpj_alfa(quantity=1, formatted=True) -> list[str]` — novo formato 2026
- `cnh(quantity=1, formatted=True) -> list[str]`
- `rg(quantity=1, formatted=True) -> list[str]`
- `pis(quantity=1, formatted=True) -> list[str]`
- `renavam(quantity=1, formatted=True) -> list[str]`
- `titulo_eleitor(quantity=1, formatted=True) -> list[str]`
- `placa(quantity=1) -> list[str]`

### Contato

- `email(quantity=1) -> list[str]`
- `phone(quantity=1, formatted=True) -> list[str]` — celular ANATEL
- `landline(quantity=1, formatted=True) -> list[str]` — fixo

### Endereço

- `cep(quantity=1, formatted=True) -> list[str]`
- `address(quantity=1, formatted=True) -> list[dict]`

### Pessoa completa

- `person(quantity=1, formatted=True) -> list[dict]`
- `full_name(quantity=1) -> list[str]`

### Financeiro

- `credit_card(quantity=1, formatted=True) -> list[dict]`
- `pix_key(quantity=1) -> list[str]`
- `bank_account(quantity=1, formatted=True) -> list[dict]`

### Empresa

- `company(quantity=1, formatted=True) -> list[dict]`

### Presets

- `preset(name, quantity=1, formatted=True) -> list[dict]`

### Genérico

- `generate(type_, quantity=1, formatted=True) -> list[Any]`

## Perguntas frequentes

### É legal usar CPFs/CNPJs gerados em testes?

Sim. Gerar números que passam validação matemática (mod-11) pra fins de teste é prática padrão em desenvolvimento. Crime é usar CPF/CNPJ (fake ou real) pra fraude, sonegação ou cadastro em nome de terceiro.

### Os dados batem no DICT/SPC/Serasa?

Não. São dados matematicamente válidos mas não existem em nenhuma base oficial. Perfeito pra teste de formato, validação de schema e seed de staging. Não serve pra teste com API externa que consulta base real.

### Como configurar em CI (GitHub Actions)?

```yaml
- name: Rodar testes com FakeForge
  env:
    FAKEFORGE_API_KEY: ${{ secrets.FAKEFORGE_API_KEY }}
  run: pytest
```

Cache dos dados na primeira chamada evita esgotar quota:

```python
# tests/fixtures.py
import json
from pathlib import Path
from fakeforge import FakeForge

CACHE = Path(__file__).parent / "customers.json"

def get_customers():
    if CACHE.exists():
        return json.loads(CACHE.read_text())

    ff = FakeForge()
    customers = ff.preset("customer", 100)
    CACHE.write_text(json.dumps(customers, indent=2, ensure_ascii=False))
    return customers
```

## Suporte

- 📚 Docs completos: [fakeforge.com.br/docs](https://fakeforge.com.br/docs)
- 💬 Email direto: `hey@fakeforge.com.br`
- 🐛 Issues: [github.com/everpaula/fakeforge-python/issues](https://github.com/everpaula/fakeforge-python/issues)
- 🤝 Quer contribuir? Veja o [CONTRIBUTING.md](CONTRIBUTING.md)

## Licença

MIT — veja [LICENSE](./LICENSE) para detalhes.

---

Feito por [Everton Paula](https://fakeforge.com.br) — engenheiro brasileiro que precisou de dados válidos pra testar checkout PIX e escreveu essa lib porque nenhuma outra funcionava direito.
