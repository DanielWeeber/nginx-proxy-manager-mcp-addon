# Nginx Proxy Manager MCP – Home Assistant Add-on

Dieses Add-on startet den [nginx-proxy-manager-mcp](https://github.com/b3nw/nginx-proxy-manager-mcp) Container
direkt in Home Assistant.

## Konfiguration

| Option | Beschreibung |
|---|---|
| `npm_api_url` | URL zur NPM API, z.B. `http://192.168.1.10:81/api` |
| `npm_identity` | E-Mail-Adresse für den NPM-Login |
| `npm_secret` | Passwort für den NPM-Login |
| `mcp_host` | Bind-Adresse (Standard: `0.0.0.0`) |
| `mcp_port` | Port des MCP-Servers (Standard: `9115`) |
| `mcp_transport` | Transport-Modus: `sse` (Standard) oder `http` |
| `npm_proxy_defaults` | Optionale JSON-Standardwerte für `create_proxy_host` |

## MCP-Endpunkt

```
http://<homeassistant-ip>:9115/sse
```

## Claude Desktop Konfiguration

```json
{
  "mcpServers": {
    "nginx-proxy-manager": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://<homeassistant-ip>:9115/sse",
        "--allow-http"
      ]
    }
  }
}
```
