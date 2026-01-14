<template>
  <div class="max-w-7xl mx-auto">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-neutral-900">Events & Parties</h1>
      <p class="text-neutral-600 mt-2">Upcoming company events and celebrations</p>
    </div>

    <div v-if="store.events.length === 0" class="text-center py-16">
      <svg class="w-20 h-20 mx-auto mb-4 text-neutral-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
      </svg>
      <h3 class="text-lg font-medium text-neutral-900 mb-2">No upcoming events</h3>
      <p class="text-neutral-500">Check back later for new events and parties</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card 
        v-for="event in store.events" 
        :key="event.id"
        hoverable
        class="overflow-hidden"
      >
        <div class="flex items-start gap-4">
          <!-- Date Badge -->
          <div class="flex-shrink-0 bg-primary-100 rounded-lg p-3 text-center min-w-[70px]">
            <div class="text-3xl font-bold text-primary-600 leading-none">
              {{ new Date(event.date).getDate() }}
            </div>
            <div class="text-xs font-semibold text-primary-700 uppercase mt-1">
              {{ new Date(event.date).toLocaleString('default', { month: 'short' }) }}
            </div>
          </div>

          <!-- Event Details -->
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-neutral-900 mb-2 flex items-center gap-2">
              <span>🎉</span>
              <span>{{ event.name }}</span>
            </h3>
            
            <div class="space-y-2 text-sm text-neutral-600">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>{{ event.time }}</span>
              </div>
              
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <span>{{ event.location }}</span>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import Card from '../components/ui/Card.vue'

const store = useDataStore()

onMounted(() => {
   if (store.events.length === 0) store.fetchAll()
})
</script>
