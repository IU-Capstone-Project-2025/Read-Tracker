<template>
  <div class="review-display">
    <div class="review-header">
      <div class="rating">
        Rating: <span class="rating-value">{{ review.rate }}/10</span>
      </div>
      <div class="visibility-tag" :class="{ 'public': review.isPublic, 'private': !review.isPublic }">
        {{ review.isPublic ? 'Public' : 'Private' }}
      </div>
    </div>
    
    <div class="review-content">{{ review.text }}</div>
    
    <div class="review-footer">
      <span class="review-date">{{ formatDate(review.created_at) }}</span>
      <div class="actions">
        <button @click="editReview" class="edit-btn">Edit</button>
        <button @click="deleteReview" class="delete-btn">Delete</button>
      </div>
    </div>
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

const emit = defineEmits(['edit-review', 'delete-review'])

const editReview = () => {
  emit('edit-review', props.review)
}

const deleteReview = () => {
  if (confirm('Are you sure you want to delete this review?')) {
    emit('delete-review', props.review)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}
</script>

<style scoped>
.review-display {
  background: #f8f9ff;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #764ba2;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.rating-value {
  font-weight: bold;
  font-size: 18px;
  color: #764ba2;
}

.visibility-tag {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 500;
}

.public {
  background-color: rgba(46, 204, 113, 0.2);
  color: #27ae60;
}

.private {
  background-color: rgba(52, 152, 219, 0.2);
  color: #2980b9;
}

.review-content {
  line-height: 1.6;
  margin-bottom: 15px;
  white-space: pre-line;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #666;
}

.actions button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13px;
  padding: 5px 10px;
  border-radius: 4px;
  margin-left: 8px;
}

.edit-btn {
  color: #3498db;
}

.edit-btn:hover {
  background: rgba(52, 152, 219, 0.1);
}

.delete-btn {
  color: #e74c3c;
}

.delete-btn:hover {
  background: rgba(231, 76, 60, 0.1);
}
</style>