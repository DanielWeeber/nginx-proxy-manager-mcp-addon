"""Pydantic models for NPM API responses."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    token: str
    expires: datetime

class Owner(BaseModel):
    id: int | None = None
    created_on: datetime | None = None
    modified_on: datetime | None = None
    is_disabled: bool = False
    email: str | None = None
    name: str = ""
    nickname: str = ""
    avatar: str = ""
    roles: list[str] = Field(default_factory=list)

class AccessList(BaseModel):
    id: int
    created_on: datetime
    modified_on: datetime
    owner_user_id: int = 0
    name: str
    satisfy_any: bool = False
    pass_auth: bool = False

class Certificate(BaseModel):
    id: int | None = None
    created_on: datetime | None = None
    modified_on: datetime | None = None
    owner_user_id: int | None = None
    provider: str = ""
    nice_name: str = ""
    domain_names: list[str] = Field(default_factory=list)
    expires_on: datetime | None = None
    meta: dict[str, Any] = Field(default_factory=dict)

class ProxyHostLocation(BaseModel):
    path: str
    forward_host: str | None = None
    forward_port: int | None = None
    forward_scheme: str | None = None
    advanced_config: str = ""

class ProxyHost(BaseModel):
    id: int
    created_on: datetime
    modified_on: datetime
    owner_user_id: int
    domain_names: list[str]
    forward_host: str
    forward_port: int
    forward_scheme: str = "http"
    certificate_id: int | None = None
    ssl_forced: bool = False
    hsts_enabled: bool = False
    hsts_subdomains: bool = False
    http2_support: bool = False
    block_exploits: bool = False
    caching_enabled: bool = False
    allow_websocket_upgrade: bool = False
    access_list_id: int = 0
    advanced_config: str = ""
    enabled: bool = True
    meta: dict[str, Any] = Field(default_factory=dict)
    locations: list[ProxyHostLocation] | None = None
    owner: Owner | None = None
    certificate: Certificate | None = None

class HealthStatus(BaseModel):
    status: str
    version: dict[str, str] | None = None

class Setting(BaseModel):
    id: str
    name: str
    description: str
    value: Any
    meta: dict[str, Any] = Field(default_factory=dict)

class AuditLogEntry(BaseModel):
    id: int
    created_on: datetime
    modified_on: datetime
    user_id: int
    object_type: str
    object_id: int
    action: str
    meta: dict[str, Any] = Field(default_factory=dict)
