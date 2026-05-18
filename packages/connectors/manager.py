from __future__ import annotations

import logging

from packages.connectors.base import BaseConnector
from packages.connectors.models import ConnectorRequest, ConnectorResponse, NormalizedRecord


class DataSourceManager:
    def __init__(
        self,
        connectors: list[BaseConnector],
        logger: logging.Logger | None = None,
    ) -> None:
        self.connectors = connectors
        self.logger = logger or logging.getLogger("guia_produto_radar.connectors.manager")

    def collect(self, request: ConnectorRequest) -> list[ConnectorResponse]:
        responses: list[ConnectorResponse] = []

        for connector in self.connectors:
            response = connector.fetch(request)
            responses.append(response)

            if not response.ok:
                self.logger.warning(
                    "Conector %s retornou falha: %s",
                    response.source,
                    [error.code for error in response.errors],
                )

        return responses

    def collect_records(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        records: list[NormalizedRecord] = []

        for response in self.collect(request):
            records.extend(response.records)

        return records
