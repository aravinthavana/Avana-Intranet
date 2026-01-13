<template>
  <div>
    <h1>Events & Parties</h1>
    <div class="card" v-for="event in store.events" :key="event.id">
       <h2>🎉 {{ event.name }}</h2>
       <p><strong>Date:</strong> {{ event.date }} at {{ event.time }}</p>
       <p><strong>Location:</strong> {{ event.location }}</p>
    </div>
    <div v-if="store.events.length === 0">No upcoming events.</div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

onMounted(() => {
   if (store.events.length === 0) store.fetchAll()
})
</script>
