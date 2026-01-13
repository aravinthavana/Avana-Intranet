<template>
  <div>
    <h1>Conference Hall Bookings</h1>
    <div class="card">
       <table style="width:100%; text-align:left;">
         <thead>
           <tr>
             <th>Hall</th>
             <th>Date</th>
             <th>Time</th>
             <th>Booked By</th>
           </tr>
         </thead>
         <tbody>
           <tr v-for="b in store.bookings" :key="b.id">
             <td>{{ b.hall }}</td>
             <td>{{ b.date }}</td>
             <td>{{ b.start_time }} - {{ b.end_time }}</td>
             <td>{{ b.booked_by }}</td>
           </tr>
         </tbody>
       </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()
onMounted(() => {
  if (store.bookings.length === 0) store.fetchAll()
})
</script>
