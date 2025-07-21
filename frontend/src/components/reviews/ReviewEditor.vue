<template>
  <div class="review-editor">
    <h3 v-if="existingReview">Edit Review</h3>
    <h3 v-else>Write a Review</h3>
    
    <div class="rating">
      <span>Rating (1-10):</span>
      <input 
        type="number" 
        v-model.number="rating" 
        min="1" 
        max="10" 
        step="1"
        class="rating-input"
      >
    </div>
    
    <textarea v-model="reviewContent" placeholder="Write your review..." rows="4"></textarea>
    
    <div class="actions">
      <button @click="saveReview" class="save-btn">Save Review</button>
      <button v-if="existingReview" @click="cancel" class="cancel-btn">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  bookId: {
    type: String,
    required: true
  },
  existingReview: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['review-saved', 'cancel-edit'])

const rating = ref(1)
const reviewContent = ref('')
const isPublic = ref(true)

onMounted(() => {
  if (props.existingReview) {
    rating.value = props.existingReview.rate || 1
    reviewContent.value = props.existingReview.text || ''
    isPublic.value = props.existingReview.isPublic ?? true
  }
})

watch(() => props.existingReview, (newReview) => {
  if (newReview) {
    rating.value = newReview.rate || 1
    reviewContent.value = newReview.text || ''
    isPublic.value = newReview.isPublic ?? true
  } else {
    rating.value = 1
    reviewContent.value = ''
    isPublic.value = true
  }
})

const saveReview = () => {
  if (rating.value < 1 || rating.value > 10 || !reviewContent.value.trim()) {
    alert('Please enter a valid rating between 1 and 10 and some review text.')
    return
  }

  const payload = {
    rate: rating.value,
    text: reviewContent.value.trim(),
    isPublic: isPublic.value
  }

  emit('review-saved', payload)
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