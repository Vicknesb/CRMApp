import { useState } from 'react'
import { useDashboard, useReport, useReportList } from '../hooks/useAnalytics'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const COLORS = ['#507d2a', '#82ca9d', '#ffc658', '#ff7c7c', '#8884d8']

export function AnalyticsDashboardPage(): JSX.Element {
  const { data: dashData, isLoading: dashLoading } = useDashboard()
  const { data: reportsData } = useReportList()
  const [selectedReport, setSelectedReport] = useState('ticket_volume')
  const { data: reportData, isLoading: reportLoading } = useReport(selectedReport)

  const widgets: any[] = dashData?.data?.widgets ?? []
  const reportKeys: string[] = reportsData?.data ?? []
  const reportResult = reportData?.data?.data

  const ticketVolumeChartData = selectedReport === 'ticket_volume' && reportResult
    ? Object.entries(reportResult).map(([k, v]) => ({ name: k, count: v }))
    : []

  return (
    <div className="space-y-6">
      {/* KPI widgets */}
      {dashLoading ? (
        <div className="flex justify-center py-8"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {widgets.map((w) => (
            <div key={w.key} className="stat bg-base-100 border border-base-300 rounded-box p-4">
              <div className="stat-title text-xs truncate">{w.title}</div>
              <div className="stat-value text-xl">
                {w.unit === 'INR' ? `₹${Number(w.value).toLocaleString('en-IN')}` : w.value}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Report selector */}
      <div className="card bg-base-100 border border-base-300 p-4 space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <h3 className="font-semibold">Pre-built Reports</h3>
          <select className="select select-bordered select-sm" value={selectedReport}
            onChange={(e) => setSelectedReport(e.target.value)}>
            {reportKeys.map((k) => (
              <option key={k} value={k}>{k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</option>
            ))}
          </select>
        </div>

        {reportLoading ? (
          <div className="flex justify-center py-8"><span className="loading loading-spinner" /></div>
        ) : selectedReport === 'ticket_volume' && ticketVolumeChartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={ticketVolumeChartData}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" fill="#507d2a" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : reportResult ? (
          <pre className="text-xs bg-base-200 rounded p-3 overflow-auto max-h-60">
            {JSON.stringify(reportResult, null, 2)}
          </pre>
        ) : null}
      </div>
    </div>
  )
}
