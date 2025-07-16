<template>
  <div class="subscriptions-page">
    <h1>My Subscriptions</h1>
    
    <div v-if="loading" class="loading">
      <p>Loading subscriptions...</p>
    </div>
    
    <div v-else>
      <div v-if="subscriptions.length" class="subscriptions-list">
        <div v-for="subscription in subscriptions" :key="subscription.id" class="subscription-card">
          <div class="user-info">
            <img 
              :src="subscription.publisher.avatar || '/images/avatar-placeholder.png'" 
              :alt="subscription.publisher.username" 
              class="avatar"
            />
            <div>
              <h3 class="username">{{ subscription.publisher.username }}</h3>
              <p class="email">{{ subscription.publisher.email }}</p>
            </div>
          </div>
          <button 
            @click="unsubscribe(subscription.id)" 
            class="unsubscribe-btn"
            :disabled="unsubscribing === subscription.id"
          >
            Unsubscribe
            <span v-if="unsubscribing === subscription.id" class="spinner"></span>
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
import { ref, onMounted } from 'vue'
import { useSubscriptionsStore } from '@/store/subscriptions'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const subscriptionsStore = useSubscriptionsStore()

const loading = ref(true)
const unsubscribing = ref(null)

const subscriptions = computed(() => 
  subscriptionsStore.subscriptions.map(sub => ({
    ...sub,
    publisher: sub.publisher || { username: 'Unknown User', email: 'unknown@example.com' }
  }))
)

onMounted(async () => {
  try {
    await subscriptionsStore.fetchSubscriptions(authStore.user.id)
  } catch (e) {
    console.error('Failed to load subscriptions:', e)
  } finally {
    loading.value = false
  }
})

const unsubscribe = async (subscriptionId) => {
  unsubscribing.value = subscriptionId
  try {
    await subscriptionsStore.unsubscribe(subscriptionId)
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
  object-fit: cover;
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