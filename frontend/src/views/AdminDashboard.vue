<template>
  <div class="admin-wrapper" style="width: 100%; max-width: 1200px; margin: 0 auto; padding: 2rem;">
    <header class="admin-header">
        <h1>Admin Dashboard</h1>
        <button class="btn-outline" @click="$router.push('/')">Exit & View Site</button>
    </header>
    
    <div class="tabs">
      <button :class="{active: tab==='announcements'}" @click="tab='announcements'">Announcements</button>
      <button :class="{active: tab==='intercom'}" @click="tab='intercom'">Intercom</button>
      <button :class="{active: tab==='events'}" @click="tab='events'">Events</button>
       <button :class="{active: tab==='bookings'}" @click="tab='bookings'">Bookings</button>
    </div>

    <div class="content">
       <!-- ANNOUNCEMENTS -->
       <div v-if="tab==='announcements'">
          <h3>Manage Announcements</h3>
          <div class="card"> <!-- New Announcement Form -->
            <h4>New Announcement</h4>
            <input v-model="newAnnouncement.title" placeholder="Title" />
            <textarea v-model="newAnnouncement.description" placeholder="Description"></textarea>
            <input v-model="newAnnouncement.date" type="date" />
            <label>
              <input type="checkbox" v-model="newAnnouncement.important" style="width:auto;" /> Important
            </label>
            <br/><br/>
            
            <!-- Email Logic -->
             <div style="background:#f0fbff; padding:10px; border:1px solid #cceeff; border-radius:4px; margin-bottom:10px;">
                <label style="font-weight:bold;">
                  <input type="checkbox" v-model="sendEmail" style="width:auto;" /> Send Email Notification ✔
                </label>
                <div v-if="sendEmail">
                  <select v-model="selectedEmailGroup">
                     <option :value="null">Select Recipient Group...</option>
                     <option v-for="g in store.emailGroups" :key="g.id" :value="g">{{ g.name }}</option>
                  </select>
                </div>
             </div>

            <button @click="addAnnouncement">Publish</button>
          </div>
          
          <div v-for="(item, idx) in store.announcements" :key="idx" class="card" style="display:flex; justify-content:space-between;">
             <div>
               <strong>{{ item.title }}</strong> ({{ item.date }})
             </div>
             <button @click="deleteAnnouncement(idx)" style="background:red;">Delete</button>
          </div>
       </div>

        <!-- INTERCOM -->
        <div v-if="tab==='intercom'">
           <h3>Manage Intercom</h3>
           
           <!-- Search Bar for Admin -->
           <input v-model="adminSearch" placeholder="Search directory..." style="width:100%; padding:10px; margin-bottom:15px; border:1px solid #ddd; border-radius:4px;" />

           <!-- ADD NEW PERSON FORM (Only for creation now) -->
           <div class="card" style="border:1px solid #4caf50;">
             <h4 style="margin-top:0; color:#2e7d32;">Add New Person</h4>
             <div style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr auto; gap:10px; align-items:center;">
                <select v-model="newPerson.floor" style="padding:8px;">
                   <option>Ground Floor</option>
                   <option>1st Floor</option>
                   <option>2nd Floor</option>
                   <option>3rd Floor</option>
                </select>
                <input v-model="newPerson.name" placeholder="Name" style="padding:8px;" />
                <input v-model="newPerson.department" placeholder="Department" style="padding:8px;" />
                <input v-model="newPerson.extension" placeholder="Ext" style="width:80px; padding:8px;" />
                <button @click="addPerson" style="background:#4caf50;">+ Add</button>
             </div>
           </div>

           <!-- Grouped List View for Admin -->
           <div class="admin-intercom-list">
              <div v-for="(floorData, floorName) in groupedIntercom" :key="floorName" style="margin-bottom:20px;">
                 <h4 style="background:#eee; padding:5px; border-bottom:2px solid #ccc; margin-bottom:0;">{{ floorName }}</h4>
                 <div style="border:1px solid #eee; padding:10px;">
                    <div v-for="item in floorData" :key="item.extension" style="display:flex; border-bottom:1px solid #f0f0f0; padding:8px 0; align-items:center;">
                       <div style="width:60px; font-weight:bold; font-size:1.1rem; color:#555;">{{ item.extension }}</div>
                       <div style="flex:1;">
                          <!-- Loop People in this Extension -->
                          <div v-for="(p, idx) in item.people" :key="p.id" class="person-row" style="margin-bottom:5px;">
                             
                             <!-- INLINE EDITING MODE -->
                             <div v-if="editingId === p.id" class="edit-grid-row">
                                <form @submit.prevent="saveEdit" style="display:contents">
                                  <input v-model="editForm.name" placeholder="Name" class="edit-input" title="Name" />
                                  <input v-model="editForm.department" placeholder="Dept" class="edit-input" title="Department" />
                                  <select v-model="editForm.floor" class="edit-input">
                                     <option>Ground Floor</option>
                                     <option>1st Floor</option>
                                     <option>2nd Floor</option>
                                     <option>3rd Floor</option>
                                  </select>
                                  <input v-model="editForm.extension" placeholder="Ext" class="edit-input" style="text-align:center;" title="Extension" />
                                  
                                  <div style="display:flex; gap:5px; align-items:center;">
                                    <button type="submit" style="background:#2196f3; color:white; border:none; padding:6px 12px; height:32px; border-radius:4px; cursor:pointer; display:flex; align-items:center; justify-content:center;" title="Save">💾</button>
                                    <button @click="cancelEdit" type="button" style="background:#f44336; color:white; border:none; padding:6px 12px; height:32px; border-radius:4px; cursor:pointer; display:flex; align-items:center; justify-content:center;" title="Cancel">❌</button>
                                  </div>
                                </form>
                             </div>

                             <!-- READ MODE -->
                             <div v-else style="display:flex; justify-content:space-between; align-items:center; padding:2px 0;">
                                <div>
                                   <strong>{{ p.name }}</strong> <small style="color:#777;">({{ p.department }})</small>
                                </div>
                                <div style="display:flex; gap:5px;">
                                   <button @click="startEdit(p)" style="background:transparent; border:1px solid orange; color:orange; padding:2px 6px; font-size:0.8rem; cursor:pointer;" title="Edit">✏️</button>
                                   <button @click="deletePerson(p.id)" style="background:transparent; border:1px solid red; color:red; padding:2px 6px; font-size:0.8rem; cursor:pointer;" title="Delete">🗑️</button>
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
       <div v-if="tab==='events'">
          <h3>Manage Events</h3>
          <div class="card">
             <input v-model="newEvent.name" placeholder="Event Name" style="margin-bottom:10px; display:block;" />
             <input v-model="newEvent.date" type="date" style="margin-bottom:10px; margin-right:10px;" />
             <input v-model="newEvent.time" type="time" style="margin-bottom:10px;" />
             <input v-model="newEvent.location" placeholder="Location" style="display:block; margin-bottom:10px;" />
             <button @click="addEvent">Add Event</button>
          </div>
          <div v-for="(e, idx) in store.events" :key="idx" class="card" style="display:flex; justify-content:space-between; align-items:center;">
             <div>
                <strong>{{ e.name }}</strong><br/>
                <small>{{ e.date }} @ {{ e.time }} ({{ e.location }})</small>
             </div>
             <button @click="deleteEvent(idx)" style="background:red;">Delete</button>
          </div>
       </div>

       <!-- BOOKINGS -->
       <div v-if="tab==='bookings'">
          <h3>Hall Bookings</h3>
          <div class="card">
             <input v-model="newBooking.hall" placeholder="Hall Name (e.g. Main Hall)" style="display:block; margin-bottom:10px;" />
             <input v-model="newBooking.booked_by" placeholder="Booked By" style="display:block; margin-bottom:10px;" />
             <div style="margin-bottom:10px;">
               <input v-model="newBooking.date" type="date" style="margin-right:10px;" />
               <input v-model="newBooking.start_time" type="time" style="width:auto;" /> - 
               <input v-model="newBooking.end_time" type="time" style="width:auto;" />
             </div>
             <button @click="addBooking">Book Hall</button>
          </div>
          <table style="width:100%; text-align:left;">
             <thead>
               <tr>
                 <th>Hall</th>
                 <th>Date</th>
                 <th>Time</th>
                 <th>Booked By</th>
                 <th>Action</th>
               </tr>
             </thead>
             <tbody>
               <tr v-for="(b, idx) in store.bookings" :key="idx">
                 <td>{{ b.hall }}</td>
                 <td>{{ b.date }}</td>
                 <td>{{ b.start_time}} - {{ b.end_time }}</td>
                 <td>{{ b.booked_by }}</td>
                 <td><button @click="deleteBooking(idx)" style="background:red; padding:2px 5px;">X</button></td>
               </tr>
             </tbody>
          </table>
       </div>
       
       <!-- Feedback Toast -->
       <div v-if="feedback" style="position:fixed; bottom:20px; right:20px; background:#4caf50; color:white; padding:10px 20px; border-radius:4px; box-shadow:0 2px 10px rgba(0,0,0,0.2); z-index:1000;">
          {{ feedback }}
       </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'

const store = useDataStore()
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

// UI Feedback
const feedback = ref('')

onMounted(() => {
  store.fetchAll()
  store.fetchEmailGroups()
})

// --- Feature: Announcements ---
async function addAnnouncement() {
  if(!newAnnouncement.value.title || !newAnnouncement.value.date) return alert('Title and Date required')
  
  const updated = [...store.announcements, { ...newAnnouncement.value, id: Date.now() }]
  const success = await store.saveData('announcements', updated)
  
  if (success) {
     if (sendEmail.value && selectedEmailGroup.value) {
        triggerEmail(selectedEmailGroup.value.email, newAnnouncement.value)
     }
     newAnnouncement.value = { title: '', description: '', date: new Date().toISOString().split('T')[0], important: false }
     sendEmail.value = false
     showFeedback('Announcement Published!')
  }
}
async function deleteAnnouncement(idx) {
  if(!confirm('Delete this announcement?')) return
  const updated = [...store.announcements]
  updated.splice(idx, 1)
  await store.saveData('announcements', updated)
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
   if(!newPerson.value.name || !newPerson.value.extension) return alert('Name and Extension required')
   
   // Create Mode Only
   const updated = [...store.intercom, { ...newPerson.value, id: Date.now() }]
   await store.saveData('intercom', updated)
   
   // Reset new person form
   newPerson.value = { name: '', department: '', extension: '', floor: 'Ground Floor' }
   showFeedback('Person added!')
}

// Inline Edit Logic
function startEdit(p) {
  editForm.value = { ...p }
  editingId.value = p.id
}

async function saveEdit() {
  if(!editForm.value.name) return
  
  const updated = store.intercom.map(p => p.id === editingId.value ? { ...editForm.value } : p)
  await store.saveData('intercom', updated)
  
  showFeedback('Updated successfully')
  cancelEdit()
}

function cancelEdit() {
  editingId.value = null
  editForm.value = {}
}

async function deletePerson(id) {
   if(!confirm('Delete user?')) return
   const updated = store.intercom.filter(p => p.id !== id)
   await store.saveData('intercom', updated)
}

// --- Feature: Events ---
async function addEvent() {
  if(!newEvent.value.name || !newEvent.value.date) return alert('Event Name and Date required')
  const updated = [...store.events, { ...newEvent.value, id: Date.now() }]
  await store.saveData('events', updated)
  newEvent.value = { name: '', date: '', time: '', location: '' }
  showFeedback('Event created!')
}
async function deleteEvent(idx) {
  if(!confirm('Delete event?')) return
  const updated = [...store.events]
  updated.splice(idx, 1)
  await store.saveData('events', updated)
}

// --- Feature: Bookings ---
async function addBooking() {
  if(!newBooking.value.hall || !newBooking.value.date) return alert('Hall and Date required')
  const updated = [...store.bookings, { ...newBooking.value, id: Date.now() }]
  await store.saveData('bookings', updated)
  newBooking.value = { hall: '', booked_by: '', date: '', start_time: '', end_time: '' }
  showFeedback('Booking confirmed!')
}
async function deleteBooking(idx) {
  if(!confirm('Cancel booking?')) return
  const updated = [...store.bookings]
  updated.splice(idx, 1)
  await store.saveData('bookings', updated)
}

// Helper
function showFeedback(msg) {
  feedback.value = msg
  setTimeout(() => feedback.value = '', 3000)
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

<style scoped>
.admin-header {
  display: flex; 
  justify-content: space-between; 
  align-items: center;
  margin-bottom: 2rem;
}

.tabs { margin-bottom: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; }
.tabs button { 
  background: transparent; 
  color: var(--text-muted); 
  margin-right: 1rem; 
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
}
.tabs button:hover { background: var(--bg-page); color: var(--text-main); }
.tabs button.active { background: var(--primary); color: white; }

.btn-outline {
  background: transparent;
  border: 1px solid var(--primary);
  color: var(--primary);
}
.btn-outline:hover {
  background: var(--primary);
  color: white;
}

.edit-grid-row {
  display: grid;
  grid-template-columns: 2fr 2fr 1.5fr 0.8fr auto;
  gap: 15px; /* Increased gap */
  align-items: center;
  width: 100%;
  padding: 8px 10px; /* Added horizontal padding */
  background: #f9f9f9;
  border-radius: 4px;
  box-shadow: inset 0 0 5px rgba(0,0,0,0.05); /* Subtle depth */
}
.edit-input {
  width: 100%;
  padding: 0 8px; /* Horizontal padding only, height set explicitly */
  height: 32px; /* Fixed height matching buttons */
  line-height: 32px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9rem;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .edit-grid-row {
    grid-template-columns: 1fr; /* Stack vertically on mobile */
    gap: 10px;
    padding: 10px;
  }
  .edit-grid-row input, .edit-grid-row select {
    width: 100%;
  }
  .edit-grid-row div[style*="display:flex"] {
     width: 100%;
     display: grid !important; /* Force buttons to grid */
     grid-template-columns: 1fr 1fr;
     gap: 10px;
  }
}
</style>
