<template>
  <div class="subscriptions-page">
    <h1>My Subscriptions</h1>
    
    <div v-if="loading" class="loading">
      <p>Loading subscriptions...</p>
    </div>
    
    <div v-else>
      <div v-if="enrichedSubscriptions.length" class="subscriptions-list">
        <div v-for="subscription in enrichedSubscriptions" :key="subscription.id" class="subscription-card">
          <div class="user-info">
            <div class="avatar">
              <i class="fas fa-user"></i>
            </div>
            <div>
              <h3 class="username">{{ subscription.username }}</h3>
              <p class="email">{{ subscription.email }}</p>
            </div>
          </div>
          <button 
            @click="unsubscribe(subscription.publisher_id)" 
            class="unsubscribe-btn"
            :disabled="unsubscribing === subscription.publisher_id"
          >
            Unsubscribe
            <span v-if="unsubscribing === subscription.publisher_id" class="spinner"></span>
          </button>
        </div>
      </div>
      
      <div v-else class="no-subscriptions">
        <p>You haven't subscribed to anyone yet.</p>
        <p>Discover users to follow on the Community Reviews page!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useSubscriptionsStore } from '@/store/subscriptions'
import { useAuthStore } from '@/store/auth'
import { useUsersStore } from '@/store/users'

const authStore = useAuthStore()
const subscriptionsStore = useSubscriptionsStore()
const usersStore = useUsersStore()

const loading = ref(true)
const unsubscribing = ref(null)
const enrichedSubscriptions = ref([])

watch(() => subscriptionsStore.subscriptions, async (newSubscriptions) => {
  if (!newSubscriptions.length) {
    enrichedSubscriptions.value = []
    return
  }
  
  const enriched = []
  for (const sub of newSubscriptions) {
    try {
      const userProfile = await usersStore.fetchUserProfile(sub.publisher_id)
      enriched.push({
        ...sub,
        username: userProfile?.username || 'Unknown User',
        email: userProfile?.email || 'unknown@example.com'
      })
    } catch (e) {
      console.error('Failed to load user profile:', e)
      enriched.push({
        ...sub,
        username: 'Unknown User',
        email: 'unknown@example.com'
      })
    }
  }
  
  enrichedSubscriptions.value = enriched
}, { immediate: true })

onMounted(async () => {
  try {
    await subscriptionsStore.fetchSubscriptions(authStore.user.id)
  } catch (e) {
    console.error('Failed to load subscriptions:', e)
  } finally {
    loading.value = false
  }
})

const unsubscribe = async (publisherId) => {
  unsubscribing.value = publisherId
  try {
    await subscriptionsStore.unsubscribe(publisherId)
  } catch (e) {
    console.error('Unsubscribe failed:', e)
  } finally {
    unsubscribing.value = null
  }
}
</script>

<style scoped>
.subscriptions-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #764ba2;
  margin-bottom: 20px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.subscriptions-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.subscription-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.subscription-card:last-child {
  border-bottom: none;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #764ba2;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.username {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.email {
  margin: 3px 0 0;
  font-size: 14px;
  color: #888;
}

.unsubscribe-btn {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.unsubscribe-btn:hover {
  background: #c0392b;
}

.unsubscribe-btn:disabled {
  background: #e67e7e;
  cursor: not-allowed;
}

.no-subscriptions {
  background: white;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  padding: 30px;
  text-align: center;
  color: #666;
}

.no-subscriptions p {
  margin: 5px 0;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>