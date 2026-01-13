<template>
  <div class="intercom-page">
    <div class="no-print header-actions">
      <h1>Intercom Directory</h1>
      
      <div class="controls">
         <input v-model="search" placeholder="Search..." class="search-box" />
         <button @click="printDirectory" class="print-btn">🖨️ Print</button>
      </div>
    </div>

    <!-- Printable Area -->
    <div class="directory-sheet" id="print-area">
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
                <!-- Floor Header Row -->
                <tr class="floor-row">
                  <td colspan="2" class="floor-cell">{{ floor }}</td>
                </tr>
                <!-- Extension Rows -->
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

        <!-- RIGHT COLUMN: 2nd Floor & Other -->
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
                <!-- Floor Header Row -->
                <tr class="floor-row">
                  <td colspan="2" class="floor-cell">{{ floor }}</td>
                </tr>
                <!-- Extension Rows -->
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
import { useDataStore } from '../stores/data'

const store = useDataStore()
const search = ref('')

onMounted(() => {
  store.fetchAll()
})

const groupedIntercom = computed(() => {
  const s = search.value.toLowerCase()
  const filtered = store.intercom.filter(p => {
    return p.name.toLowerCase().includes(s) || 
           p.department.toLowerCase().includes(s) || 
           p.floor?.toLowerCase().includes(s) ||
           p.extension.includes(s)
  })
  
  // Group by Floor, then by Extension
  const floors = {}
  
  filtered.forEach(p => {
    const f = p.floor || 'Other'
    if (!floors[f]) floors[f] = {}
    
    const ext = p.extension
    if (!floors[f][ext]) {
      floors[f][ext] = { extension: ext, people: [] }
    }
    floors[f][ext].people.push(p)
  })
  
  // Sort floors and extensions
  const floorOrder = ['Ground Floor', '1st Floor', '2nd Floor', '3rd Floor', 'Other']
  const sortedFloors = {}
  
  floorOrder.forEach(floor => {
    if (floors[floor]) {
      const extensions = Object.values(floors[floor])
      extensions.sort((a, b) => a.extension.localeCompare(b.extension))
      sortedFloors[floor] = extensions
    }
  })
  
  return sortedFloors
})


function printDirectory() {
  window.print()
}
</script>

<style scoped>
.intercom-page { 
  max-width: 1200px; 
  margin: 0 auto; 
  padding: 20px;
  font-family: 'Segoe UI', sans-serif; 
}

.header-actions { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 20px; 
}
.controls { display: flex; gap: 10px; align-items: center; }

.search-box { 
  padding: 8px; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
}
.print-btn { 
  background: #333; 
  color: white; 
  border: none; 
  padding: 8px 12px; 
  border-radius: 4px; 
  cursor: pointer; 
}

/* Sheet Container */
.directory-sheet { 
  background: white; 
  border: 2px solid #000;
  padding: 10px;
}

.sheet-header {
  text-align: center; 
  padding: 8px;
  border-bottom: 2px solid #000;
  margin-bottom: 10px;
}
.sheet-header h2 { 
  margin: 0; 
  font-size: 1.2rem; 
  color: #000; 
  font-weight: bold;
}

/* Table Container - Side by Side */
.table-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 10px;
}

/* Table Styling */
.intercom-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #000;
}

.intercom-table thead {
  background: #d3d3d3;
}

.intercom-table th {
  padding: 6px 8px;
  text-align: left;
  font-weight: bold;
  font-size: 0.9rem;
  border: 1px solid #000;
  color: #000;
}

/* Floor Header Rows */
.floor-row {
  background: #f0f0f0;
}

.floor-cell {
  padding: 4px 8px;
  font-weight: bold;
  font-size: 0.95rem;
  color: #000;
  border: 1px solid #000;
  text-align: center;
}

/* Data Rows */
.intercom-table tbody tr:not(.floor-row) td {
  padding: 4px 8px;
  border: 1px solid #000;
  font-size: 0.9rem;
}

.name-col {
  text-align: left;
}

.person-name {
  font-weight: 600;
}

.person-designation {
  font-weight: normal;
  color: #666;
  font-size: 0.85rem;
}

.ext-col { 
  font-weight: bold; 
  text-align: center;
  width: 80px;
}

.sheet-footer {
  border-top: 2px solid #000;
  padding: 0;
  font-size: 0.75rem;
  text-align: center;
}

.footer-header {
  background: #e9ecef;
  font-weight: bold;
  padding: 6px;
  border-bottom: 2px solid #000;
  font-size: 0.85rem;
  color: #333;
}

.footer-note {
  margin: 3px 0;
  padding: 2px;
  border-bottom: 1px solid #ddd;
}
.footer-note:last-child {
  border-bottom: none;
}

@media screen and (max-width: 900px) {
  .table-container {
    grid-template-columns: 1fr;
  }
}
</style>



<!-- GLOBAL PRINT STYLES (NON-SCOPED) -->
<style>
@page { 
  margin: 0.75cm; 
  size: A4 portrait;
}

@media print {
  /* HIDE ALL UI ELEMENTS */
  .sidebar, .top-bar, .mobile-toggle, .btn-outline, 
  .admin-link, .sidebar-overlay, .no-print { 
    display: none !important; 
  }
  
  /* RESET LAYOUT FOR FULL WIDTH */
  html, body, #app, #app-layout, .content-wrapper, .main-content {
    width: 100% !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
    display: block !important;
    overflow: visible !important;
  }

  /* ENSURE BOX-SIZING FOR PRINT */
  * {
    box-sizing: border-box !important;
  }

  .intercom-page {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  /* Sheet */
  .directory-sheet { 
    width: 100%; 
    border: 2px solid #000;
    padding: 5px;
    overflow: hidden; /* Clear floats */
  }
  
  /* Header */
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

  /* 2-Column Grid */
  .table-container {
    display: block;
    width: 100%;
    overflow: hidden;
  }

  .intercom-table {
    width: 48%; /* Safe width */
    border-collapse: collapse;
    border: 1px solid #000;
    page-break-inside: avoid;
  }

  .left-table {
    float: left;
  }

  .right-table {
    float: right;
    margin-right: 0;
  }

  .intercom-table thead {
    background: #d3d3d3 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .intercom-table th {
    padding: 3px 5px !important;
    font-size: 8pt !important;
    font-weight: bold;
    border: 1px solid #000 !important;
    text-align: left;
  }

  /* Floor Rows */
  .floor-row {
    background: #f0f0f0 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .floor-cell {
    padding: 3px 5px !important;
    font-size: 9pt !important;
    font-weight: bold;
    border: 1px solid #000 !important;
    text-align: center;
  }

  /* Data Rows */
  .intercom-table tbody tr:not(.floor-row) td {
    padding: 3px 5px !important;
    font-size: 8pt !important;
    border: 1px solid #000 !important;
    line-height: 1.3;
  }

  .name-col {
    text-align: left;
  }

  .person-name {
    font-weight: 600;
  }

  .person-designation {
    font-weight: normal;
    color: #555;
    font-size: 7pt !important;
  }

  .ext-col { 
    font-weight: bold; 
    text-align: center;
    font-size: 8pt !important;
    width: 60px;
  }

  /* Footer */
  .sheet-footer {
    border-top: 2px solid #000;
    padding: 0 !important;
    font-size: 7pt !important;
    text-align: center;
    clear: both;
    margin-top: 5px;
    border: 1px solid #000;
  }

  .footer-header {
    background: #e9ecef !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    font-weight: bold;
    padding: 3px !important;
    border-bottom: 1px solid #000;
    font-size: 8pt !important;
  }

  .footer-note {
    margin: 0 !important;
    padding: 2px !important;
    border-bottom: 1px solid #000;
  }
  .footer-note:last-child {
    border-bottom: none;
  }
}
</style>


