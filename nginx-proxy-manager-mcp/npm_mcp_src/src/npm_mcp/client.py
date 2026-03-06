"""Async HTTP client for Nginx Proxy Manager API."""

import logging
from datetime import UTC, datetime, timedelta
import httpx
from .config import settings
from .exceptions import NpmApiError, NpmAuthenticationError, NpmConnectionError, NpmNotFoundError
from .models import AccessList, AuditLogEntry, Certificate, HealthStatus, ProxyHost, Setting, TokenResponse

logger = logging.getLogger(__name__)


class NpmClient:
    def __init__(self, base_url=None, identity=None, secret=None, timeout=30.0):
        self.base_url = (base_url or settings.api_url).rstrip("/")
        self._identity = identity or settings.identity
        self._secret = secret or settings.secret
        self._token: str | None = None
        self._token_expires: datetime | None = None
        self._client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self): return self
    async def __aexit__(self, *args): await self.close()
    async def close(self): await self._client.aclose()

    async def login(self) -> TokenResponse:
        if not self._identity or not self._secret:
            raise NpmAuthenticationError("NPM_IDENTITY and NPM_SECRET must be configured")
        try:
            response = await self._client.post(
                f"{self.base_url}/tokens",
                json={"identity": self._identity, "secret": self._secret},
            )
        except httpx.ConnectError as e:
            raise NpmConnectionError(f"Failed to connect to NPM at {self.base_url}: {e}") from e
        except httpx.TimeoutException as e:
            raise NpmConnectionError(f"Connection to NPM timed out: {e}") from e
        if response.status_code == 401:
            raise NpmAuthenticationError("Invalid credentials")
        if response.status_code != 200:
            raise NpmApiError(f"Login failed: {response.text}", status_code=response.status_code)
        data = response.json()
        token_response = TokenResponse(**data)
        self._token = token_response.token
        self._token_expires = token_response.expires
        return token_response

    def _is_token_valid(self):
        if not self._token or not self._token_expires:
            return False
        return datetime.now(UTC) < (self._token_expires - timedelta(minutes=1))

    async def _ensure_authenticated(self):
        if not self._is_token_valid():
            await self.login()

    async def _request(self, method, endpoint, **kwargs):
        await self._ensure_authenticated()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._token}"
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self._client.request(method, url, headers=headers, **kwargs)
        except httpx.ConnectError as e:
            raise NpmConnectionError(f"Failed to connect to NPM: {e}") from e
        except httpx.TimeoutException as e:
            raise NpmConnectionError(f"Request to NPM timed out: {e}") from e
        if response.status_code == 401:
            await self.login()
            headers["Authorization"] = f"Bearer {self._token}"
            response = await self._client.request(method, url, headers=headers, **kwargs)
            if response.status_code == 401:
                raise NpmAuthenticationError("Re-authentication failed")
        if response.status_code == 404:
            raise NpmNotFoundError(f"Resource not found: {endpoint}")
        if response.status_code >= 400:
            raise NpmApiError(f"API error: {response.text}", status_code=response.status_code)
        return response

    async def get_status(self) -> HealthStatus:
        try:
            response = await self._client.get(f"{self.base_url.replace('/api', '')}/")
            return HealthStatus(status="online", version=response.json().get("version"))
        except Exception:
            await self._ensure_authenticated()
            return HealthStatus(status="online")

    async def get_proxy_hosts(self, expand="owner,certificate") -> list[ProxyHost]:
        response = await self._request("GET", "/nginx/proxy-hosts", params={"expand": expand})
        return [ProxyHost(**host) for host in response.json()]

    async def get_proxy_host(self, host_id, expand="owner,certificate") -> ProxyHost:
        response = await self._request("GET", f"/nginx/proxy-hosts/{host_id}", params={"expand": expand})
        return ProxyHost(**response.json())

    async def get_certificates(self) -> list[Certificate]:
        response = await self._request("GET", "/nginx/certificates")
        return [Certificate(**cert) for cert in response.json()]

    async def get_settings(self) -> list[Setting]:
        response = await self._request("GET", "/settings")
        return [Setting(**s) for s in response.json()]

    async def get_audit_log(self, limit=100, offset=0) -> list[AuditLogEntry]:
        response = await self._request("GET", "/audit-log", params={"limit": limit, "offset": offset})
        return [AuditLogEntry(**entry) for entry in response.json()]

    async def get_access_lists(self) -> list[AccessList]:
        response = await self._request("GET", "/nginx/access-lists")
        return [AccessList(**item) for item in response.json()]

    async def create_proxy_host(self, domain_names, forward_host, forward_port,
                                 forward_scheme="http", certificate_id=None, ssl_forced=True,
                                 hsts_enabled=True, hsts_subdomains=False, http2_support=True,
                                 block_exploits=True, caching_enabled=False,
                                 allow_websocket_upgrade=True, access_list_id=0,
                                 advanced_config="", meta=None) -> ProxyHost:
        payload = {
            "domain_names": domain_names, "forward_host": forward_host, "forward_port": forward_port,
            "forward_scheme": forward_scheme, "certificate_id": certificate_id or 0,
            "ssl_forced": ssl_forced, "hsts_enabled": hsts_enabled, "hsts_subdomains": hsts_subdomains,
            "http2_support": http2_support, "block_exploits": block_exploits,
            "caching_enabled": caching_enabled, "allow_websocket_upgrade": allow_websocket_upgrade,
            "access_list_id": access_list_id, "advanced_config": advanced_config, "meta": meta or {},
        }
        response = await self._request("POST", "/nginx/proxy-hosts", json=payload)
        return ProxyHost(**response.json())

    async def update_proxy_host(self, host_id, **kwargs) -> ProxyHost:
        existing = await self.get_proxy_host(host_id)
        payload = {
            "domain_names": existing.domain_names, "forward_host": existing.forward_host,
            "forward_port": existing.forward_port, "forward_scheme": existing.forward_scheme,
            "certificate_id": existing.certificate_id or 0, "ssl_forced": existing.ssl_forced,
            "hsts_enabled": existing.hsts_enabled, "hsts_subdomains": existing.hsts_subdomains,
            "http2_support": existing.http2_support, "block_exploits": existing.block_exploits,
            "caching_enabled": existing.caching_enabled, "allow_websocket_upgrade": existing.allow_websocket_upgrade,
            "access_list_id": existing.access_list_id, "advanced_config": existing.advanced_config, "meta": existing.meta,
        }
        payload.update({k: v for k, v in kwargs.items() if v is not None})
        response = await self._request("PUT", f"/nginx/proxy-hosts/{host_id}", json=payload)
        return ProxyHost(**response.json())

    async def create_certificate(self, domain_names, email, provider="letsencrypt", dns_challenge=False) -> Certificate:
        payload = {
            "domain_names": domain_names,
            "meta": {"letsencrypt_email": email, "letsencrypt_agree": True, "dns_challenge": dns_challenge},
            "provider": provider,
        }
        response = await self._request("POST", "/nginx/certificates", json=payload)
        return Certificate(**response.json())
