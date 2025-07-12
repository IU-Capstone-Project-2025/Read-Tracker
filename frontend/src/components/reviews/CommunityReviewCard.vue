<template>
  <div class="review-card">
    <div class="review-header">
      <img 
        :src="review.user.avatar || '/images/avatar-placeholder.png'" 
        :alt="review.user.username" 
        class="avatar"
      />
      <div>
        <h3 class="username">{{ review.user.username }}</h3>
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
import { defineProps } from 'vue'

const props = defineProps({
  review: {
    type: Object,
    required: true
  }
})

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
</script>

<style scoped>
.review-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.username {
  margin: 0;
  font-size: 16px;
  color: #333;
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
</style>