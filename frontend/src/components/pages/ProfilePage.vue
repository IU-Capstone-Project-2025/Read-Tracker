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
        <h2 class="profile-name"> {{ authStore.user.username }} </h2>
        <p>Member since 2020</p>

        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-value"> {{ booksStore.books.length || 0 }} </span>
            <span class="stat-label">Books Read</span>
          </div>
          <div class="stat-item">
            <span class="stat-value"> {{ reviewsStore.reviews.length || 0 }} </span>
            <span class="stat-label">Reviews</span>
          </div>
          <div class="stat-item">
            <span class="stat-value"> {{ collectionsStore.collections.length || 0 }} </span>
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useBooksStore } from '@/store/books'
import { useReviewsStore } from '@/store/reviews'
import { useCollectionsStore } from '@/store/collections'
import { apiLoadStreaks, apiCheckIn } from '@/api/streaks'

const authStore = useAuthStore()
const booksStore = useBooksStore()
const reviewsStore = useReviewsStore()
const collectionsStore = useCollectionsStore()

const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const months = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

const currentDate = new Date()
const currentMonth = ref(currentDate.getMonth())
const currentYear = ref(currentDate.getFullYear())

const readingData = ref({})
const currentStreak = ref(0)
const todayMarked = ref(false)

const loadStreaks = async () => {
  try {
    const res = await apiLoadStreaks(authStore.user.id)
    const streaks = res.data?.data

    if (Array.isArray(streaks)) {
      readingData.value = {}

      let maxStreak = 0

      streaks.forEach((item) => {
        const start = new Date(item.start_date)
        const end = item.end_date ? new Date(item.end_date) : new Date()
        
        let date = new Date(start)
        while (date <= end) {
          const dateStr = date.toISOString().split('T')[0]
          readingData.value[dateStr] = true
          date.setDate(date.getDate() + 1)
        }
        
        const streakLength = calculateStreakLength(item.start_date, item.end_date)
        if (streakLength > maxStreak) {
          maxStreak = streakLength
        }
      })

      currentStreak.value = maxStreak
      const today = new Date().toISOString().split('T')[0]
      todayMarked.value = !!readingData.value[today]
    } else {
      console.error('Invalid streaks format', res.data)
    }
  } catch (e) {
    console.error('Failed to load streaks', e)
  }
}

const markAsRead = async () => {
  if (!todayMarked.value) {
    try {
      const today = new Date().toISOString().split('T')[0]
      await apiCheckIn(authStore.user.id)
      readingData.value[today] = true
      currentStreak.value++
      todayMarked.value = true
    } catch (error) {
      console.error('Failed to mark today as read', error)
    }
  }
}

const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)

  for (let i = 0; i < firstDay.getDay(); i++) {
    days.push({ day: '', date: '' })
  }

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

const calculateStreakLength = (startDate, endDate = null) => {
  const start = new Date(startDate)
  const end = endDate ? new Date(endDate) : new Date()
  const diffTime = end - start
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 ? diffDays : 0
}


onMounted(() => {
  console.log(authStore.user)
  loadStreaks()
})
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
