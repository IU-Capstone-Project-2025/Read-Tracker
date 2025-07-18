<template>
  <div class="note-item">
    <div class="note-content">{{ note.text }}</div>
    <div class="note-meta">
      <span class="note-date">{{ formatDate(note.created_at) }}</span>
      <button @click="deleteNote" class="delete-btn">Delete</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  note: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['delete'])

const deleteNote = () => {
  emit('delete', props.note.id)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.note-item {
  background: #f8f9ff;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  border-left: 3px solid #764ba2;
}

.note-content {
  max-width: 1200px;
  overflow-wrap: break-word;
  margin-bottom: 10px;
  line-height: 1.5;
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #666;
}

.delete-btn {
  background: none;
  border: none;
  color: #e74c3c;
  cursor: pointer;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 4px;
}

.delete-btn:hover {
  background: rgba(231, 76, 60, 0.1);
}
</style>