import apiClient from "@/lib/apiClient";

export interface Connector {
  id: string;
  provider: string;
  isActive: boolean;
  connectedAt: string;
}

export const PROVIDERS = [
  { key: "gmail",            label: "Gmail",             icon: "📧", category: "Email" },
  { key: "outlook",          label: "Outlook",           icon: "📬", category: "Email" },
  { key: "slack",            label: "Slack",             icon: "💬", category: "Messaging" },
  { key: "teams",            label: "Microsoft Teams",   icon: "🟦", category: "Messaging" },
  { key: "jira",             label: "Jira",              icon: "🔧", category: "Project" },
  { key: "azuredevops",      label: "Azure DevOps",      icon: "🔵", category: "Project" },
  { key: "google_calendar",  label: "Google Calendar",   icon: "📅", category: "Calendar" },
  { key: "mailchimp",        label: "Mailchimp",         icon: "🐵", category: "Marketing" },
];

export const integrationsApi = {
  list: (): Promise<{ data: Connector[] }> => apiClient.get("/api/v1/integrations"),
  connect: (body: { provider: string; accessToken: string; scopes?: string }): Promise<Connector> =>
    apiClient.post("/api/v1/integrations/connect", body),
  disconnect: (provider: string): Promise<unknown> =>
    apiClient.delete(`/api/v1/integrations/${provider}`),
  sendEmail: (body: { to: string; subject: string; body: string; contactId?: string }) =>
    apiClient.post("/api/v1/integrations/email/send", body),
  slackNotify: (body: { channel: string; message: string }) =>
    apiClient.post("/api/v1/integrations/slack/notify", body),
  syncCalendar: () => apiClient.post("/api/v1/integrations/calendar/sync", {}),
};
