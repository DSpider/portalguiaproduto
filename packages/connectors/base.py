from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod

from packages.connectors.config import ConnectorConfig, load_connector_config
from packages.connectors.errors import ConnectorRuntimeError
from packages.connectors.models import (
    ConnectorError,
    ConnectorRequest,
    ConnectorResponse,
    ConnectorSource,
    NormalizedRecord,
)
from packages.connectors.rate_limit import InMemoryRateLimiter


class BaseConnector(ABC):
    source: ConnectorSource

    def __init__(
        self,
        config: ConnectorConfig | None = None,
        rate_limiter: InMemoryRateLimiter | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.config = config or load_connector_config(self.source)
        self.rate_limiter = rate_limiter or InMemoryRateLimiter()
        self.logger = logger or logging.getLogger(f"guia_produto_radar.connectors.{self.source}")

    def fetch(self, request: ConnectorRequest) -> ConnectorResponse:
        started_at = time.perf_counter()

        if not self.config.enabled:
            return self._response(
                ok=False,
                started_at=started_at,
                errors=[
                    ConnectorError(
                        source=self.source,
                        code="connector_disabled",
                        message="Conector desabilitado por configuracao.",
                        retryable=False,
                    )
                ],
            )

        if not self.rate_limiter.allow(self.source, self.config.rate_limit_per_minute):
            self.logger.warning("Rate limit interno atingido para %s", self.source)
            return self._response(
                ok=False,
                started_at=started_at,
                rate_limited=True,
                errors=[
                    ConnectorError(
                        source=self.source,
                        code="rate_limited",
                        message="Rate limit interno atingido.",
                        retryable=True,
                    )
                ],
            )

        try:
            records = self._fetch(request)
        except ConnectorRuntimeError as exc:
            self.logger.warning("Falha controlada no conector %s: %s", self.source, exc.message)
            return self._response(
                ok=False,
                started_at=started_at,
                errors=[
                    ConnectorError(
                        source=self.source,
                        code=exc.code,
                        message=exc.message,
                        retryable=exc.retryable,
                    )
                ],
            )
        except Exception as exc:
            self.logger.exception("Erro inesperado no conector %s", self.source)
            return self._response(
                ok=False,
                started_at=started_at,
                errors=[
                    ConnectorError(
                        source=self.source,
                        code="unexpected_error",
                        message=str(exc),
                        retryable=True,
                    )
                ],
            )

        return self._response(ok=True, started_at=started_at, records=records)

    @abstractmethod
    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        raise NotImplementedError

    def _response(
        self,
        *,
        ok: bool,
        started_at: float,
        records: list[NormalizedRecord] | None = None,
        errors: list[ConnectorError] | None = None,
        rate_limited: bool = False,
    ) -> ConnectorResponse:
        return ConnectorResponse(
            source=self.source,
            ok=ok,
            records=records or [],
            errors=errors or [],
            rate_limited=rate_limited,
            duration_ms=(time.perf_counter() - started_at) * 1000.0,
        )
