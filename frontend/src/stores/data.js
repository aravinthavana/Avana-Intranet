import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () =>{
    const announcements = ref([])
    const intercom = ref([])
    const events = ref([])
    const bookings = ref([])
    const emailGroups = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Base URL is relative
    const API_BASE = '/api'

    /**
     * Get authentication token from localStorage
     */
    function getAuthToken() {
        return localStorage.getItem('admin_token')
    }

    /**
     * Get headers for authenticated requests
     */
    function getAuthHeaders() {
        const token = getAuthToken()
        const headers = {
            'Content-Type': 'application/json'
        }
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`
        }
        
        return headers
    }

    /**
     * Handle API errors with proper status code checking
     */
    async function handleResponse(response) {
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            const errorMessage = errorData.error || errorData.message || `HTTP ${response.status}`
            
            // Handle authentication errors
            if (response.status === 401) {
                localStorage.removeItem('admin_token')
                throw new Error('Authentication required. Please log in again.')
            }
            
            throw new Error(errorMessage)
        }
        
        return response.json()
    }

    /**
     * Fetch all public data
     */
    async function fetchAll() {
        loading.value = true
        error.value = null
        
        try {
            await Promise.all([
                fetchAnnouncements(),
                fetchIntercom(),
                fetchEvents(),
                fetchBookings()
            ])
        } catch (e) {
            error.value = e.message
            console.error('Failed to fetch data:', e)
        } finally {
            loading.value = false
        }
    }

    async function fetchAnnouncements() {
        try {
            const res = await fetch(`${API_BASE}/announcements`)
            announcements.value = await handleResponse(res)
        } catch (e) {
            console.error('Failed to fetch announcements:', e)
            throw e
        }
    }

    async function fetchIntercom() {
        try {
            const res = await fetch(`${API_BASE}/intercom`)
            intercom.value = await handleResponse(res)
        } catch (e) {
            console.error('Failed to fetch intercom:', e)
            throw e
        }
    }

    async function fetchEvents() {
        try {
            const res = await fetch(`${API_BASE}/events`)
            events.value = await handleResponse(res)
        } catch (e) {
            console.error('Failed to fetch events:', e)
            throw e
        }
    }

    async function fetchBookings() {
        try {
            const res = await fetch(`${API_BASE}/bookings`)
            bookings.value = await handleResponse(res)
        } catch (e) {
            console.error('Failed to fetch bookings:', e)
            throw e
        }
    }

    async function fetchEmailGroups() {
        try {
            const res = await fetch(`${API_BASE}/email-groups`)
            emailGroups.value = await handleResponse(res)
        } catch (e) {
            console.error('Failed to fetch email groups:', e)
            throw e
        }
    }

    /**
     * Save data to API (requires authentication)
     */
    async function saveData(endpoint, data) {
        loading.value = true
        error.value = null
        
        try {
            const res = await fetch(`${API_BASE}/${endpoint}`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(data)
            })
            
            await handleResponse(res)
            
            // Refresh local data
            if (endpoint === 'announcements') await fetchAnnouncements()
            if (endpoint === 'intercom') await fetchIntercom()
            if (endpoint === 'events') await fetchEvents()
            if (endpoint === 'bookings') await fetchBookings()
            if (endpoint === 'email-groups') await fetchEmailGroups()
            
            return true
        } catch (e) {
            error.value = e.message
            console.error('Failed to save data:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Login and get JWT token
     */
    async function login(password) {
        loading.value = true
        error.value = null
        
        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            })
            
            const data = await handleResponse(res)
            
            if (data.token) {
                localStorage.setItem('admin_token', data.token)
                return true
            }
            
            return false
        } catch (e) {
            error.value = e.message
            console.error('Login failed:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Logout and clear token
     */
    function logout() {
        localStorage.removeItem('admin_token')
    }

    /**
     * Check if user is authenticated
     */
    function isAuthenticated() {
        return !!getAuthToken()
    }

    return {
        // State
        announcements,
        intercom,
        events,
        bookings,
        emailGroups,
        loading,
        error,
        
        // Methods
        fetchAll,
        fetchAnnouncements,
        fetchIntercom,
        fetchEvents,
        fetchBookings,
        fetchEmailGroups,
        saveData,
        login,
        logout,
        isAuthenticated
    }
})
