let userEmail = '';

        document.addEventListener('DOMContentLoaded', function() {
            // Get email from URL
            const urlParams = new URLSearchParams(window.location.search);
            userEmail = urlParams.get('email');

            if (!userEmail) {
                location.href = '/';
                return;
            }

            // Load profile data
            loadProfile();
        });

        function loadProfile() {
            fetch(`/api/profile?email=${userEmail}`)
                .then(response => response.json())
                .then(data => {
                    const profileContent = document.getElementById('profile-content');

                    let quizResultsHtml = '';
                    if (data.quiz_results && Object.keys(data.quiz_results).length > 0) {
                        quizResultsHtml = Object.entries(data.quiz_results)
                            .map(([category, count]) => `<p><strong>${category}:</strong> ${count}</p>`)
                            .join('');
                    } else {
                        quizResultsHtml = '<p>No quiz results yet</p>';
                    }

                    profileContent.innerHTML = `
                        <div class="profile-info">
                            <div class="profile-field">
                                <p><strong>Name:</strong> ${data.name}</p>
                            </div>
                            <div class="profile-field">
                                <p><strong>Email:</strong> ${data.email}</p>
                            </div>
                            <div class="profile-field">
                                <h3>Quiz Results Summary</h3>
                                <div class="profile-results">
                                    ${quizResultsHtml}
                                </div>
                            </div>
                        </div>
                    `;
                })
                .catch(error => {
                    console.error('Error loading profile:', error);
                    document.getElementById('profile-content').innerHTML =
                        '<p class="error">Failed to load profile. Please try again later.</p>';
                });
        }

        function goBackToDashboard() {
            location.href = `/dashboard?email=${userEmail}`;
        }