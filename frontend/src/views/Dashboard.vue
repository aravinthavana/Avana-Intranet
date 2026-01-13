<template>
  <div class="dashboard-container">
    <!-- Hero Section for Important Announcements -->
    <section v-if="importantAnnouncements.length > 0" class="hero-section">
      <div v-for="item in importantAnnouncements" :key="item.id" class="announcement-hero">
        <div class="hero-content">
          <span class="badge">📢 Important</span>
          <h2>{{ item.title }}</h2>
          <p>{{ item.description }}</p>
          <div class="meta">Posted on {{ item.date }}</div>
        </div>
      </div>
    </section>

    <div class="dashboard-grid">
      <!-- Latest News -->
      <div class="card news-card">
        <div class="card-header">
          <h3>Latest News</h3>
        </div>
        <div v-if="store.announcements.length === 0" class="empty-state">No announcements yet.</div>
        <ul v-else class="list-group">
           <li v-for="a in store.announcements.slice(0, 5)" :key="a.id" class="list-item">
             <div class="item-content">
               <span class="item-title">{{ a.title }}</span>
               <span class="item-date">{{ a.date }}</span>
             </div>
           </li>
        </ul>
      </div>

      <!-- Upcoming Events -->
      <div class="card events-card">
        <div class="card-header">
          <h3>Upcoming Events</h3>
          <router-link to="/events" class="view-all">View All</router-link>
        </div>
        <div v-if="store.events.length === 0" class="empty-state">No upcoming events.</div>
        <ul v-else class="event-list">
           <li v-for="e in store.events.slice(0, 3)" :key="e.id" class="event-item">
             <div class="event-date-box">
               <span class="day">{{ new Date(e.date).getDate() }}</span>
               <span class="month">{{ new Date(e.date).toLocaleString('default', { month: 'short' }) }}</span>
             </div>
             <div class="event-details">
               <strong>{{ e.name }}</strong>
               <div class="event-meta">📍 {{ e.location }} • 🕒 {{ e.time }}</div>
             </div>
           </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

onMounted(() => {
  store.fetchAll()
})

const importantAnnouncements = computed(() => {
  return store.announcements.filter(a => a.important)
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  margin-bottom: 2rem;
}

.announcement-hero {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
  color: white;
  padding: 2rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.badge {
  background: rgba(255,255,255,0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: inline-block;
}

.announcement-hero h2 {
  color: white;
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.meta {
  opacity: 0.8;
  font-size: 0.9rem;
  margin-top: 1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.view-all {
  font-size: 0.9rem;
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.list-group {
  list-style: none;
  padding: 0;
  margin: 0;
}

.list-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.list-item:last-child {
  border-bottom: none;
}

.item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-title {
  font-weight: 500;
  color: var(--text-main);
}

.item-date {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* Event Items */
.event-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.event-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-page);
  border-radius: 8px;
  margin-bottom: 0.75rem;
  transition: transform 0.2s;
}

.event-item:hover {
  transform: translateX(5px);
}

.event-date-box {
  background: white;
  border-radius: 8px;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 50px;
  box-shadow: var(--shadow-sm);
  text-align: center;
}

.day {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1;
}

.month {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
}

.event-details strong {
  display: block;
  font-size: 1.05rem;
  margin-bottom: 0.25rem;
  color: var(--text-main);
}

.event-meta {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.empty-state {
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
  padding: 1rem;
  font-size: 0.9rem;
  background: #f8fafc;
  border-radius: 8px;
}
</style>
