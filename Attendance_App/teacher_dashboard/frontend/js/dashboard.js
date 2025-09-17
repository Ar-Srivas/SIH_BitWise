document.addEventListener("DOMContentLoaded", () => {
    // 1. Check if user is logged in, redirect if not
    const teacherId = sessionStorage.getItem('teacherId');
    if (!teacherId) {
        window.location.href = '/'; // Redirect to login
        return;
    }

    // 2. Get references to HTML elements
    const dateList = document.getElementById('date-list');
    const welcomeMessage = document.getElementById('welcome-message');
    const attendanceDetails = document.getElementById('attendance-details');
    const logoutBtn = document.getElementById('logout-btn');

    /**
     * Fetches the list of session dates from the API and populates the sidebar.
     */
    async function loadDates() {
        try {
            const response = await fetch(`/api/dates?teacher_id=${teacherId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch dates.');
            }
            const dates = await response.json();

            dateList.innerHTML = ''; // Clear the "Loading..." message
            if (dates && dates.length > 0) {
                dates.forEach(date => {
                    const link = document.createElement('a');
                    link.href = '#';
                    link.textContent = date;
                    // Add click event listener to load data for the selected date
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        loadDashboardForDate(date);
                    });
                    dateList.appendChild(link);
                });
            } else {
                dateList.innerHTML = '<p>No session records found.</p>';
            }
        } catch (error) {
            console.error("Error loading dates:", error);
            dateList.innerHTML = '<p>Error loading dates.</p>';
        }
    }

    /**
     * Fetches and displays the attendance data for a specific date.
     * @param {string} date - The date in YYYY-MM-DD format.
     */
    async function loadDashboardForDate(date) {
        try {
            welcomeMessage.style.display = 'none'; // Hide initial welcome message
            attendanceDetails.innerHTML = `<p>Loading records for ${date}...</p>`;

            const response = await fetch(`/api/dashboard?teacher_id=${teacherId}&date=${date}`);
            if (!response.ok) {
                throw new Error('Failed to fetch dashboard data.');
            }
            const data = await response.json();
            const students = data.students || {};

            // Build the HTML table with student data
            let tableHtml = `
                <h2>Attendance for ${date}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Name</th>
                            <th>Status</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            for (const studentId in students) {
                const student = students[studentId];
                const statusClass = student.status === 'present' ? 'status-present' : 'status-absent';
                tableHtml += `
                    <tr>
                        <td>${studentId}</td>
                        <td>${student.name}</td>
                        <td class="${statusClass}">${student.status}</td>
                        <td>${student.timestamp || 'N/A'}</td>
                    </tr>
                `;
            }
            tableHtml += '</tbody></table>';
            attendanceDetails.innerHTML = tableHtml;

        } catch (error) {
            console.error(`Error loading dashboard for ${date}:`, error);
            attendanceDetails.innerHTML = `<p>Error loading data for ${date}.</p>`;
        }
    }

    // Logout functionality
    logoutBtn.addEventListener('click', () => {
        sessionStorage.removeItem('teacherId');
        window.location.href = '/';
    });

    // Initial load of dates when the page is ready
    loadDates();
});
