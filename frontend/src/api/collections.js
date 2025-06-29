import axios from 'axios'

export async function fetchCollections() {
  try {
    const response = await axios.get('http://localhost:8000/collections')
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to fetch collections')
    }
  } catch (error) {
    console.error('Axios error:', error)
    return []
  }
}

export async function createCollection(collectionData) {
  try {
    const response = await axios.post('http://localhost:8000/collections', collectionData)
    return response.data
  } catch (error) {
    console.error('Error creating collection:', error)
    throw error
  }
}

export async function fetchCollection(collectionId) {
  try {
    const response = await axios.get(`http://localhost:8000/collections/${collectionId}`)
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to fetch collection')
    }
  } catch (error) {
    console.error('Axios error:', error)
    throw error
  }
}