<template>
  <div class="profile-container">
    <div class="page-header">
      <h1 class="page-title">My Profile</h1>
      <p class="page-subtitle">Manage your account</p>
    </div>

    <div class="profile-header">
      <div class="avatar">
        <i class="fas fa-user"></i>
      </div>
      <div class="profile-info">
        <h2 class="profile-name">Alex Johnson</h2>
        <p>125 books read • Member since 2020</p>

        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-value">86</span>
            <span class="stat-label">Books Read</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">42</span>
            <span class="stat-label">Reviews</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">7</span>
            <span class="stat-label">Collections</span>
          </div>
        </div>
      </div>
    </div>

    <div class="calendar-section">
      <div class="calendar-header">
        <h3 class="calendar-title">Reading Calendar - {{ currentMonth }} {{ currentYear }}</h3>
        <div class="month-navigation">
          <button class="nav-button" @click="prevMonth">
            <i class="fas fa-chevron-left"></i>
          </button>
          <button class="nav-button" @click="nextMonth">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>

      <div class="calendar-grid">
        <div class="calendar-day-header" v-for="day in weekDays" :key="day">{{ day }}</div>
        <div 
          v-for="day in calendarDays" 
          :key="day.date"
          class="calendar-day"
          :class="{
            active: isToday(day.date),
            'has-data': readingData[day.date]
          }"
        >
          {{ day.day }}
        </div>
      </div>
    </div>

    <div class="streak-container">
      <div class="streak-count">
        {{ currentStreak }} days in a row
        <span>Your reading streak</span>
      </div>
      <button
        class="mark-read-button"
        @click="markAsRead"
        :disabled="todayMarked"
      >
        <i class="fas fa-check"></i> I have read today
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentDate = new Date()
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const months = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

const currentMonth = ref(currentDate.getMonth())
const currentYear = ref(currentDate.getFullYear())

const readingData = ref({
  '2025-06-03': true,
  '2025-06-05': true,
  '2025-06-07': true,
  '2025-06-10': true,
  '2025-06-12': true,
  '2025-06-15': true,
  '2025-06-17': true,
  '2025-06-20': true,
  '2025-06-22': true,
  '2025-06-25': true,
  '2025-06-28': true
})

const currentStreak = ref(12)
const todayMarked = ref(false)

const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  
  // Add empty days for the first week
  for (let i = 0; i < firstDay.getDay(); i++) {
    days.push({ day: '', date: '' })
  }
  
  // Add actual days of the month
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(currentYear.value, currentMonth.value, i)
    days.push({ 
      day: i, 
      date: date.toISOString().split('T')[0]
    })
  }
  
  return days
})

const isToday = (dateString) => {
  const today = new Date().toISOString().split('T')[0]
  return dateString === today
}

const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

const markAsRead = () => {
  if (!todayMarked.value) {
    const today = new Date().toISOString().split('T')[0]
    readingData.value[today] = true
    currentStreak.value++
    todayMarked.value = true
  }
}
</script>

<style scoped>
.calendar-day.has-data {
  background: #764ba2;
  color: white;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #f8f9ff;
  font-weight: 500;
  position: relative;
  font-size: 14px;
}

.calendar-day.active {
  background: #667eea;
  color: white;
  font-weight: bold;
}

@media (max-width: 768px) {
  .calendar-day {
    font-size: 12px;
  }
}
</style>