<template>
  <div class="review-card">
    <div class="review-header">
      <img 
        :src="review.user.avatar || '/images/avatar-placeholder.png'" 
        :alt="review.user.username" 
        class="avatar"
      />
      <div class="user-info">
        <div class="username-container">
          <h3 class="username">{{ review.user.username }}</h3>
          <button 
            v-if="showSubscribeButton"
            @click="toggleSubscription"
            class="subscribe-btn"
            :disabled="subscriptionLoading"
          >
            {{ isSubscribed ? 'Unsubscribe' : 'Subscribe' }}
            <span v-if="subscriptionLoading" class="spinner"></span>
          </button>
        </div>
        <div class="rating">
          <span v-for="star in 10" :key="star">
            <i :class="['star', star <= review.rate ? 'filled' : '']">★</i>
          </span>
        </div>
      </div>
    </div>
    <p class="review-text">{{ review.text }}</p>
    <p class="review-date">{{ formatDate(review.created_at) }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useSubscriptionsStore } from '@/store/subscriptions'

const props = defineProps({
  review: {
    type: Object,
    required: true
  }
})

const authStore = useAuthStore()
const subscriptionsStore = useSubscriptionsStore()
const subscriptionLoading = ref(false)

const currentUserId = computed(() => authStore.user?.id)
const showSubscribeButton = computed(() => 
  currentUserId.value && props.review.user.id !== currentUserId.value
)

const isSubscribed = computed(() => {
  if (!currentUserId.value) return false
  return subscriptionsStore.isSubscribedTo(props.review.user.id)
})

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const toggleSubscription = async () => {
  if (!currentUserId.value) return
  
  subscriptionLoading.value = true
  try {
    if (isSubscribed.value) {
      const subscriptionId = subscriptionsStore.getSubscriptionId(props.review.user.id)
      if (subscriptionId) {
        await subscriptionsStore.unsubscribe(subscriptionId)
      }
    } else {
      await subscriptionsStore.subscribe(props.review.user.id, currentUserId.value)
    }
  } catch (e) {
    console.error('Subscription toggle failed:', e)
  } finally {
    subscriptionLoading.value = false
  }
}
</script>

<style scoped>
.review-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
}

.review-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.username-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.username {
  margin: 0;
  font-size: 16px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.subscribe-btn {
  background: #764ba2;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s;
  margin-left: 10px;
  flex-shrink: 0;
  white-space: nowrap;
}

.subscribe-btn:hover {
  background: #5a3d80;
}

.subscribe-btn:disabled {
  background: #b39ddb;
  cursor: not-allowed;
}

.rating {
  display: flex;
  margin-top: 4px;
}

.star {
  color: #ddd;
  font-style: normal;
}

.star.filled {
  color: #ffc107;
}

.review-text {
  margin: 10px 0;
  font-size: 14px;
  line-height: 1.5;
  color: #444;
}

.review-date {
  font-size: 12px;
  color: #888;
  text-align: right;
}

.spinner {
  display: inline-block;
  width: 10px;
  height: 10px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-left: 5px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>