import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface JDContent {
  text: string
  fileName: string
  uploadedAt: number
}

export interface ResumeContent {
  text: string
  fileName: string
  uploadedAt: number
}

export interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  timestamp: number
}

export interface FavoriteItem {
  id: string
  question: string
  answer: string
  folderId: string
  createdAt: number
}

export interface Folder {
  id: string
  name: string
  createdAt: number
}

export const useAppStore = defineStore('app', () => {
  const jdContent = ref<JDContent | null>(null)
  const resumeContent = ref<ResumeContent | null>(null)
  const messages = ref<Message[]>([])
  const folders = ref<Folder[]>([])
  const favorites = ref<FavoriteItem[]>([])

  const hasJDContent = computed(() => !!jdContent.value?.text)
  const hasResumeContent = computed(() => !!resumeContent.value?.text)
  const messageCount = computed(() => messages.value.length)

  const setJDContent = (content: JDContent) => {
    jdContent.value = content
    localStorage.setItem('jdContent', JSON.stringify(content))
  }

  const setResumeContent = (content: ResumeContent) => {
    resumeContent.value = content
    localStorage.setItem('resumeContent', JSON.stringify(content))
  }

  const addMessage = (role: 'user' | 'ai', content: string) => {
    const message: Message = {
      id: Date.now().toString(),
      role,
      content,
      timestamp: Date.now()
    }
    messages.value.push(message)
    saveMessages()
  }

  const clearMessages = () => {
    messages.value = []
    localStorage.removeItem('messages')
  }

  const saveMessages = () => {
    localStorage.setItem('messages', JSON.stringify(messages.value))
  }

  const addFolder = (name: string) => {
    const folder: Folder = {
      id: Date.now().toString(),
      name,
      createdAt: Date.now()
    }
    folders.value.push(folder)
    saveFolders()
    return folder
  }

  const deleteFolder = (id: string) => {
    folders.value = folders.value.filter(f => f.id !== id)
    favorites.value = favorites.value.filter(f => f.folderId !== id)
    saveFolders()
    saveFavorites()
  }

  const saveFolders = () => {
    localStorage.setItem('folders', JSON.stringify(folders.value))
  }

  const addFavorite = (question: string, answer: string, folderId: string) => {
    const item: FavoriteItem = {
      id: Date.now().toString(),
      question,
      answer,
      folderId,
      createdAt: Date.now()
    }
    favorites.value.push(item)
    saveFavorites()
    return item
  }

  const deleteFavorite = (id: string) => {
    favorites.value = favorites.value.filter(f => f.id !== id)
    saveFavorites()
  }

  const saveFavorites = () => {
    localStorage.setItem('favorites', JSON.stringify(favorites.value))
  }

  const loadFromStorage = () => {
    const storedJD = localStorage.getItem('jdContent')
    if (storedJD) jdContent.value = JSON.parse(storedJD)

    const storedResume = localStorage.getItem('resumeContent')
    if (storedResume) resumeContent.value = JSON.parse(storedResume)

    const storedMessages = localStorage.getItem('messages')
    if (storedMessages) messages.value = JSON.parse(storedMessages)

    const storedFolders = localStorage.getItem('folders')
    if (storedFolders) folders.value = JSON.parse(storedFolders)

    const storedFavorites = localStorage.getItem('favorites')
    if (storedFavorites) favorites.value = JSON.parse(storedFavorites)
  }

  return {
    jdContent,
    resumeContent,
    messages,
    folders,
    favorites,
    hasJDContent,
    hasResumeContent,
    messageCount,
    setJDContent,
    setResumeContent,
    addMessage,
    clearMessages,
    addFolder,
    deleteFolder,
    addFavorite,
    deleteFavorite,
    loadFromStorage
  }
})
