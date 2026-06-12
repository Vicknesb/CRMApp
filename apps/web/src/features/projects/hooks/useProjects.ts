import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { projectsApi } from '../api/projectsApi'

export const useProjects = (params?: { status?: string }) =>
  useQuery({ queryKey: ['projects', params], queryFn: () => projectsApi.list(params) })

export const useProject = (id: string) =>
  useQuery({ queryKey: ['projects', id], queryFn: () => projectsApi.get(id), enabled: !!id })

export const useCreateProject = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: projectsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['projects'] }),
  })
}

export const useUpdateProject = (id: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: Parameters<typeof projectsApi.update>[1]) => projectsApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['projects'] }),
  })
}

export const useProjectMilestones = (id: string) =>
  useQuery({ queryKey: ['projects', id, 'milestones'], queryFn: () => projectsApi.listMilestones(id), enabled: !!id })

export const useProjectTasks = (id: string) =>
  useQuery({ queryKey: ['projects', id, 'tasks'], queryFn: () => projectsApi.listTasks(id), enabled: !!id })

export const useCreateProjectTask = (projectId: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: Parameters<typeof projectsApi.createTask>[1]) =>
      projectsApi.createTask(projectId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['projects', projectId, 'tasks'] }),
  })
}
