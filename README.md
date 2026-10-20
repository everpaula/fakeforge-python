# fakeforge-br

SDK oficial do [FakeForge](https://fakeforge.com.br) para Python: gera dados brasileiros válidos (CPF, CNPJ, CEP, PIX, cartão de crédito) para testes de software.

- ✅ **Zero dependências runtime** (usa `urllib` nativo)
- ✅ **Type hints** em todos os métodos
- ✅ **Python 3.8+**
- ✅ **Validação real**: CPF e CNPJ passam no mod-11 da Receita Federal, cartão no Luhn, telefone com DDD da ANATEL
- ✅ **Presets com dados relacionados**: cliente ou pedido inteiro em 1 chamada, com campos que batem entre si
- ✅ **CNPJ alfanumérico 2026**: cobertura do novo formato (IN RFB 2.229)
- ✅ **Grátis para começar**: 50 chamadas/dia sem chave; chave grátis com 100 itens por chamada; plano Dev (R$29/mês) com 10.000

## Instalação

```bash
pip install fakeforge-br
```

```bash
poetry add fakeforge-br
```

```bash
uv add fakeforge-br
```

## Chave de API

Desde a 0.3.0 o cliente lê a chave da variável de ambiente `FAKEFORGE_API_KEY` quando você não passa `api_key`. Pegue a sua em [fakeforge.com.br/dashboard](https://fakeforge.com.br/dashboard) (grátis, sem cartão).

```bash
export FAKEFORGE_API_KEY=ff_sua_chave
```

| | Chamadas por dia | Itens por chamada | Presets (dados relacionados) |
|---|---|---|---|
| Sem chave | 50 por IP | 50 | amostra de 3 |
| Free (chave grátis) | 50 | 100 | amostra de 3 |
| [Dev](https://fakeforge.com.br/pricing?plan=dev) (R$29/mês) | 10.000 | 10.000 | até 2.000 |
| [Team](https://fakeforge.com.br/pricing?plan=team) (R$79/mês) | 100.000 | 10.000 | até 2.000 |

## Uso rápido

```python
from fakeforge import FakeForge

ff = FakeForge()  # usa FAKEFORGE_API_KEY se existir

# CPFs válidos (mod-11 da Receita Federal)
cpfs = ff.cpf(10)
# ['123.456.789-09', '987.654.321-00', ...]

# CNPJs válidos (mod-11)
cnpjs = ff.cnpj(5)

# Chave PIX no formato BACEN
pix = ff.pix_key(3)

# Cartão de crédito com Luhn válido
cards = ff.credit_card(5)
# [{'number': '...', 'holder': '...', 'expiry': '12/28', 'cvv': '123', 'brand': 'Visa'}, ...]

# Cliente com nome, CPF, email, telefone e endereço da mesma pessoa
[cliente] = ff.customer(1)
print(cliente["nome"], cliente["cpf"], cliente["email"], cliente["endereco"]["city"])
```

## Presets: dados relacionados em 1 chamada

Cada item de um preset é um cliente ou um pedido inteiro, com campos que batem entre si: o email sai do nome, as chaves Pix são o CPF, o email e o celular do próprio cliente, o cartão sai no nome do titular e o total do pedido fecha com os itens.

```python
clientes = ff.preset("customer", 3)  # no Dev, até 2.000

for c in clientes:
    print({
        "nome": c["nome"],          # "Aline Fonseca Vieira"
        "cpf": c["cpf"],            # "640.254.907-06" (mod-11 válido)
        "email": c["email"],        # "aline.fonseca886@gmail.com" (derivado do nome)
        "telefone": c["telefone"],  # "(67) 97576-6589"
        "cidade": c["endereco"]["city"],
    })
```

Presets disponíveis:

| Preset | Retorna |
|---|---|
| `fintech` | cliente + chaves PIX do próprio CPF/email/celular + conta bancária + cartão + score Serasa + renda |
| `ecom` | pedido com cliente, endereços, carrinho de 1 a 5 produtos, pagamento e totais |
| `customer` | nome, CPF, email, telefone e endereço |
| `employee` | pessoa + conta bancária + PIX |
| `company` | empresa + endereço + contato |
| `ecommerce_order` | cliente + cartão + entrega |
| `contact_list` | nome + email + telefone |

Sem chave e no Free a API devolve uma amostra de até 3 por preset; para lotes maiores, use o passe de 7 dias ou o plano Dev.

## Comparação com as bibliotecas populares do PyPI

| Recurso | fakeforge-br | [pycpfcnpj](https://pypi.org/project/pycpfcnpj/) | [brutils-py](https://pypi.org/project/brutils/) | [mkfbr](https://pypi.org/project/mkfbr/) | faker (pt-BR) | python-brasilidades |
|---|---|---|---|---|---|---|
| CPF com mod-11 válido | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| CNPJ com mod-11 válido | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| CNPJ alfanumérico 2026 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Cartão com Luhn + bandeira | ✅ | ❌ | ❌ | ❌ | ⚠️ (genérico) | ❌ |
| PIX BACEN (4 formatos) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Campos relacionados (email do nome, Pix do CPF, cartão do titular) | ✅ | ❌ | ❌ | ⚠️ parcial | ❌ | ❌ |
| DDDs oficiais ANATEL | ✅ (67 DDDs) | ❌ | ⚠️ parcial | ❌ | ❌ | ⚠️ parcial |
| Bancos brasileiros com código COMPE real | ✅ (15) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Presets (fintech, ecom, customer) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export CSV / SQL direto | ✅ (via API) | ❌ | ❌ | ❌ | ❌ | ❌ |
| API HTTP (sem precisar instalar) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Zero dependências runtime | ✅ | ✅ | ✅ | ⚠️ (requer) | ❌ | ✅ |

**Quando escolher cada uma:**

- **pycpfcnpj** se você só precisa de CPF+CNPJ validação/geração puros, lib leve e madura. Sem features extras.
- **brutils-py** se você quer uma lib standalone cobrindo mais docs BR (CPF, CNPJ, RG, CEP, CNH) sem chamar API externa. Nenhum preset.
- **mkfbr** se você quer gerar uma pessoa fictícia completa standalone (nome, endereço, CPF, CNPJ, idade), mas sem presets avançados nem PIX/cartão.
- **python-brasilidades** biblioteca histórica com cobertura média, dev community estabelecida.
- **fakeforge-br** se você precisa de **clientes e pedidos com campos relacionados** (customer, fintech, ecom), **PIX BACEN**, **cartão com Luhn+bandeira**, **CNPJ alfanumérico 2026**, ou **API HTTP** pra consumir de outras linguagens do stack sem instalar dep.

**Resumo:** se seu uso é "quero 1 CPF válido em Python puro", qualquer uma funciona; use pycpfcnpj ou brutils-py. Se seu uso é "quero popular o banco de staging com milhares de clientes com nome, CPF, email e endereço da mesma pessoa, direto em SQL", o fakeforge-br entrega isso em poucas chamadas no plano Dev.

## Uso com pytest

### Fixture reutilizável

```python
# conftest.py
import pytest
from fakeforge import FakeForge

@pytest.fixture(scope="session")
def clientes():
    """Clientes com campos da mesma pessoa. Escopo session pra reutilizar entre testes."""
    return FakeForge().customer(3)  # no Dev, até 2.000


@pytest.fixture(scope="session")
def cpfs_validos():
    """100 CPFs válidos (com a chave grátis; no Dev, até 10.000)."""
    return FakeForge().cpf(100)
```

```python
# test_checkout.py
def test_checkout_aceita_cpf_valido(clientes, client):
    for cliente in clientes:
        response = client.post("/checkout", json={
            "cpf": cliente["cpf"],
            "email": cliente["email"],
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
    help = "Popula banco com 1000 clientes via FakeForge"

    def handle(self, *args, **options):
        ff = FakeForge()  # FAKEFORGE_API_KEY de um plano Dev
        clientes = ff.customer(1000)

        Customer.objects.bulk_create([
            Customer(
                cpf=c["cpf"],
                name=c["nome"],
                email=c["email"],
                phone=c["telefone"],
            )
            for c in clientes
        ])

        self.stdout.write(f"{len(clientes)} clientes inseridos")
```

### FastAPI mock

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from fakeforge import FakeForge

@pytest.fixture
def fake_customer():
    return FakeForge().customer(1)[0]

@pytest.mark.asyncio
async def test_signup(fake_customer, client: AsyncClient):
    response = await client.post("/signup", json=fake_customer)
    assert response.status_code == 201
```

## Planos pagos

Com a chave do plano [Dev (R$29/mês)](https://fakeforge.com.br/pricing?plan=dev): 10.000 chamadas/dia, até 10.000 itens por chamada nos tipos simples e até 2.000 nos presets. Bom pra CI/CD, seed de staging e teste de carga.

```python
from fakeforge import FakeForge

ff = FakeForge()  # FAKEFORGE_API_KEY do plano Dev
cpfs = ff.cpf(10_000)  # cabe em 1 chamada
```

## Tratamento de erros

```python
from fakeforge import FakeForge, FakeForgeError

ff = FakeForge()

try:
    cpfs = ff.cpf(1000)
except FakeForgeError as e:
    if e.status == 429:
        print(f"Limite do dia: {e.used_today}/{e.daily_limit}")
        print(f"Plano Dev: {e.upgrade_url}")
    else:
        raise  # 400 = pediu mais itens que o plano permite por chamada
```

## API completa

### Documentos pessoais

- `cpf(quantity=1, formatted=True) -> list[str]`
- `cnpj(quantity=1, formatted=True) -> list[str]`
- `cnpj_alfa(quantity=1, formatted=True) -> list[str]`: novo formato 2026
- `cnh(quantity=1, formatted=True) -> list[str]`
- `rg(quantity=1, formatted=True) -> list[str]`
- `pis(quantity=1, formatted=True) -> list[str]`
- `renavam(quantity=1, formatted=True) -> list[str]`
- `titulo_eleitor(quantity=1, formatted=True) -> list[str]`
- `placa(quantity=1) -> list[str]`

### Contato

- `email(quantity=1) -> list[str]`
- `phone(quantity=1, formatted=True) -> list[str]`: celular ANATEL
- `landline(quantity=1, formatted=True) -> list[str]`: fixo

### Endereço

- `cep(quantity=1, formatted=True) -> list[str]`
- `address(quantity=1, formatted=True) -> list[dict]`

### Pessoa

- `customer(quantity=1) -> list[dict]`: nome, CPF, email, telefone e endereço da mesma pessoa
- `person(quantity=1, formatted=True) -> list[dict]`: nome e gênero
- `full_name(quantity=1) -> list[str]`

### Financeiro

- `credit_card(quantity=1, formatted=True) -> list[dict]`
- `pix_key(quantity=1) -> list[str]`
- `bank_account(quantity=1, formatted=True) -> list[dict]`: código COMPE real; o dígito da conta é sorteado

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

    ff = FakeForge()  # FAKEFORGE_API_KEY vem do ambiente
    clientes = ff.customer(3)  # no Dev, até 2.000
    CACHE.write_text(json.dumps(clientes, indent=2, ensure_ascii=False))
    return clientes
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
