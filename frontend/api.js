// API Base URL
const API_URL = 'http://127.0.0.1:8000/api';

// Global data storage
let allSchedules = [];
let allRoutineInfos = [];
let allRooms = [];
let allDepartments = [];
let allCourses = [];
let allTeachers = [];

// Page load হলে data fetch করা
document.addEventListener('DOMContentLoaded', function() {
    loadAllData();
});

// সব data একসাথে load করা
// সব data একসাথে load করা
async function loadAllData() {
    try {
        const [schedules, routineInfos, rooms, departments, courses, teachers] = await Promise.all([
            fetch(`${API_URL}/schedules/`).then(res => res.json()),
            fetch(`${API_URL}/routines/`).then(res => res.json()),
            fetch(`${API_URL}/rooms/`).then(res => res.json()),
            fetch(`${API_URL}/departments/`).then(res => res.json()),
            fetch(`${API_URL}/courses/`).then(res => res.json()),
            fetch(`${API_URL}/teachers/`).then(res => res.json())
        ]);

        allSchedules = schedules;
        allRoutineInfos = routineInfos;
        allRooms = rooms;
        allDepartments = departments;
        allCourses = courses;
        allTeachers = teachers;

        console.log('✅ Data loaded successfully!');
        
        // ==========================================
        //  NEW CODE: Populate Department Dropdown
        // ==========================================
        const deptDropdown = document.getElementById('department');
        if (deptDropdown) {
            allDepartments.forEach(dept => {
                const option = document.createElement('option');
                option.value = dept.id;
                option.textContent = dept.name;
                deptDropdown.appendChild(option);
            });
        }
        
        // If on routine_view page, load routine
        if (window.location.pathname.includes('routine_view')) {
            loadRoutineView();
        }
        
    } catch (error) {
        console.error('❌ Error loading data:', error);
    }
}
// Load routine for view page
// Load routine for view page
function loadRoutineView() {
    // Get selected values from session storage
    const deptId = sessionStorage.getItem('selectedDept'); // নতুন যোগ করা হয়েছে
    const level = sessionStorage.getItem('selectedLevel') || '2';
    const term = sessionStorage.getItem('selectedTerm') || 'II';
    const section = sessionStorage.getItem('selectedSection') || 'B';
    
    const levelTerm = `${level}-${term}`;
    
    console.log('🔍 Looking for:', 'Dept ID:', deptId, 'Level-Term:', levelTerm, 'Section:', section);
    
    // Find routine info that matches all criteria
    const routineInfo = allRoutineInfos.find(r => 
        r.department == deptId && // department ID দিয়ে check
        r.level_term === levelTerm && 
        r.section === section
    );
    
    if (routineInfo) {
        console.log('✅ Found Routine Info:', routineInfo);
        const filtered = allSchedules.filter(s => s.routine === routineInfo.id);
        console.log('📅 Found schedules:', filtered.length);
        
        if (typeof displayScheduleTable === 'function') {
            displayScheduleTable(filtered);
        }
    } else {
        console.log('⚠️ No routine info found for this selection.');
        if (typeof displayNoData === 'function') {
            displayNoData();
        }
    }
}

// Room Search Function
window.searchRooms = function() {
    const day = document.getElementById('day').value;
    const timeSlot = document.getElementById('time').value;
    const resultsDiv = document.getElementById('room-results');
    const resultTitle = document.getElementById('result-title');
    
    if (!day || !timeSlot) {
        showAlert('Please select both day and time slot');
        return;
    }
    
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner"></span> Searching...';
    button.disabled = true;
    
    setTimeout(() => {
        // Extract hour from time slot
        const [startTime] = timeSlot.split('-');
        const searchHour = startTime.split(':')[0];
        
        // Find occupied rooms
        const occupiedRoomIds = allSchedules
            .filter(schedule => {
                if (schedule.day_of_week !== day) return false;
                
                const scheduleHour = schedule.start_time.split(':')[0];
                return scheduleHour === searchHour;
            })
            .map(schedule => schedule.room);

        // Find available rooms
        const availableRooms = allRooms.filter(room => 
            !occupiedRoomIds.includes(room.id)
        );

        // Display results
        displayAvailableRooms(availableRooms, day, timeSlot);
        
        resultTitle.textContent = `Available Rooms for ${day}, ${timeSlot}`;
        resultsDiv.style.display = 'block';
        button.innerHTML = originalText;
        button.disabled = false;
        
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 1000);
}

// Display available rooms
function displayAvailableRooms(rooms, day, time) {
    const tbody = document.querySelector('#room-results tbody');
    
    if (rooms.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center; padding: 30px;">
                    <i class="fas fa-info-circle" style="font-size: 2rem; color: #fc00ff; margin-bottom: 10px;"></i>
                    <p>No available rooms for this time slot</p>
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = rooms.map(room => `
        <tr>
            <td>${room.room_number}</td>
            <td>${room.capacity} Students</td>
            <td>${room.room_type}</td>
            <td><span style="color: #43e97b;">✓ Available</span></td>
        </tr>
    `).join('');
}

// Form Submit Handler
// Form Submit Handler
const routineForm = document.getElementById('routine-form');
if (routineForm) {
    routineForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const departmentId = document.getElementById('department').value; // নতুন যোগ করা হয়েছে
        const level = document.getElementById('level').value;
        const term = document.getElementById('term').value;
        const section = document.getElementById('section').value;

        if (!departmentId) { // Validation
            alert('Please select a department.');
            return;
        }
        
        const button = this.querySelector('button[type="submit"]');
        const originalText = button.innerHTML;
        
        button.innerHTML = '<span class="spinner"></span> Loading...';
        button.disabled = true;
        
        const termRoman = term === '1' ? 'I' : 'II';
        
        // Store in session storage
        sessionStorage.setItem('selectedDept', departmentId); // নতুন যোগ করা হয়েছে
        sessionStorage.setItem('selectedLevel', level);
        sessionStorage.setItem('selectedTerm', termRoman);
        sessionStorage.setItem('selectedSection', section);
        
        setTimeout(() => {
            window.location.href = 'routine_view.html';
        }, 500);
    });
}

// Show Alert Function
function showAlert(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert-custom';
    alertDiv.innerHTML = `<i class="fas fa-exclamation-circle" style="margin-right: 10px;"></i> ${message}`;
    
    const card = event.target.closest('.glass-card');
    if (card) {
        card.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}

// Toggle Dropdown
function toggleDropdown(dropdownId, button) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle('show');
    button.classList.toggle('active');
}

// Activate Search
function activateSearch(event) {
    event.preventDefault();
    const daySelect = document.getElementById('day');
    if (daySelect) {
        daySelect.focus();
        daySelect.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

console.log('🚀 BAUST Routine System Loaded!');