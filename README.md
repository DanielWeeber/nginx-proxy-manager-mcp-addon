# nginx-proxy-manager-mcp-addon

> ⚡ Vibecoded into existence — this is just a skeleton that wraps someone else's Docker container so you don't have to run it separately.

A Home Assistant add-on that runs the excellent [nginx-proxy-manager-mcp](https://github.com/b3nw/nginx-proxy-manager-mcp) server by [@b3nw](https://github.com/b3nw) directly inside Home Assistant — no separate Docker host needed.

## What this does

The [nginx-proxy-manager-mcp](https://github.com/b3nw/nginx-proxy-manager-mcp) project exposes an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that lets AI assistants like Claude manage your [Nginx Proxy Manager](https://nginxproxymanager.com/) — creating proxy hosts, managing SSL certs, etc.

This repo is purely a **Home Assistant add-on wrapper** around that project. It:
- Installs the Python source from the upstream repo during the Docker build
- Wires it into the HA add-on lifecycle (s6-overlay, bashio config)
- Exposes port `9115` for the MCP HTTP endpoint

All the actual logic lives upstream. We're just a cozy little shell around it. 🐚

## Installation

### Step 1: Add the repository

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FDanielWeeber%2Fnginx-proxy-manager-mcp-addon)

Or manually:
1. Go to **Settings → Add-ons → Add-on Store**
2. Click the three-dot menu (top right) → **Repositories**
3. Add: `https://github.com/DanielWeeber/nginx-proxy-manager-mcp-addon`

### Step 2: Install & configure

| Option | Description | Example |
|---|---|---|
| `npm_api_url` | URL to your NPM API | `http://192.168.1.10:81/api` |
| `npm_identity` | NPM login email | `admin@example.com` |
| `npm_secret` | NPM password | `yourpassword` |
| `mcp_port` | Port for the MCP server | `9115` (default) |
| `mcp_host` | Bind address | `0.0.0.0` (default) |
| `npm_proxy_defaults` | Optional JSON defaults for proxy host creation | `{"certificate_id": 24, "ssl_forced": true}` |

### Step 3: Connect your AI assistant

Once the add-on is running, the MCP endpoint is available at:

```
http://<your-homeassistant-ip>:9115/mcp
```

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "nginx-proxy-manager": {
      "url": "http://<your-homeassistant-ip>:9115/mcp"
    }
  }
}
```

## Supported architectures

- `amd64`
- `aarch64` (Raspberry Pi etc.)

## Credits

All credit for the actual MCP server goes to [@b3nw](https://github.com/b3nw) and the [nginx-proxy-manager-mcp](https://github.com/b3nw/nginx-proxy-manager-mcp) project. 🎩

## License

MIT
