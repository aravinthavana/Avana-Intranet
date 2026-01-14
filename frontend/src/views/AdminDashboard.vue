<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Header -->
    <header class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-neutral-900">Admin Dashboard</h1>
        <p class="text-neutral-600 mt-1">Manage your intranet content</p>
      </div>
      <Button variant="outline" @click="$router.push('/')">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
        </svg>
        Exit & View Site
      </Button>
    </header>
    
    <!-- Tabs -->
    <div class="border-b border-neutral-200 mb-6">
      <nav class="-mb-px flex space-x-8">
        <button 
          @click="tab='announcements'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            tab === 'announcements' 
              ? 'border-primary-600 text-primary-600' 
              : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
          ]"
        >
          Announcements
        </button>
        <button 
          @click="tab='intercom'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            tab === 'intercom' 
              ? 'border-primary-600 text-primary-600' 
              : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
          ]"
        >
          Intercom
        </button>
        <button 
          @click="tab='events'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            tab === 'events' 
              ? 'border-primary-600 text-primary-600' 
              : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
          ]"
        >
          Events
        </button>
        <button 
          @click="tab='bookings'"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
            tab === 'bookings' 
              ? 'border-primary-600 text-primary-600' 
              : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300'
          ]"
        >
          Bookings
        </button>
      </nav>
    </div>

    <div class="content">
       <!-- ANNOUNCEMENTS -->
       <div v-if="tab==='announcements'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h3 class="text-xl font-semibold text-neutral-800">Manage Announcements</h3>
          </div>

          <!-- New Announcement Form -->
          <Card title="New Announcement">
            <div class="space-y-4">
              <Input v-model="newAnnouncement.title" label="Title" placeholder="e.g. Office Closure" />
              
              <div class="w-full">
                <label class="block text-sm font-medium text-neutral-700 mb-1.5">Description</label>
                <textarea 
                  v-model="newAnnouncement.description" 
                  rows="3"
                  class="block w-full px-3 py-2 border border-neutral-300 rounded-lg shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors sm:text-sm"
                  placeholder="Enter announcement details..."
                ></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input type="date" v-model="newAnnouncement.date" label="Date" />
                
                <div class="flex items-center h-full pt-6">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" v-model="newAnnouncement.important" class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500" />
                    <span class="text-sm font-medium text-neutral-700">Mark as Important</span>
                  </label>
                </div>
              </div>

              <!-- Email Logic -->
              <div class="bg-primary-50 p-4 rounded-lg border border-primary-100">
                <label class="flex items-center gap-2 mb-2 cursor-pointer">
                  <input type="checkbox" v-model="sendEmail" class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500" />
                  <span class="font-semibold text-primary-900">Send Email Notification</span>
                </label>
                
                <div v-if="sendEmail" class="mt-2">
                   <select 
                    v-model="selectedEmailGroup"
                    class="block w-full px-3 py-2 bg-white border border-neutral-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 sm:text-sm"
                   >
                      <option :value="null">Select Recipient Group...</option>
                      <option v-for="g in store.emailGroups" :key="g.id" :value="g">{{ g.name }}</option>
                   </select>
                </div>
              </div>

              <div class="flex justify-end pt-2">
                <Button @click="addAnnouncement" variant="primary">Publish Announcement</Button>
              </div>
            </div>
          </Card>
          
          <!-- Announcements List -->
          <div class="space-y-4">
            <h4 class="text-lg font-medium text-neutral-700">Recent Announcements</h4>
            <div v-if="store.announcements.length === 0" class="text-neutral-500 italic">No announcements found.</div>
            
            <Card 
              v-for="(item, idx) in store.announcements" 
              :key="idx" 
              class="transition-all hover:shadow-md"
            >
              <div class="flex justify-between items-start gap-4">
                 <div>
                   <div class="flex items-center gap-2 mb-1">
                     <span v-if="item.important" class="px-2 py-0.5 rounded text-xs font-medium bg-warning-100 text-warning-800">Important</span>
                     <h5 class="font-semibold text-neutral-900">{{ item.title }}</h5>
                   </div>
                   <p class="text-sm text-neutral-600 mb-2 line-clamp-2">{{ item.description }}</p>
                   <div class="text-xs text-neutral-500">Posted on {{ item.date }}</div>
                 </div>
                 <Button @click="deleteAnnouncement(idx)" variant="danger" size="sm">Delete</Button>
              </div>
            </Card>
          </div>
       </div>

        <!-- INTERCOM -->
        <div v-if="tab==='intercom'" class="space-y-6">
           <div class="flex justify-between items-center">
             <h3 class="text-xl font-semibold text-neutral-800">Manage Intercom Directory</h3>
           </div>
           
           <!-- Search Bar -->
           <div class="max-w-md">
             <Input v-model="adminSearch" placeholder="Search directory..." />
           </div>

           <!-- Add New Person Form -->
           <Card title="Add New Person">
             <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                <div class="md:col-span-1">
                   <label class="block text-sm font-medium text-neutral-700 mb-1.5">Floor</label>
                   <select 
                    v-model="newPerson.floor" 
                    class="block w-full px-3 py-2 bg-white border border-neutral-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 sm:text-sm"
                   >
                      <option>Ground Floor</option>
                      <option>1st Floor</option>
                      <option>2nd Floor</option>
                      <option>3rd Floor</option>
                   </select>
                </div>
                <div class="md:col-span-1">
                  <Input v-model="newPerson.name" label="Name" placeholder="Full Name" />
                </div>
                <div class="md:col-span-1">
                  <Input v-model="newPerson.department" label="Department" placeholder="Dept." />
                </div>
                <div class="md:col-span-1 flex gap-2">
                  <div class="flex-1">
                    <Input v-model="newPerson.extension" label="Ext" placeholder="123" />
                  </div>
                  <Button @click="addPerson" variant="primary" class="mb-[2px] h-[42px] px-6">Add</Button>
                </div>
             </div>
           </Card>

           <!-- Grouped List View for Admin -->
           <div class="space-y-6">
              <div v-for="(floorData, floorName) in groupedIntercom" :key="floorName" class="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden">
                 <div class="bg-neutral-50 px-6 py-3 border-b border-neutral-200">
                   <h4 class="font-semibold text-neutral-700">{{ floorName }}</h4>
                 </div>
                 <div class="divide-y divide-neutral-100">
                    <div v-for="item in floorData" :key="item.extension" class="p-4 hover:bg-neutral-50 transition-colors">
                       <div class="flex items-start gap-4">
                          <div class="flex-shrink-0 w-16 pt-1">
                            <span class="inline-flex items-center justify-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-primary-100 text-primary-800">
                              {{ item.extension }}
                            </span>
                          </div>
                          <div class="flex-1 space-y-3">
                             <!-- Loop People in this Extension -->
                             <div v-for="(p, idx) in item.people" :key="p.id" class="relative group">
                                
                                <!-- INLINE EDITING MODE -->
                                <div v-if="editingId === p.id" class="bg-neutral-50 p-3 rounded-lg border border-neutral-200 shadow-inner">
                                   <form @submit.prevent="saveEdit" class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
                                      <div class="md:col-span-3">
                                        <Input v-model="editForm.name" placeholder="Name" />
                                      </div>
                                      <div class="md:col-span-3">
                                        <Input v-model="editForm.department" placeholder="Dept" />
                                      </div>
                                      <div class="md:col-span-3">
                                         <select 
                                          v-model="editForm.floor" 
                                          class="block w-full px-3 py-2 bg-white border border-neutral-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 sm:text-sm"
                                         >
                                            <option>Ground Floor</option>
                                            <option>1st Floor</option>
                                            <option>2nd Floor</option>
                                            <option>3rd Floor</option>
                                         </select>
                                      </div>
                                      <div class="md:col-span-2">
                                        <Input v-model="editForm.extension" placeholder="Ext" />
                                      </div>
                                      
                                      <div class="md:col-span-1 flex gap-2 justify-end">
                                        <button type="submit" class="text-primary-600 hover:text-primary-700 p-1" title="Save">
                                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                                        </button>
                                        <button @click="cancelEdit" type="button" class="text-red-500 hover:text-red-700 p-1" title="Cancel">
                                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                                        </button>
                                      </div>
                                   </form>
                                </div>

                                <!-- READ MODE -->
                                <div v-else class="flex justify-between items-center py-1">
                                   <div class="flex items-center gap-2">
                                      <span class="font-medium text-neutral-900">{{ p.name }}</span>
                                      <span class="text-sm text-neutral-500">({{ p.department }})</span>
                                   </div>
                                   <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                      <button @click="startEdit(p)" class="text-neutral-400 hover:text-primary-600 p-1 transition-colors" title="Edit">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                                      </button>
                                      <button @click="deletePerson(p.id)" class="text-neutral-400 hover:text-red-600 p-1 transition-colors" title="Delete">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                                      </button>
                                   </div>
                                </div>

                             </div>
                          </div>
                       </div>
                    </div>
                 </div>
              </div>
           </div>
        </div>
    
       <!-- EVENTS -->
       <div v-if="tab==='events'" class="space-y-6">
          <div class="flex justify-between items-center">
             <h3 class="text-xl font-semibold text-neutral-800">Manage Events</h3>
          </div>

          <!-- Add Event Form -->
          <Card title="Add New Event">
             <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2">
                   <Input v-model="newEvent.name" label="Event Name" placeholder="e.g. Annual Meeting" />
                </div>
                <Input type="date" v-model="newEvent.date" label="Date" />
                <Input type="time" v-model="newEvent.time" label="Time" />
                <div class="md:col-span-2">
                   <Input v-model="newEvent.location" label="Location" placeholder="e.g. Conference Room A" />
                </div>
                <div class="md:col-span-2 flex justify-end mt-2">
                   <Button @click="addEvent" variant="primary">Create Event</Button>
                </div>
             </div>
          </Card>

          <!-- Events List -->
          <div class="space-y-4">
             <h4 class="text-lg font-medium text-neutral-700">Upcoming Events</h4>
             <div v-if="store.events.length === 0" class="text-neutral-500 italic">No events scheduled.</div>

             <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card v-for="(e, idx) in store.events" :key="idx" class="relative group">
                   <div class="flex justify-between items-start">
                      <div>
                         <h4 class="font-bold text-lg text-neutral-900 mb-1">{{ e.name }}</h4>
                         <div class="flex flex-col gap-1 text-sm text-neutral-600">
                             <span class="flex items-center gap-2">
                                <svg class="w-4 h-4 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                                {{ e.date }} at {{ e.time }}
                             </span>
                             <span class="flex items-center gap-2">
                                <svg class="w-4 h-4 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                                {{ e.location }}
                             </span>
                         </div>
                      </div>
                      <Button @click="deleteEvent(idx)" variant="danger" size="sm" class="opacity-0 group-hover:opacity-100 transition-opacity">Delete</Button>
                   </div>
                </Card>
             </div>
          </div>
       </div>

       <!-- BOOKINGS -->
       <div v-if="tab==='bookings'" class="space-y-6">
          <div class="flex justify-between items-center">
             <h3 class="text-xl font-semibold text-neutral-800">Hall Bookings</h3>
          </div>

          <Card title="New Booking">
             <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input v-model="newBooking.hall" label="Hall Name" placeholder="e.g. Main Hall" />
                <Input v-model="newBooking.booked_by" label="Booked By" placeholder="Requester Name" />
                <Input type="date" v-model="newBooking.date" label="Date" />
                <div class="flex gap-2">
                   <div class="flex-1">
                      <Input type="time" v-model="newBooking.start_time" label="Start" />
                   </div>
                   <div class="flex-1">
                      <Input type="time" v-model="newBooking.end_time" label="End" />
                   </div>
                </div>
                <div class="md:col-span-2 flex justify-end mt-2">
                   <Button @click="addBooking" variant="primary">Confirm Booking</Button>
                </div>
             </div>
          </Card>

          <div class="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden">
             <table class="min-w-full divide-y divide-neutral-200">
                <thead class="bg-neutral-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Hall</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Date</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Time</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Booked By</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-neutral-500 uppercase tracking-wider">Action</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-neutral-200">
                  <tr v-if="store.bookings.length === 0">
                     <td colspan="5" class="px-6 py-4 text-center text-sm text-neutral-500 italic">No active bookings.</td>
                  </tr>
                  <tr v-for="(b, idx) in store.bookings" :key="idx" class="hover:bg-neutral-50 transition-colors">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900">{{ b.hall }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-500">{{ b.date }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-500">{{ b.start_time}} - {{ b.end_time }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-500">{{ b.booked_by }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                       <button @click="deleteBooking(idx)" class="text-red-500 hover:text-red-700 font-medium">Cancel</button>
                    </td>
                  </tr>
                </tbody>
             </table>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'
import { useToast } from '../composables/useToast'
import Button from '../components/ui/Button.vue'
import Input from '../components/ui/Input.vue'
import Card from '../components/ui/Card.vue'

const store = useDataStore()
const toast = useToast()
const tab = ref('announcements')
const router = useRouter()

// Forms
const newAnnouncement = ref({ title: '', description: '', date: new Date().toISOString().split('T')[0], important: false })
const newPerson = ref({ name: '', department: '', extension: '', floor: 'Ground Floor' })
const newEvent = ref({ name: '', date: '', time: '', location: '' })
const newBooking = ref({ hall: '', booked_by: '', date: '', start_time: '', end_time: '' })

// Email Logic
const sendEmail = ref(false)
const selectedEmailGroup = ref(null)

onMounted(() => {
  store.fetchAll()
  store.fetchEmailGroups()
})

// --- Feature: Announcements ---
async function addAnnouncement() {
  if(!newAnnouncement.value.title || !newAnnouncement.value.date) {
    toast.warning('Title and Date are required')
    return
  }
  
  const updated = [...store.announcements, { ...newAnnouncement.value, id: Date.now() }]
  const success = await store.saveData('announcements', updated)
  
  if (success) {
     if (sendEmail.value && selectedEmailGroup.value) {
        triggerEmail(selectedEmailGroup.value.email, newAnnouncement.value)
     }
     newAnnouncement.value = { title: '', description: '', date: new Date().toISOString().split('T')[0], important: false }
     sendEmail.value = false
     toast.success('Announcement published successfully!')
  } else {
     toast.error('Failed to publish announcement')
  }
}
async function deleteAnnouncement(idx) {
  if(!confirm('Delete this announcement?')) return
  const updated = [...store.announcements]
  updated.splice(idx, 1)
  const success = await store.saveData('announcements', updated)
  if (success) {
    toast.success('Announcement deleted')
  }
}

// --- Feature: Intercom ---
const editingId = ref(null)
const adminSearch = ref('')


const groupedIntercom = computed(() => {
  const s = adminSearch.value.toLowerCase()
  const dataset = store.intercom.filter(p => {
    return p.name.toLowerCase().includes(s) || 
           p.department.toLowerCase().includes(s) || 
           p.floor?.toLowerCase().includes(s) ||
           p.extension.includes(s)
  })

  // Group strictly by Floor
  const floors = {}

  dataset.forEach(p => {
     const f = p.floor || 'Other'
     if (!floors[f]) floors[f] = {}
     
     // Club by Extension
     const ext = p.extension
     if (!floors[f][ext]) {
        floors[f][ext] = { extension: ext, people: [] }
     }
     floors[f][ext].people.push(p)
  })

  // Sort Floors
  const floorOrder = ['Ground Floor', '1st Floor', '2nd Floor', '3rd Floor']
  const sortedKeys = Object.keys(floors).sort((a,b) => {
     return floorOrder.indexOf(a) - floorOrder.indexOf(b)
  })

  const finalOutput = {}
  sortedKeys.forEach(key => {
     const extGroups = Object.values(floors[key])
     extGroups.sort((a,b) => a.extension.localeCompare(b.extension))
     finalOutput[key] = extGroups
  })

  return finalOutput
})

const editForm = ref({})

async function addPerson() {
   if(!newPerson.value.name || !newPerson.value.extension) {
     toast.warning('Name and Extension are required')
     return
   }
   
   // Create Mode Only
   const updated = [...store.intercom, { ...newPerson.value, id: Date.now() }]
   const success = await store.saveData('intercom', updated)
   
   if (success) {
     newPerson.value = { name: '', department: '', extension: '', floor: 'Ground Floor' }
     toast.success('Person added to directory')
   }
}

// Inline Edit Logic
function startEdit(p) {
  editForm.value = { ...p }
  editingId.value = p.id
}

async function saveEdit() {
  if(!editForm.value.name) return
  
  const updated = store.intercom.map(p => p.id === editingId.value ? { ...editForm.value } : p)
  const success = await store.saveData('intercom', updated)
  
  if (success) {
    toast.success('Directory updated')
    cancelEdit()
  }
}

function cancelEdit() {
  editingId.value = null
  editForm.value = {}
}

async function deletePerson(id) {
   if(!confirm('Delete user?')) return
   const updated = store.intercom.filter(p => p.id !== id)
   const success = await store.saveData('intercom', updated)
   if (success) toast.success('Person deleted')
}

// --- Feature: Events ---
async function addEvent() {
  if(!newEvent.value.name || !newEvent.value.date) {
    toast.warning('Event Name and Date required')
    return
  }
  const updated = [...store.events, { ...newEvent.value, id: Date.now() }]
  const success = await store.saveData('events', updated)
  
  if (success) {
    newEvent.value = { name: '', date: '', time: '', location: '' }
    toast.success('Event created successfully')
  }
}
async function deleteEvent(idx) {
  if(!confirm('Delete event?')) return
  const updated = [...store.events]
  updated.splice(idx, 1)
  const success = await store.saveData('events', updated)
  if (success) toast.success('Event deleted')
}

// --- Feature: Bookings ---
async function addBooking() {
  if(!newBooking.value.hall || !newBooking.value.date) {
    toast.warning('Hall and Date required')
    return
  }
  const updated = [...store.bookings, { ...newBooking.value, id: Date.now() }]
  const success = await store.saveData('bookings', updated)
  
  if (success) {
    newBooking.value = { hall: '', booked_by: '', date: '', start_time: '', end_time: '' }
    toast.success('Booking confirmed!')
  }
}
async function deleteBooking(idx) {
  if(!confirm('Cancel booking?')) return
  const updated = [...store.bookings]
  updated.splice(idx, 1)
  const success = await store.saveData('bookings', updated)
  if (success) toast.success('Booking cancelled')
}

function triggerEmail(recipientEmail, announcement) {
   const subject = encodeURIComponent(`Intranet Update: ${announcement.title}`)
   const body = encodeURIComponent(
`New Announcement:

${announcement.title}
Date: ${announcement.date}

${announcement.description}

View full details on the Intranet Dashboard.
`
   )
   window.location.href = `mailto:${recipientEmail}?subject=${subject}&body=${body}`
}
</script>
