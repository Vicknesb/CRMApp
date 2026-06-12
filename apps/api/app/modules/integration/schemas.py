from typing import Optional
from pydantic import BaseModel


class ConnectorCreate(BaseModel):
    provider: str        # gmail | outlook | slack | teams | jira | azuredevops | google_calendar | mailchimp
    displayName: Optional[str] = None


class TokenStore(BaseModel):
    provider: str
    accessToken: str
    refreshToken: Optional[str] = None
    expiresAt: Optional[str] = None
    scopes: Optional[str] = None


class WebhookEvent(BaseModel):
    provider: str
    eventType: str
    payload: dict


class OAuthCallbackParams(BaseModel):
    code: str
    state: str


class SlackNotify(BaseModel):
    channel: str
    message: str


class EmailSend(BaseModel):
    to: str
    subject: str
    body: str
    contactId: Optional[str] = None
