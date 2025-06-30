import axios from 'axios'

export async function fetchBooks() {
  try {
    const response = await axios.get('http://localhost:8000/books/')
    if (response.data.status === 'success') {
      return response.data.data.map(book => ({
        id: book.id,
        title: book.title,
        author: book.author,
        language: book.language,
        description: book.description,
        cover: book.cover || null
      }))
    } else {
      throw new Error(response.data.message || 'Failed to fetch books')
    }
  } catch (error) {
    console.error('Axios error:', error)
    return []
  }
}