"""Exceções específicas do FakeForge SDK."""

from typing import Any, Optional


class FakeForgeError(Exception):
    """
    Erro específico do FakeForge com contexto adicional.

    Attributes:
        status: Código HTTP retornado pela API (0 se erro de rede).
        code: Nome do erro (rate_limit_exceeded, quantity_limit_exceeded, etc).
        upgrade_url: URL do checkout do plano superior, quando aplicável.
        plan: Plano do user (anon, free, dev, team).
        daily_limit: Limite diário do plano atual.
        used_today: Quantas chamadas já foram feitas hoje.
    """

    def __init__(
        self,
        message: str,
        status: int = 0,
        body: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        body = body or {}
        self.code = str(body.get("error", "unknown"))
        upgrade_obj = body.get("upgrade")
        if isinstance(upgrade_obj, dict):
            self.upgrade_url = upgrade_obj.get("url")
        else:
            self.upgrade_url = body.get("upgrade_url")
        self.plan = body.get("plan")
        self.daily_limit = body.get("daily_limit")
        self.used_today = body.get("your_usage_today")
