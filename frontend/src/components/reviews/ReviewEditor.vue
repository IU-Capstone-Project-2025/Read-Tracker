<template>
  <div class="review-editor">
    <h3 v-if="existingReview">Edit Review</h3>
    <h3 v-else>Write a Review</h3>
    
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
    
    <textarea v-model="reviewContent" placeholder="Write your review..." rows="4"></textarea>
    
    <div class="visibility">
      <label>
        <input type="checkbox" v-model="isPublic"> 
        Make this review public
      </label>
    </div>
    
    <div class="actions">
      <button @click="saveReview" class="save-btn">Save Review</button>
      <button v-if="existingReview" @click="cancel" class="cancel-btn">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createReview, updateReview } from '@/api/reviews.js'

const props = defineProps({
  bookId: {
    type: [String, Number],
    required: true
  },
  existingReview: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['review-saved', 'cancel-edit'])

const rating = ref(0)
const reviewContent = ref('')
const isPublic = ref(false)

onMounted(() => {
  if (props.existingReview) {
    rating.value = props.existingReview.rate
    reviewContent.value = props.existingReview.text
    isPublic.value = props.existingReview.isPublic ?? true
  }
})

const saveReview = async () => {
  if (rating.value < 0 || rating.value > 10 || !reviewContent.value.trim()) {
    alert('Please enter valid rating and text.')
    return
  }

  const payload = {
    rate: parseInt(rating.value),
    text: reviewContent.value.trim(),
    isPublic: isPublic.value
  }

  try {
    if (props.existingReview) {
      await updateReview(props.bookId, payload)
    } else {
      await createReview(props.bookId, payload)
    }

    emit('review-saved') 
  } catch (error) {
    console.error('Review save failed:', error)
    alert('Failed to save review. Please try again.')
  }
}


const cancel = () => {
  emit('cancel-edit')
}
</script>

<style scoped>
.review-editor {
  background: #f8f9ff;
  padding: 15px;
  border-radius: 8px;
}

h3 {
  color: #764ba2;
  margin-bottom: 15px;
  font-size: 18px;
}

.rating {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
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
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 12px;
  resize: vertical;
  min-height: 100px;
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

.actions {
  display: flex;
  gap: 10px;
}

.save-btn {
  background: #764ba2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
  flex: 1;
}

.save-btn:hover {
  background: #667eea;
}

.cancel-btn {
  background: #e0e0e0;
  color: #333;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
  flex: 1;
}

.cancel-btn:hover {
  background: #d0d0d0;
}
</style>