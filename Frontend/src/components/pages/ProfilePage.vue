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
        <h3 class="calendar-title">Reading Calendar - June 2025</h3>
        <div class="month-navigation">
          <button class="nav-button"><i class="fas fa-chevron-left"></i></button>
          <button class="nav-button"><i class="fas fa-chevron-right"></i></button>
        </div>
      </div>

      <div class="calendar-grid">
        <div class="calendar-day-header" v-for="day in weekDays" :key="day">{{ day }}</div>

        <div
          class="calendar-day"
          v-for="day in calendarDays"
          :key="day"
          :class="{
            active: day === currentDate,
            'has-data': readingData[day]
          }"
        >
          {{ day }}
          <span v-if="readingData[day]" class="reading-count">
            {{ readingData[day] }} min
          </span>
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
import { ref } from 'vue'

const currentDate = new Date().getDate()
const calendarDays = Array.from({ length: 30 }, (_, i) => i + 1)
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const readingData = ref({
  3: 45,
  5: 60,
  7: 30,
  10: 90,
  12: 120,
  15: 45,
  17: 60,
  20: 75,
  22: 90,
  25: 60,
  28: 120
})

const currentStreak = ref(12)
const todayMarked = ref(false)

const markAsRead = () => {
  if (!todayMarked.value) {
    const today = new Date().getDate()
    readingData.value[today] = 30
    currentStreak.value++
    todayMarked.value = true
  }
}
</script>
