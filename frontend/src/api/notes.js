import axios from 'axios'
import config from '@/runtimeConfig'
import { useAuthStore } from '@/store/auth'

// Create axios instance with base URL
const api = axios.create({
  baseURL: config.api.baseUrl
})

// Add request interceptor to include auth token
api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

export async function saveNoteApi(bookId, noteData) {
  try {
    console.log(`[API] Saving note for book ID: ${bookId}`)
    const response = await api.post(`/me/books/${bookId}/notes`, noteData)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to save your note. Please try again.'
      console.error('[API] saveNoteApi error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Note saved successfully for book ID: ${bookId}`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to save note. Please check your connection and try again.'
    console.error('[API] saveNoteApi exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export async function fetchBookNotes(bookId) {
  try {
    console.log(`[API] Fetching notes for book ID: ${bookId}`)
    const response = await api.get(`/me/books/${bookId}/notes`)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load notes. Please try again.'
      console.error('[API] fetchBookNotes error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Successfully fetched ${response.data.data.length} notes for book ID: ${bookId}`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load notes. Please check your connection and try again.'
    console.error('[API] fetchBookNotes exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export async function deleteNoteApi(noteId) {
  try {
    console.log(`[API] Deleting note ID: ${noteId}`)
    const response = await api.delete(`/me/notes/${noteId}`)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to delete note. Please try again.'
      console.error('[API] deleteNoteApi error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Note deleted successfully: ${noteId}`)
    return true
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to delete note. Please check your connection and try again.'
    console.error('[API] deleteNoteApi exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}