import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () => {
    const announcements = ref([])
    const intercom = ref([])
    const events = ref([])
    const bookings = ref([])
    const emailGroups = ref([])

    // Base URL is relative
    const API_BASE = '/api'

    async function fetchAll() {
        await Promise.all([
            fetchAnnouncements(),
            fetchIntercom(),
            fetchEvents(),
            fetchBookings()
        ])
    }

    async function fetchAnnouncements() {
        try {
            const res = await fetch(`${API_BASE}/announcements`)
            announcements.value = await res.json()
        } catch (e) {
            console.error('Failed to fetch announcements', e)
        }
    }

    async function fetchIntercom() {
        try {
            const res = await fetch(`${API_BASE}/intercom`)
            intercom.value = await res.json()
        } catch (e) { console.error(e) }
    }

    async function fetchEvents() {
        try {
            const res = await fetch(`${API_BASE}/events`)
            events.value = await res.json()
        } catch (e) { console.error(e) }
    }

    async function fetchBookings() {
        try {
            const res = await fetch(`${API_BASE}/bookings`)
            bookings.value = await res.json()
        } catch (e) { console.error(e) }
    }

    async function fetchEmailGroups() {
        try {
            const res = await fetch(`${API_BASE}/email-groups`)
            emailGroups.value = await res.json()
        } catch (e) { console.error(e) }
    }

    // Admin Actions
    async function saveData(endpoint, data) {
        try {
            await fetch(`${API_BASE}/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            // Refresh local
            // In a real app we might optimize this, but for json files just reload
            if (endpoint === 'announcements') await fetchAnnouncements()
            if (endpoint === 'intercom') await fetchIntercom()
            if (endpoint === 'events') await fetchEvents()
            if (endpoint === 'bookings') await fetchBookings()
            if (endpoint === 'email-groups') await fetchEmailGroups()
            return true
        } catch (e) {
            console.error(e)
            return false
        }
    }

    return {
        announcements, intercom, events, bookings, emailGroups,
        fetchAll, saveData, fetchEmailGroups
    }
})
