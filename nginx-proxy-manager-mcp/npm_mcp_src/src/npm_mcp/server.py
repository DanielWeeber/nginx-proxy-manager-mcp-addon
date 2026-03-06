"""MCP Server implementation for Nginx Proxy Manager."""

import json
import logging
from contextlib import asynccontextmanager
from typing import Any
from mcp.server.fastmcp import FastMCP
from .client import NpmClient
from .config import settings
from .exceptions import NpmApiError, NpmAuthenticationError, NpmConnectionError

logger = logging.getLogger(__name__)
_client: NpmClient | None = None


def get_client() -> NpmClient:
    global _client
    if _client is None:
        _client = NpmClient()
    return _client


@asynccontextmanager
async def lifespan(server: FastMCP):
    global _client
    _client = NpmClient()
    logger.info(f"NPM MCP Server starting, connecting to {settings.api_url}")
    try:
        yield
    finally:
        if _client:
            await _client.close()
            _client = None


mcp = FastMCP(
    "npm-mcp",
    instructions="MCP server for Nginx Proxy Manager - manage reverse proxy configurations",
    lifespan=lifespan,
    host=settings.mcp_host,
    port=settings.mcp_port,
)


def _format_error(e: Exception) -> str:
    if isinstance(e, NpmAuthenticationError): return f"Authentication failed: {e}"
    elif isinstance(e, NpmConnectionError): return f"Connection error: {e}"
    elif isinstance(e, NpmApiError): return f"API error: {e}"
    return f"Error: {e}"


@mcp.tool()
async def list_proxy_hosts() -> str:
    """List all proxy hosts configured in Nginx Proxy Manager."""
    try:
        hosts = await get_client().get_proxy_hosts()
        if not hosts: return "No proxy hosts configured."
        result = []
        for host in hosts:
            domains = ", ".join(host.domain_names)
            result.append(f"{'\u2705' if host.enabled else '\u274c'} [{host.id}] {domains}\n   \u2192 {host.forward_scheme}://{host.forward_host}:{host.forward_port} {'\ud83d\udd12 SSL' if host.ssl_forced else '\ud83d\udd13 HTTP'}")
        return f"Found {len(hosts)} proxy host(s):\n\n" + "\n\n".join(result)
    except Exception as e: return _format_error(e)


@mcp.tool()
async def get_proxy_host_details(host_id: int) -> str:
    """Get detailed configuration for a specific proxy host."""
    try:
        host = await get_client().get_proxy_host(host_id)
        details: dict[str, Any] = {
            "id": host.id, "domains": host.domain_names,
            "forward": {"scheme": host.forward_scheme, "host": host.forward_host, "port": host.forward_port},
            "enabled": host.enabled,
            "ssl": {"forced": host.ssl_forced, "certificate_id": host.certificate_id,
                    "hsts_enabled": host.hsts_enabled, "http2_support": host.http2_support},
            "created_on": host.created_on.isoformat(), "modified_on": host.modified_on.isoformat(),
        }
        return json.dumps(details, indent=2)
    except Exception as e: return _format_error(e)


@mcp.tool()
async def get_system_health() -> str:
    """Check the health and status of the Nginx Proxy Manager instance."""
    try:
        client = get_client()
        status = await client.get_status()
        await client._ensure_authenticated()
        return f"Status: {status.status}\nAuthenticated: \u2705"
    except Exception as e: return _format_error(e)


@mcp.tool()
async def list_certificates() -> str:
    """List all SSL certificates managed by Nginx Proxy Manager."""
    try:
        certs = await get_client().get_certificates()
        if not certs: return "No certificates configured."
        result = []
        for cert in certs:
            domains = ", ".join(cert.domain_names[:3])
            expiry = f" (expires: {cert.expires_on.strftime('%Y-%m-%d')})" if cert.expires_on else ""
            result.append(f"[{cert.id}] {cert.nice_name} ({cert.provider})\n   Domains: {domains}{expiry}")
        return f"Found {len(certs)} certificate(s):\n\n" + "\n\n".join(result)
    except Exception as e: return _format_error(e)


@mcp.tool()
async def list_access_lists() -> str:
    """List all access lists configured in Nginx Proxy Manager."""
    try:
        access_lists = await get_client().get_access_lists()
        if not access_lists: return "No access lists configured."
        return f"Found {len(access_lists)} access list(s):\n\n" + "\n".join(f"[{al.id}] {al.name}" for al in access_lists)
    except Exception as e: return _format_error(e)


@mcp.tool()
async def create_proxy_host(
    domain_names: list[str], forward_host: str, forward_port: int,
    forward_scheme: str | None = None, certificate_id: int | None = None,
    ssl_forced: bool | None = None, block_exploits: bool | None = None,
    allow_websocket_upgrade: bool | None = None, access_list_id: int | None = None,
    advanced_config: str | None = None,
) -> str:
    """Create a new proxy host in Nginx Proxy Manager."""
    try:
        defaults = settings.get_proxy_defaults()
        host = await get_client().create_proxy_host(
            domain_names=domain_names, forward_host=forward_host, forward_port=forward_port,
            forward_scheme=forward_scheme if forward_scheme is not None else defaults["forward_scheme"],
            certificate_id=certificate_id if certificate_id is not None else defaults["certificate_id"],
            ssl_forced=ssl_forced if ssl_forced is not None else defaults["ssl_forced"],
            hsts_enabled=defaults.get("hsts_enabled", True),
            block_exploits=block_exploits if block_exploits is not None else defaults["block_exploits"],
            allow_websocket_upgrade=allow_websocket_upgrade if allow_websocket_upgrade is not None else defaults["allow_websocket_upgrade"],
            access_list_id=access_list_id if access_list_id is not None else defaults["access_list_id"],
            advanced_config=advanced_config if advanced_config is not None else defaults["advanced_config"],
        )
        return f"Successfully created proxy host!\n\nID: {host.id}\nDomains: {', '.join(host.domain_names)}\nForward: {host.forward_scheme}://{host.forward_host}:{host.forward_port}\nSSL: {'Enabled' if host.ssl_forced else 'Disabled'}"
    except Exception as e: return _format_error(e)


@mcp.tool()
async def update_proxy_host(
    host_id: int, forward_host: str | None = None, forward_port: int | None = None,
    forward_scheme: str | None = None, certificate_id: int | None = None,
    ssl_forced: bool | None = None, block_exploits: bool | None = None,
    allow_websocket_upgrade: bool | None = None, access_list_id: int | None = None,
    advanced_config: str | None = None,
) -> str:
    """Update an existing proxy host in Nginx Proxy Manager."""
    try:
        kwargs = {k: v for k, v in {
            "forward_host": forward_host, "forward_port": forward_port, "forward_scheme": forward_scheme,
            "certificate_id": certificate_id, "ssl_forced": ssl_forced, "block_exploits": block_exploits,
            "allow_websocket_upgrade": allow_websocket_upgrade, "access_list_id": access_list_id,
            "advanced_config": advanced_config,
        }.items() if v is not None}
        host = await get_client().update_proxy_host(host_id, **kwargs)
        return f"Successfully updated proxy host!\n\nID: {host.id}\nDomains: {', '.join(host.domain_names)}\nForward: {host.forward_scheme}://{host.forward_host}:{host.forward_port}"
    except Exception as e: return _format_error(e)


@mcp.tool()
async def create_certificate(domain_names: list[str], email: str, dns_challenge: bool = False) -> str:
    """Provision a new Let's Encrypt SSL certificate."""
    try:
        cert = await get_client().create_certificate(domain_names=domain_names, email=email, dns_challenge=dns_challenge)
        expiry = cert.expires_on.strftime("%Y-%m-%d") if cert.expires_on else "N/A"
        return f"Successfully created certificate!\n\nID: {cert.id}\nProvider: {cert.provider}\nDomains: {', '.join(cert.domain_names)}\nExpires: {expiry}"
    except Exception as e: return _format_error(e)
