<template>
  <div class="review-editor">
    <div class="rating">
      <span>Rating (0-10):</span>
      <input 
        type="number" 
        v-model="rating" 
        min="0" 
        max="10" 
        step="1"
        class="rating-input"
      >
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

const saveReview = () => {
  if (rating.value >= 0 && rating.value <= 10 && reviewContent.value.trim()) {
    const newReview = {
      id: Date.now(),
      rating: parseInt(rating.value),
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

.rating-input {
  margin-left: 10px;
  width: 60px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
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