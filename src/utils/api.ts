import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'

const instance: AxiosInstance = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

instance.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export const api = {
  get: <T = unknown>(url: string, config?: AxiosRequestConfig) =>
    instance.get<T>(url, config),

  post: <T = unknown>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    instance.post<T>(url, data, config),

  put: <T = unknown>(url: string, data?: unknown, config?: AxiosRequestConfig) =>
    instance.put<T>(url, data, config),

  delete: <T = unknown>(url: string, config?: AxiosRequestConfig) =>
    instance.delete<T>(url, config)
}

export const jdApi = {
  parse: (jdText: string) => api.post('/jd/parse', { text: jdText }),

  analyze: (jdText: string, resumeText: string) =>
    api.post('/jd/analyze', { jd: jdText, resume: resumeText })
}

export const resumeApi = {
  parse: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return instance.post('/resume/parse', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export const interviewApi = {
  start: (jdText: string) => api.post('/interview/start', { jd: jdText }),

  chat: (sessionId: string, message: string) =>
    api.post('/interview/chat', { sessionId, message })
}

export const notesApi = {
  save: (data: { question: string; answer: string; folderId: string }) =>
    api.post('/notes/save', data),

  list: (folderId?: string) => api.get('/notes/list', { params: { folderId } })
}

export default instance
