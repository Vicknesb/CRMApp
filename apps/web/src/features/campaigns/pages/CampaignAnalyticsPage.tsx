import { useParams } from 'react-router-dom'
import { useCampaign, useCampaignMetrics } from '../hooks/useCampaigns'
import { RadialBarChart, RadialBar, ResponsiveContainer, Tooltip } from 'recharts'

export function CampaignAnalyticsPage(): JSX.Element {
  const { id } = useParams<{ id: string }>()
  const { data: campaignData } = useCampaign(id ?? '')
  const { data: metricsData, isLoading } = useCampaignMetrics(id ?? '')

  const campaign = campaignData?.data
  const metrics = metricsData?.data

  if (isLoading) return <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>

  const rateData = metrics ? [
    { name: 'Open Rate', value: metrics.openRate, fill: '#507d2a' },
    { name: 'Click Rate', value: metrics.clickRate, fill: '#82ca9d' },
    { name: 'Conversion', value: metrics.conversionRate, fill: '#ffc658' },
  ] : []

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">{campaign?.name} — Analytics</h2>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Sent', value: metrics?.sent ?? 0 },
          { label: 'Opens', value: metrics?.opens ?? 0 },
          { label: 'Clicks', value: metrics?.clicks ?? 0 },
          { label: 'Conversions', value: metrics?.conversions ?? 0 },
        ].map(({ label, value }) => (
          <div key={label} className="stat bg-base-100 border border-base-300 rounded-box p-3">
            <div className="stat-title text-xs">{label}</div>
            <div className="stat-value text-xl">{value.toLocaleString('en-IN')}</div>
          </div>
        ))}
      </div>

      <div className="card bg-base-100 border border-base-300 p-4">
        <h3 className="font-semibold mb-4">Engagement Rates (%)</h3>
        <div className="flex gap-6 flex-wrap">
          {[
            { label: 'Open Rate', value: metrics?.openRate ?? 0, color: 'text-success' },
            { label: 'Click Rate', value: metrics?.clickRate ?? 0, color: 'text-info' },
            { label: 'Conversion', value: metrics?.conversionRate ?? 0, color: 'text-warning' },
          ].map(({ label, value, color }) => (
            <div key={label} className="text-center">
              <div className={`text-3xl font-bold ${color}`}>{value}%</div>
              <div className="text-xs text-base-content/60 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
