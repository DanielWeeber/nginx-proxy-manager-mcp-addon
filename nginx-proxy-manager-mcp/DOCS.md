# Nginx Proxy Manager MCP – Home Assistant Add-on

Dieses Add-on startet den [nginx-proxy-manager-mcp](https://github.com/b3nw/nginx-proxy-manager-mcp) Server
direkt in Home Assistant. Es stellt einen MCP HTTP-Server bereit, über den KI-Assistenten (z.B. Claude)
deinen Nginx Proxy Manager steuern können.

## Konfiguration

| Option | Beschreibung |
|---|---|
| `npm_api_url` | URL zur NPM API, z.B. `http://192.168.1.10:81/api` |
| `npm_identity` | E-Mail-Adresse für den NPM-Login |
| `npm_secret` | Passwort für den NPM-Login |
| `mcp_host` | Bind-Adresse (Standard: `0.0.0.0`) |
| `mcp_port` | Port des MCP-Servers (Standard: `9115`) |
| `npm_proxy_defaults` | Optionale JSON-Standardwerte für `create_proxy_host`, z.B. `{"certificate_id": 24, "ssl_forced": true}` |

## MCP-Endpunkt

Nach dem Start ist der MCP-Server unter folgender Adresse erreichbar:

```
http://<homeassistant-ip>:9115/
```

## Claude Desktop Konfiguration

```json
{
  "mcpServers": {
    "nginx-proxy-manager": {
      "url": "http://<homeassistant-ip>:9115/"
    }
  }
}
```

## Hinweise

- Der NPM muss von Home Assistant aus erreichbar sein
- Port `9115` muss in der Firewall freigegeben sein, wenn du von außen darauf zugreifen möchtest
- Das Add-on nutzt ausschließlich HTTP-Transport (kein stdio)
