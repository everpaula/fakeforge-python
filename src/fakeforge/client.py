"""Cliente principal do SDK FakeForge."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional, TypeVar, cast

from fakeforge.exceptions import FakeForgeError

T = TypeVar("T")

DEFAULT_BASE_URL = "https://fakeforge.com.br"
DEFAULT_TIMEOUT = 30.0
USER_AGENT = "fakeforge-python-sdk/0.1.0"


class FakeForge:
    """
    Cliente principal do SDK FakeForge.

    Example:
        >>> from fakeforge import FakeForge
        >>> ff = FakeForge()
        >>> cpfs = ff.cpf(10)  # 10 CPFs válidos (mod-11)
        >>> customers = ff.preset("customer", 100)  # pessoa correlacionada

    Example com API key (plano Dev/Team):
        >>> import os
        >>> ff = FakeForge(api_key=os.environ["FAKEFORGE_API_KEY"])
        >>> cpfs = ff.cpf(10000)  # até 10.000 por chamada no Dev
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Args:
            api_key: API key opcional (plano Dev/Team). Sem key, usa tier
                grátis: 50 chamadas/dia por IP.
            base_url: URL base da API. Só mude se for self-hosted.
            timeout: Timeout em segundos pra cada request. Default: 30s.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        type_or_preset: str,
        quantity: int = 1,
        formatted: bool = True,
        is_preset: bool = False,
    ) -> list[Any]:
        params = {
            "quantity": str(quantity),
            "formatted": "true" if formatted else "false",
        }
        if is_preset:
            params["preset"] = type_or_preset
        else:
            params["type"] = type_or_preset

        url = f"{self.base_url}/api/generate?{urllib.parse.urlencode(params)}"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        req = urllib.request.Request(url, headers=headers, method="GET")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                status = response.status
                body_bytes = response.read()
        except urllib.error.HTTPError as e:
            status = e.code
            body_bytes = e.read()
        except urllib.error.URLError as e:
            raise FakeForgeError(f"Erro de rede: {e.reason}", status=0)
        except TimeoutError:
            raise FakeForgeError(f"Timeout após {self.timeout}s", status=0)

        try:
            body = json.loads(body_bytes)
        except json.JSONDecodeError:
            raise FakeForgeError(f"Resposta inválida ({status})", status=status)

        if status >= 400:
            message = body.get("message") or body.get("error") or f"HTTP {status}"
            raise FakeForgeError(message, status=status, body=body)

        data = body.get("data", [])
        return cast(list[Any], data)

    # === Documentos pessoais ===

    def cpf(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera CPFs válidos (mod-11 da Receita Federal)."""
        return self._request("cpf", quantity, formatted)

    def cnpj(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera CNPJs numéricos válidos (mod-11)."""
        return self._request("cnpj", quantity, formatted)

    def cnpj_alfa(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera CNPJs no novo formato alfanumérico (IN RFB 2.229, vigência 01/07/2026)."""
        return self._request("cnpjAlfa", quantity, formatted)

    def cnh(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera CNHs válidas (mod-11 do DENATRAN)."""
        return self._request("cnh", quantity, formatted)

    def rg(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera RGs (formato por estado, mod-11)."""
        return self._request("rg", quantity, formatted)

    def pis(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera PIS/PASEP/NIT/NIS válidos."""
        return self._request("pis", quantity, formatted)

    def renavam(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera RENAVAMs válidos (mod-11 do DENATRAN)."""
        return self._request("renavam", quantity, formatted)

    def titulo_eleitor(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera Títulos de Eleitor válidos."""
        return self._request("tituloEleitor", quantity, formatted)

    def placa(self, quantity: int = 1) -> list[str]:
        """Gera placas Mercosul (formato LLLNLNN)."""
        return self._request("placa", quantity)

    # === Contato ===

    def email(self, quantity: int = 1) -> list[str]:
        """Gera emails com nomes brasileiros e domínios populares."""
        return self._request("email", quantity)

    def phone(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera celulares ANATEL (11 dígitos com 9 na frente + DDD válido)."""
        return self._request("phone", quantity, formatted)

    def landline(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera telefones fixos residenciais (10 dígitos, sem 9)."""
        return self._request("landline", quantity, formatted)

    # === Endereço ===

    def cep(self, quantity: int = 1, formatted: bool = True) -> list[str]:
        """Gera CEPs válidos por estado."""
        return self._request("cep", quantity, formatted)

    def address(self, quantity: int = 1, formatted: bool = True) -> list[dict[str, Any]]:
        """Gera endereços completos (rua, bairro, cidade, estado, CEP)."""
        return self._request("address", quantity, formatted)

    # === Pessoa completa ===

    def person(self, quantity: int = 1, formatted: bool = True) -> list[dict[str, Any]]:
        """Gera pessoa completa correlacionada (nome + CPF + email + telefone)."""
        return self._request("person", quantity, formatted)

    def full_name(self, quantity: int = 1) -> list[str]:
        """Gera nomes completos brasileiros."""
        return self._request("fullName", quantity)

    # === Financeiro ===

    def credit_card(self, quantity: int = 1, formatted: bool = True) -> list[dict[str, Any]]:
        """Gera cartões de crédito com Luhn válido (qualquer bandeira)."""
        return self._request("creditCard", quantity, formatted)

    def pix_key(self, quantity: int = 1) -> list[str]:
        """Gera chaves PIX no formato BACEN (CPF, email, telefone ou EVP UUID)."""
        return self._request("pixKey", quantity)

    def bank_account(self, quantity: int = 1, formatted: bool = True) -> list[dict[str, Any]]:
        """Gera conta bancária brasileira (banco + agência + conta com DV)."""
        return self._request("bankAccount", quantity, formatted)

    # === Empresa ===

    def company(self, quantity: int = 1, formatted: bool = True) -> list[dict[str, Any]]:
        """Gera empresa completa (CNPJ + razão social + endereço)."""
        return self._request("company", quantity, formatted)

    # === Presets correlacionados ===

    def preset(self, name: str, quantity: int = 1, formatted: bool = True) -> list[dict[str, Any]]:
        """
        Gera dados correlacionados via preset.

        Presets disponíveis:
        - customer: pessoa + endereço + email + telefone + PIX
        - employee: pessoa + conta bancária + PIX
        - company: empresa + endereço + contato
        - ecommerce_order: cliente + cartão + entrega
        - contact_list: nome + email + telefone

        Example:
            >>> customers = ff.preset("customer", 100)
            >>> for c in customers:
            ...     print(c["name"], c["cpf"], c["email"])
        """
        return self._request(name, quantity, formatted, is_preset=True)

    # === Genérico ===

    def generate(self, type_: str, quantity: int = 1, formatted: bool = True) -> list[Any]:
        """Genérico: chama a API com qualquer type. Útil pra types sem método dedicado."""
        return self._request(type_, quantity, formatted)
