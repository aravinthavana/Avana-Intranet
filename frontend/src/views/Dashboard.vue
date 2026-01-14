<template>
  <div class="max-w-7xl mx-auto">
    <!-- Hero Section for Important Announcements -->
    <section v-if="importantAnnouncements.length > 0" class="mb-8">
      <div 
        v-for="item in importantAnnouncements" 
        :key="item.id" 
        class="bg-gradient-to-r from-warning-400 to-warning-500 text-white p-8 rounded-xl shadow-lg relative overflow-hidden"
      >
        <div class="relative z-10">
          <span class="inline-block bg-white/20 px-3 py-1 rounded-full text-sm font-semibold mb-3">
            📢 Important
          </span>
          <h2 class="text-3xl font-bold mb-2">{{ item.title }}</h2>
          <p class="text-lg opacity-95 mb-4">{{ item.description }}</p>
          <div class="text-sm opacity-80">Posted on {{ item.date }}</div>
        </div>
        <!-- Decorative element -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32"></div>
      </div>
    </section>

    <!-- Dashboard Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Latest News -->
      <Card title="Latest News" hoverable>
        <div v-if="store.announcements.length === 0" class="text-center py-8 text-neutral-500">
          <svg class="w-16 h-16 mx-auto mb-3 text-neutral-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
          </svg>
          <p class="text-sm font-medium">No announcements yet</p>
        </div>
        
        <ul v-else class="space-y-3">
          <li 
            v-for="a in store.announcements.slice(0, 5)" 
            :key="a.id" 
            class="flex justify-between items-center py-3 border-b border-neutral-100 last:border-0 hover:bg-neutral-50 -mx-2 px-2 rounded transition-colors"
          >
            <span class="font-medium text-neutral-800">{{ a.title }}</span>
            <span class="text-sm text-neutral-500 whitespace-nowrap ml-4">{{ a.date }}</span>
          </li>
        </ul>
      </Card>

      <!-- Upcoming Events -->
      <Card hoverable>
        <template #header>
          <div class="flex justify-between items-center w-full">
            <h3 class="text-lg font-semibold text-neutral-900">Upcoming Events</h3>
            <router-link 
              to="/events" 
              class="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors"
            >
              View All →
            </router-link>
          </div>
        </template>

        <div v-if="store.events.length === 0" class="text-center py-8 text-neutral-500">
          <svg class="w-16 h-16 mx-auto mb-3 text-neutral-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <p class="text-sm font-medium">No upcoming events</p>
        </div>

        <ul v-else class="space-y-3">
          <li 
            v-for="e in store.events.slice(0, 3)" 
            :key="e.id" 
            class="flex gap-4 p-4 bg-neutral-50 rounded-lg hover:bg-neutral-100 hover:translate-x-1 transition-all"
          >
            <!-- Date Box -->
            <div class="flex-shrink-0 bg-white rounded-lg p-3 shadow-sm text-center min-w-[60px]">
              <div class="text-2xl font-bold text-primary-600 leading-none">
                {{ new Date(e.date).getDate() }}
              </div>
              <div class="text-xs font-semibold text-neutral-500 uppercase mt-1">
                {{ new Date(e.date).toLocaleString('default', { month: 'short' }) }}
              </div>
            </div>

            <!-- Event Details -->
            <div class="flex-1 min-w-0">
              <h4 class="font-semibold text-neutral-900 mb-1">{{ e.name }}</h4>
              <div class="text-sm text-neutral-600 flex flex-wrap gap-3">
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  {{ e.location }}
                </span>
                <span class="flex items-center gap-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  {{ e.time }}
                </span>
              </div>
            </div>
          </li>
        </ul>
      </Card>
    </div>

    <!-- Quick Stats (Optional Enhancement) -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
      <div class="bg-white p-4 rounded-lg border border-neutral-200 hover:shadow-md transition-shadow">
        <div class="text-2xl font-bold text-primary-600">{{ store.announcements.length }}</div>
        <div class="text-sm text-neutral-600 mt-1">Announcements</div>
      </div>
      
      <div class="bg-white p-4 rounded-lg border border-neutral-200 hover:shadow-md transition-shadow">
        <div class="text-2xl font-bold text-secondary-600">{{ store.events.length }}</div>
        <div class="text-sm text-neutral-600 mt-1">Events</div>
      </div>
      
      <div class="bg-white p-4 rounded-lg border border-neutral-200 hover:shadow-md transition-shadow">
        <div class="text-2xl font-bold text-success-600">{{ store.bookings.length }}</div>
        <div class="text-sm text-neutral-600 mt-1">Bookings</div>
      </div>
      
      <div class="bg-white p-4 rounded-lg border border-neutral-200 hover:shadow-md transition-shadow">
        <div class="text-2xl font-bold text-warning-600">{{ store.intercom.length }}</div>
        <div class="text-sm text-neutral-600 mt-1">Contacts</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useDataStore } from '../stores/data'
import Card from '../components/ui/Card.vue'

const store = useDataStore()

onMounted(() => {
  store.fetchAll()
})

const importantAnnouncements = computed(() => {
  return store.announcements.filter(a => a.important)
})
</script>
