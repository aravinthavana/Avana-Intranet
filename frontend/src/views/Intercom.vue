<template>
  <div class="max-w-[1400px] mx-auto p-6 intercom-container">
    <!-- Header -->
    <div class="mb-8 no-print">
      <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-5">
        <div>
          <h1 class="text-3xl font-bold text-neutral-900 leading-tight">Intercom Directory</h1>
          <p class="text-neutral-500 mt-2">Office phone directory</p>
        </div>
        
        <div class="flex flex-wrap items-center gap-3">
          <input 
            v-model="searchQuery" 
            name="search"
            placeholder="Search by name, department, or extension..." 
            class="w-full md:w-auto md:min-w-[300px] px-4 py-3 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
          />
          
          <template v-if="isAdmin">
            <button @click="showPasswordModal = true" class="inline-flex items-center gap-2 px-5 py-3 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 hover:border-neutral-400 transition-all duration-200" title="Change Password">
              <Icon name="cog" size="sm" />
            </button>

            <button @click="toggleEditMode" class="inline-flex items-center gap-2 px-5 py-3 text-sm font-medium text-neutral-700 bg-white border border-neutral-300 rounded-lg hover:bg-neutral-50 hover:border-neutral-400 transition-all duration-200">
              <Icon :name="isEditMode ? 'x' : 'edit'" size="sm" />
              <span>{{ isEditMode ? 'Cancel' : 'Edit Mode' }}</span>
            </button>
          </template>
          
          <button @click="printDirectory" class="inline-flex items-center gap-2 px-5 py-3 text-sm font-semibold text-white bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg shadow-sm hover:-translate-y-px hover:shadow-md transition-all duration-200">
            <Icon name="print" size="sm" />
            <span>Print</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Password Change Modal -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md p-6 animate-fade-in relative">
        <button @click="showPasswordModal = false" class="absolute top-4 right-4 text-neutral-400 hover:text-neutral-600">
          <Icon name="x" size="sm" />
        </button>
        
        <h3 class="text-xl font-bold text-neutral-900 mb-6">Change Admin Password</h3>
        
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="text-sm font-medium text-neutral-700">Current Password</label>
            <input type="password" v-model="passwordForm.old" class="w-full px-4 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none" placeholder="Enter current password" />
          </div>
          
          <div class="space-y-1">
            <label class="text-sm font-medium text-neutral-700">New Password</label>
            <input type="password" v-model="passwordForm.new" class="w-full px-4 py-2 text-sm border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 outline-none" placeholder="Enter new password (min 6 chars)" />
          </div>
        </div>
        
        <div class="flex gap-3 mt-8">
          <button @click="changeAdminPassword" class="flex-1 px-4 py-2 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors">
            Update Password
          </button>
          <button @click="showPasswordModal = false" class="flex-1 px-4 py-2 bg-white border border-neutral-300 text-neutral-700 font-medium rounded-lg hover:bg-neutral-50 transition-colors">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Add New Person Form (Edit Mode Only) -->
    <div v-if="isEditMode" class="bg-white rounded-xl shadow-card p-6 mb-6 border-l-4 border-primary-500 no-print">
      <h3 class="text-xl font-semibold text-neutral-800 mb-6">Add New Person</h3>
      <div class="grid grid-cols-1 sm:grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-4 items-end">
        <select v-model="newPerson.floor" name="new-floor" class="w-full px-4 py-3 text-sm bg-white border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200">
          <option>Ground Floor</option>
          <option>1st Floor</option>
          <option>2nd Floor</option>
          <option>3rd Floor</option>
        </select>
        
        <input v-model="newPerson.name" name="new-name" placeholder="Full Name" class="w-full px-4 py-3 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200" />
        <input v-model="newPerson.department" name="new-dept" placeholder="Department" class="w-full px-4 py-3 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200" />
        <input v-model="newPerson.extension" name="new-ext" placeholder="Extension" class="w-full px-4 py-3 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200" />
        
        <button @click="addPerson" class="inline-flex items-center gap-2 px-5 py-3 text-sm font-semibold text-white bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg shadow-sm hover:-translate-y-px hover:shadow-md transition-all duration-200">
          <Icon name="plus" size="sm" />
          <span>Add Person</span>
        </button>
      </div>
    </div>

    <!-- Intercom Directory Grouped List (Screen View) -->
    <div class="flex flex-col gap-8 no-print">
      <div v-for="(extensions, floor) in groupedIntercom" :key="floor" class="animate-fade-in">
        <div class="flex items-center gap-4 mb-6">
          <h2 class="text-xl font-bold text-neutral-800">{{ floor }}</h2>
          <div class="h-px bg-neutral-200 flex-1"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div 
            v-for="ext in extensions" 
            :key="ext.extension" 
            class="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden flex flex-col transition-all duration-200 hover:shadow-md"
            :class="{ 'ring-2 ring-primary-500 ring-offset-2': isEditMode && ext.people.some(p => editingId === p.id) }"
          >
            <!-- Header: Extension Number -->
            <div class="bg-neutral-50 border-b border-neutral-100 p-4 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="px-3 py-1.5 bg-primary-600 text-white font-mono font-bold text-lg rounded-lg shadow-sm">
                  {{ ext.extension }}
                </div>
                <span class="text-xs font-semibold text-neutral-400 uppercase tracking-wider">Extension</span>
              </div>
            </div>

            <!-- People List -->
            <div class="divide-y divide-neutral-100">
              <div 
                v-for="person in ext.people" 
                :key="person.id" 
                class="group bg-white"
                :class="{ 'bg-blue-50/50': editingId === person.id }"
              >
                <!-- Edit View -->
                <div v-if="editingId === person.id" class="p-4 bg-white">
                  <div class="flex flex-col gap-3">
                    <div class="space-y-1">
                      <label class="text-[10px] uppercase font-bold text-neutral-400 tracking-wider">Name</label>
                      <input v-model="editForm.name" class="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 outline-none" placeholder="Full Name" />
                    </div>
                    <div class="space-y-1">
                      <label class="text-[10px] uppercase font-bold text-neutral-400 tracking-wider">Department</label>
                      <input v-model="editForm.department" class="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 outline-none" placeholder="Department" />
                    </div>
                    
                    <div class="flex gap-2 pt-2">
                      <button @click="saveEdit" class="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-primary-600 text-white text-xs font-medium rounded-lg hover:bg-primary-700 transition-colors">
                        <Icon name="check" size="sm" />
                        Save
                      </button>
                      <button @click="cancelEdit" class="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-white border border-neutral-200 text-neutral-600 text-xs font-medium rounded-lg hover:bg-neutral-50 transition-colors">
                        <Icon name="x" size="sm" />
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Read View -->
                <div v-else class="p-4 flex items-center gap-3 hover:bg-neutral-50 transition-colors duration-200">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-neutral-100 to-neutral-200 text-neutral-500 flex items-center justify-center font-bold text-xs border border-neutral-200 shrink-0">
                    {{ person.name.charAt(0).toUpperCase() }}
                  </div>
                  
                  <div class="flex flex-col min-w-0 flex-1">
                    <span class="font-semibold text-neutral-900 text-sm truncate">{{ person.name }}</span>
                    <span class="text-xs text-neutral-500 truncate">{{ person.department }}</span>
                  </div>

                  <!-- Actions -->
                  <div v-if="isEditMode" class="flex items-center gap-1 opacity-100">
                    <button @click="startEdit(person)" class="p-1.5 text-neutral-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors" title="Edit">
                      <Icon name="edit" size="xs" />
                    </button>
                    <button @click="deletePerson(person.id)" class="p-1.5 text-neutral-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Delete">
                      <Icon name="trash" size="xs" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Print View (Hidden on Screen) -->
    <div class="print-only directory-sheet" id="print-area">
      <div class="sheet-header">
        <h2>Avana Head Quarters Intercom List</h2>
      </div>

      <div class="table-container">
        <!-- LEFT COLUMN: Ground Floor & 1st Floor -->
        <table class="intercom-table left-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Intercom No</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="floor in ['Ground Floor', '1st Floor']" :key="floor">
              <template v-if="groupedIntercom[floor]">
                <tr class="floor-row">
                  <td colspan="2" class="floor-cell">{{ floor }}</td>
                </tr>
                <tr v-for="ext in groupedIntercom[floor]" :key="ext.extension">
                  <td class="name-col">
                    <span v-for="(person, idx) in ext.people" :key="person.id">
                      <span class="person-name">{{ person.name }}</span>
                      <span class="person-designation">({{ person.department }})</span>
                      <span v-if="idx < ext.people.length - 1">, </span>
                    </span>
                  </td>
                  <td class="ext-col">{{ ext.extension }}</td>
                </tr>
              </template>
            </template>
          </tbody>
        </table>

        <!-- RIGHT COLUMN: 2nd Floor & 3rd Floor -->
        <table class="intercom-table right-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Intercom No</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="floor in ['2nd Floor', '3rd Floor']" :key="floor">
              <template v-if="groupedIntercom[floor]">
                <tr class="floor-row">
                  <td colspan="2" class="floor-cell">{{ floor }}</td>
                </tr>
                <tr v-for="ext in groupedIntercom[floor]" :key="ext.extension">
                  <td class="name-col">
                    <span v-for="(person, idx) in ext.people" :key="person.id">
                      <span class="person-name">{{ person.name }}</span>
                      <span class="person-designation">({{ person.department }})</span>
                      <span v-if="idx < ext.people.length - 1">, </span>
                    </span>
                  </td>
                  <td class="ext-col">{{ ext.extension }}</td>
                </tr>
              </template>
            </template>
          </tbody>
        </table>
      </div>

      <div class="sheet-footer">
         <div class="footer-header">Quick Reference Guide</div>
         <div class="footer-note"><strong>Call Pickup:</strong> Dial <strong>*0</strong> to answer a ringing phone</div>
         <div class="footer-note"><strong>Redial:</strong> Dial <strong>6</strong> to redial</div>
         <div class="footer-note"><strong>Transfer Call:</strong> Press <strong>Flash</strong>, then dial the <strong>Extension Number</strong></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDataStore } from '../stores/data'
import { useToast } from '../composables/useToast'
import Icon from '../components/ui/Icon.vue'

const store = useDataStore()
const toast = useToast()
const route = useRoute()

const searchQuery = ref('')
const isEditMode = ref(false)
const showPasswordModal = ref(false)
const passwordForm = ref({ old: '', new: '' })
const editingId = ref(null)
const editForm = ref({})
const newPerson = ref({ name: '', department: '', extension: '', floor: 'Ground Floor' })

const isAdmin = computed(() => {
  return store.isAuthenticated()
})

async function changeAdminPassword() {
  if (!passwordForm.value.old || !passwordForm.value.new) {
    toast.warning('Please fill in both fields')
    return
  }
  
  if (passwordForm.value.new.length < 6) {
    toast.warning('New password must be at least 6 characters')
    return
  }
  
  const success = await store.changePassword(passwordForm.value.old, passwordForm.value.new)
  if (success) {
    toast.success('Password updated successfully')
    showPasswordModal.value = false
    passwordForm.value = { old: '', new: '' }
  }
}

onMounted(() => {
  store.fetchAll()
})

const filteredIntercom = computed(() => {
  const query = searchQuery.value.toLowerCase()
  if (!query) return store.intercom
  
  return store.intercom.filter(p => {
    return p.name.toLowerCase().includes(query) ||
           p.department.toLowerCase().includes(query) ||
           p.extension.includes(query) ||
           p.floor?.toLowerCase().includes(query)
  })
})

const flatIntercom = computed(() => {
  const floors = {}
  
  filteredIntercom.value.forEach(p => {
    const floor = p.floor || 'Other'
    if (!floors[floor]) floors[floor] = []
    floors[floor].push(p)
  })
  
  const floorOrder = ['Ground Floor', '1st Floor', '2nd Floor', '3rd Floor']
  const sortedKeys = Object.keys(floors).sort((a, b) => {
    return floorOrder.indexOf(a) - floorOrder.indexOf(b)
  })
  
  const result = {}
  sortedKeys.forEach(key => {
    result[key] = floors[key].sort((a, b) => a.name.localeCompare(b.name))
  })
  
  return result
})

const groupedIntercom = computed(() => {
  const floors = {}
  
  filteredIntercom.value.forEach(p => {
    const floor = p.floor || 'Other'
    if (!floors[floor]) floors[floor] = {}
    
    const ext = p.extension
    if (!floors[floor][ext]) {
      floors[floor][ext] = { extension: ext, people: [] }
    }
    floors[floor][ext].people.push(p)
  })
  
  const floorOrder = ['Ground Floor', '1st Floor', '2nd Floor', '3rd Floor']
  const sortedKeys = Object.keys(floors).sort((a, b) => {
    return floorOrder.indexOf(a) - floorOrder.indexOf(b)
  })
  
  const result = {}
  sortedKeys.forEach(key => {
    const extGroups = Object.values(floors[key])
    extGroups.sort((a, b) => a.extension.localeCompare(b.extension))
    result[key] = extGroups
  })
  
  return result
})

function toggleEditMode() {
  isEditMode.value = !isEditMode.value
  if (!isEditMode.value) {
    cancelEdit()
  }
}

async function addPerson() {
  if (!newPerson.value.name || !newPerson.value.extension) {
    toast.warning('Name and Extension are required')
    return
  }
  
  const success = await store.addIntercom(newPerson.value)
  
  if (success) {
    newPerson.value = { name: '', department: '', extension: '', floor: 'Ground Floor' }
    toast.success('Person added to directory')
  }
}

function startEdit(person) {
  editForm.value = { ...person }
  editingId.value = person.id
}

async function saveEdit() {
  if (!editForm.value.name) return
  
  const success = await store.updateIntercom(editingId.value, editForm.value)
  
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
  if (!confirm('Delete this person from the directory?')) return
  
  const success = await store.deleteIntercom(id)
  
  if (success) {
    toast.success('Person deleted')
  }
}

function printDirectory() {
  window.print()
}
</script>

<style scoped>
@media print {
  .intercom-container {
    padding: 0 !important;
  }
}

/* Print view styles (Specific to Intercom) */
@page { 
  margin: 0.5cm; 
  size: A4 landscape;
}

.directory-sheet { 
  background: white; 
  padding: 10px;
  font-family: Arial, sans-serif;
  font-size: 9pt;
}

.sheet-header { 
  text-align: center;
  padding: 4px;
  border-bottom: 2px solid #000;
  margin-bottom: 5px;
}

.sheet-header h2 { 
  font-size: 11pt !important;
  margin: 0 !important;
  font-weight: bold;
}

.table-container { 
  display: flex; 
  gap: 8px; 
  justify-content: space-between;
}

.intercom-table { 
  width: 49%; 
  border-collapse: collapse;
  font-size: 8pt;
}

.intercom-table th { 
  background: #333; 
  color: white; 
  padding: 3px 5px;
  text-align: left;
  font-weight: bold;
  font-size: 8.5pt;
}

.intercom-table td { 
  padding: 2px 5px;
  border-bottom: 1px solid #ddd;
}

.floor-row { 
  background: #f0f0f0 !important; 
  font-weight: bold;
}

.floor-cell { 
  padding: 3px 5px !important;
  font-size: 8.5pt;
}

.name-col { 
  width: 70%; 
}

.ext-col { 
  width: 30%; 
  text-align: center;
  font-weight: bold;
}

.person-name { 
  font-weight: 600; 
}

.person-designation { 
  font-style: italic; 
  color: #555;
}

.sheet-footer { 
  margin-top: 8px; 
  padding-top: 5px;
  border-top: 1px solid #ccc;
  font-size: 7.5pt;
}

.footer-header { 
  font-weight: bold; 
  margin-bottom: 3px;
  font-size: 8pt;
}

.footer-note { 
  margin: 2px 0; 
}
</style>
