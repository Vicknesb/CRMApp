import pytest
from httpx import AsyncClient
from app.modules.integration.token_vault import encrypt_token, decrypt_token
from app.modules.integration.webhook import verify_slack_signature, verify_github_signature
import hashlib
import hmac
import time


# --- Unit tests: token vault ---
def test_encrypt_decrypt_roundtrip():
    data = {"accessToken": "tok_abc", "refreshToken": "ref_xyz", "expiresAt": None, "scopes": "email"}
    encrypted = encrypt_token(data)
    assert encrypted != "tok_abc"
    decrypted = decrypt_token(encrypted)
    assert decrypted["accessToken"] == "tok_abc"
    assert decrypted["refreshToken"] == "ref_xyz"


def test_encrypted_token_is_different_each_call():
    data = {"accessToken": "same", "refreshToken": None, "expiresAt": None, "scopes": None}
    e1 = encrypt_token(data)
    e2 = encrypt_token(data)
    assert e1 != e2  # random nonce each time


# --- Unit tests: webhook signatures ---
def test_slack_signature_valid():
    secret = "test_slack_secret"
    body = b'{"type":"event_callback"}'
    ts = str(int(time.time()))
    base = f"v0:{ts}:{body.decode()}"
    sig = "v0=" + hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()
    assert verify_slack_signature(body, ts, sig, secret)


def test_slack_signature_invalid():
    assert not verify_slack_signature(b"body", str(int(time.time())), "v0=bad", "secret")


def test_slack_signature_expired():
    secret = "s"
    old_ts = str(int(time.time()) - 400)  # > 5 min old
    assert not verify_slack_signature(b"body", old_ts, "v0=any", secret)


def test_github_signature_valid():
    secret = "test_jira_secret"
    body = b'{"issue":"updated"}'
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_github_signature(body, sig, secret)


def test_github_signature_invalid():
    assert not verify_github_signature(b"body", "sha256=bad", "secret")


# --- Integration tests: API ---
@pytest.mark.asyncio
async def test_list_connectors_empty(auth_client: AsyncClient):
    resp = await auth_client.get("/api/v1/integrations")
    assert resp.status_code == 200
    assert "data" in resp.json()


@pytest.mark.asyncio
async def test_connect_and_disconnect(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/integrations/connect", json={
        "provider": "slack",
        "accessToken": "xoxb-test-token",
        "scopes": "channels:read,chat:write",
    })
    assert resp.status_code == 201
    assert resp.json()["data"]["provider"] == "slack"
    assert resp.json()["data"]["isActive"] is True

    disconnect = await auth_client.delete("/api/v1/integrations/slack")
    assert disconnect.status_code == 200
    assert disconnect.json()["data"]["disconnected"] is True


@pytest.mark.asyncio
async def test_webhook_unknown_provider(auth_client: AsyncClient):
    resp = await auth_client.post("/api/v1/integrations/webhook/unknown_provider", json={
        "provider": "unknown_provider", "eventType": "test", "payload": {}
    })
    assert resp.status_code == 200
    assert resp.json()["data"]["processed"] is False
