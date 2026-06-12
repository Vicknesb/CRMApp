// Shared sidebar HTML — call sidebar('leads') to get sidebar with 'leads' active
// Used via <script> include in each page
function sidebar(active) {
  const nav = [
    { id:'dashboard',  label:'Dashboard',    href:'01-dashboard.html',  icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>' },
    { id:'leads',      label:'Leads',        href:'02-leads.html',      icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4-2A1 1 0 018 17v-3.586L3.293 6.707A1 1 0 013 6V4z"/>' },
    { id:'contacts',   label:'Contacts',     href:'03-contacts.html',   icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>' },
    { id:'accounts',   label:'Accounts',     href:'04-accounts.html',   icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>' },
    { id:'pipeline',   label:'Pipeline',     href:'05-pipeline.html',   icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>' },
    { id:'tickets',    label:'Support',      href:'06-tickets.html',    icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>' },
    { id:'projects',   label:'Projects',     href:'07-projects.html',   icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>' },
    { id:'contracts',  label:'Contracts',    href:'08-contracts.html',  icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>' },
    { id:'invoicing',  label:'Invoicing',    href:'09-invoicing.html',  icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>' },
    { id:'campaigns',  label:'Campaigns',    href:'10-campaigns.html',  icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"/>' },
    { id:'analytics',  label:'Analytics',    href:'11-analytics.html',  icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>' },
    { id:'admin',      label:'Admin',        href:'12-admin.html',      icon:'<path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><circle cx="12" cy="12" r="3" stroke-linecap="round" stroke-linejoin="round"/>' },
  ];

  const items = nav.map(n => {
    const isActive = n.id === active;
    return `<a href="${n.href}" class="flex items-center gap-3 px-3 py-2.5 rounded-xl ${isActive ? 'bg-primary text-primary-content font-semibold shadow-sm' : 'hover:bg-base-200 text-base-content/70'} text-sm transition-all">
      <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">${n.icon}</svg>
      ${n.label}
    </a>`;
  });

  return `
  <aside class="w-60 min-h-screen bg-base-100 border-r border-base-300 flex flex-col shadow-sm flex-shrink-0 fixed top-0 left-0 h-full z-20">
    <div class="flex items-center gap-3 px-5 py-4 border-b border-base-300">
      <div class="w-9 h-9 rounded-xl bg-primary flex items-center justify-center shadow">
        <svg class="w-5 h-5 text-primary-content" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
        </svg>
      </div>
      <div><p class="font-extrabold text-base tracking-tight leading-tight">IT CRM</p><p class="text-xs text-base-content/40 leading-tight">IT Services Platform</p></div>
    </div>
    <nav class="flex-1 px-3 py-4 flex flex-col gap-0.5 overflow-y-auto">
      ${items.join('')}
    </nav>
    <div class="px-4 py-3 border-t border-base-300">
      <div class="flex items-center gap-3">
        <div class="avatar placeholder">
          <div class="w-8 rounded-full bg-primary text-primary-content text-xs font-bold"><span>RS</span></div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-xs font-semibold truncate">Ravi Sharma</p>
          <p class="text-xs text-base-content/40 truncate">Sales Executive</p>
        </div>
        <button class="btn btn-ghost btn-xs btn-square opacity-50">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
        </button>
      </div>
    </div>
  </aside>`;
}
