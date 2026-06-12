import { useMutation, useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../api/analyticsApi'

export const useDashboard = (role?: string) =>
  useQuery({ queryKey: ['dashboard', role], queryFn: () => analyticsApi.dashboard(role) })

export const useReportList = () =>
  useQuery({ queryKey: ['reports'], queryFn: analyticsApi.listReports })

export const useReport = (key: string) =>
  useQuery({ queryKey: ['reports', key], queryFn: () => analyticsApi.runReport(key), enabled: !!key })

export const useRunCustomReport = () =>
  useMutation({ mutationFn: analyticsApi.runCustom })
