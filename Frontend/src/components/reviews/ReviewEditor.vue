<template>
  <div class="review-editor">
    <div class="rating">
      <span>Rating:</span>
      <div class="stars">
        <span 
          v-for="star in 5" 
          :key="star" 
          @click="setRating(star)"
          :class="{ 'active': star <= rating }"
        >★</span>
      </div>
    </div>
    
    <textarea v-model="reviewContent" placeholder="Write your review..." rows="6"></textarea>
    
    <div class="visibility">
      <label>
        <input type="checkbox" v-model="isPublic"> 
        Make this review public
      </label>
    </div>
    
    <button @click="saveReview" class="save-btn">Save Review</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  bookId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['review-saved'])

const rating = ref(0)
const reviewContent = ref('')
const isPublic = ref(false)

const setRating = (stars) => {
  rating.value = stars
}

const saveReview = () => {
  if (rating.value > 0 && reviewContent.value.trim()) {
    const newReview = {
      id: Date.now(),
      rating: rating.value,
      content: reviewContent.value,
      isPublic: isPublic.value,
      createdAt: new Date().toISOString()
    }
    emit('review-saved', newReview)
  }
}
</script>

<style scoped>
.review-editor {
  background: #f8f9ff;
  padding: 20px;
  border-radius: 10px;
}

.rating {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-weight: 500;
  color: #333;
}

.stars {
  margin-left: 10px;
  cursor: pointer;
}

.stars span {
  font-size: 24px;
  color: #ddd;
  transition: color 0.2s;
}

.stars span.active {
  color: #f39c12;
}

textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 15px;
  resize: vertical;
  min-height: 120px;
}

.visibility {
  margin-bottom: 15px;
  font-size: 14px;
}

.visibility label {
  display: flex;
  align-items: center;
}

.visibility input {
  margin-right: 8px;
}

.save-btn {
  background: #764ba2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
}

.save-btn:hover {
  background: #667eea;
}
</style>