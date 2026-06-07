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
  parse: (jdText: string) => api.post('/api/jd/parse', { jd_content: jdText, position_type: 'dev' }),

  analyze: (jdText: string, resumeText: string) =>
    api.post('/api/resume/analyze', { resume_content: resumeText, jd_content: jdText })
}

export const resumeApi = {
  parse: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return instance.post('/api/resume/parse', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  analyze: (resumeContent: string, jdId?: string, jdContent?: string) =>
    api.post('/api/resume/analyze', { resume_content: resumeContent, jd_id: jdId, jd_content: jdContent }),

  optimize: (resumeContent: string, jdId: string, positionType: string = 'dev') =>
    api.post('/api/resume/optimize', { resume_content: resumeContent, jd_id: jdId, position_type: positionType })
}

export const interviewApi = {
  start: (jdId: string = '', questionCount: number = 5, difficultyRatio: string = 'balanced') =>
    api.post('/api/interview/start', { jd_id: jdId, question_count: questionCount, difficulty_ratio: difficultyRatio }),

  chat: (sessionId: string, message: string, context?: object) =>
    api.post('/api/interview/chat', { session_id: sessionId, message, context }),

  answer: (sessionId: string, questionId: string, answer: string) =>
    api.post('/api/interview/answer', { session_id: sessionId, question_id: questionId, answer }),

  studyNotes: (sessionId: string) =>
    api.post('/api/interview/study-notes', { session_id: sessionId }),

  complete: (sessionId: string) =>
    api.post('/api/interview/complete', { session_id: sessionId })
}

export const notesApi = {
  generate: (jdId: string, sessionId?: string, gaps?: string[]) =>
    api.post('/api/note/generate', { jd_id: jdId, session_id: sessionId, gaps }),

  generateFromFavorites: (items: Array<{question: string, answer: string}>) =>
    api.post('/api/note/generate-from-favorites', { items }),

  save: (data: { question: string; answer: string; folderId: string }) =>
    api.post('/api/notes/save', data),

  list: (folderId?: string) => api.get('/api/notes/list', { params: { folderId } })
}

export const archiveApi = {
  list: (jdId?: string) => api.get('/api/archive/list', { params: { jd_id: jdId } }),
  get: (itemId: string) => api.get(`/api/archive/get/${itemId}`),
  delete: (itemId: string) => api.delete(`/api/archive/delete/${itemId}`)
}

export default instance
