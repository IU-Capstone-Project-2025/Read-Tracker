import axios from 'axios'
import config from '@/runtimeConfig'


const api = axios.create({
  baseURL: config.api.baseUrl
})


export const getNotes = async (userId, bookId) => {
  try {
    const response = await api.post(`me/books/${bookId}/notes`, {
      user_id: userId
    })
    return response.data
  } catch (error) {
    console.error('Failed to fetch all notes:', error)
    throw error
  }
}

export const createNote = async (userId, bookId, text) => {
  try {
    const response = await api.put(`me/books/${bookId}/notes`, {
      user_id: userId,
      text: text
    })
    return response.data
  } catch (error) {
    console.error(`Failed to create note for book ${bookId}:`, error)
    throw error
  }
}

export const deleteNote = async (userId, noteId) => {
  try {
    const response = await api.delete(`me/notes/${noteId}`, {
      data: {
        user_id: userId
      }
    })
    return response.data
  } catch (error) {
    console.error(`Failed to delete note:`, error)
    throw error
  }
}

export const updateNote = async (userId, noteId, text) => {
  try {
    const response = await api.put(`me/notes/${noteId}`, {
      user_id: userId,
      text: text
    })
    return response.data
  } catch (error) {
    console.error(`Failed to update note:`, error)
    throw error
  }
}