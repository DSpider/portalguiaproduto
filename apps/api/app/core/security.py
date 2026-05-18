from hmac import compare_digest

from fastapi import Header, HTTPException, status

from app.core.config import get_settings

ADMIN_TOKEN_HEADER = "X-GPR-Admin-Token"


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        return ""

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return ""

    return token.strip()


def require_admin_auth(
    authorization: str | None = Header(default=None),
    x_gpr_admin_token: str | None = Header(default=None, alias=ADMIN_TOKEN_HEADER),
) -> None:
    settings = get_settings()

    if not settings.admin_auth_enabled:
        return

    if not settings.has_configured_admin_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Autenticacao administrativa nao configurada.",
        )

    provided_token = (x_gpr_admin_token or _extract_bearer_token(authorization)).strip()
    expected_token = settings.admin_api_token.strip()

    if not provided_token or not compare_digest(provided_token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token administrativo invalido ou ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
