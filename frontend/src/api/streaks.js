import axios from 'axios'
import config from '@/runtimeConfig'


const api = axios.create({
  baseURL: config.api.baseUrl
})


export async function apiLoadStreaks(userId) {
    const response = await api.post('me/streaks', {
      user_id: userId
    })
    if (response.data.status === 'success') {
        return response
    }
    throw new Error('Failed to load streaks')
}

export async function apiCheckIn(userId) {
    const today = new Date().toISOString().split('T')[0]
    const response = await api.post('me/streaks', {
      user_id: userId
    })
    if (response.data.status === 'success') {
        return true
    }
    throw new Error('Failed to check in')
}