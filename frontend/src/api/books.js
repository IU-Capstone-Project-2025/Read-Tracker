import axios from 'axios'

export async function fetchBooks() {
  try {
    const response = await axios.get('http://localhost:8000/books/')
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to fetch books')
    }
  } catch (error) {
    console.error('Axios error:', error)
    return []
  }
}