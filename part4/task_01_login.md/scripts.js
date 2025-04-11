document.addEventListener('DOMContentLoaded', () => {
    // ======= LOGIN FORM =======
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }

            const response = await fetch('http://localhost:5000/login', {  // Change the URL if needed
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/`;  // Store the JWT token in a cookie
                window.location.href = 'index.html';  // Redirect to the main page
            } else {
                alert('Login failed: ' + response.statusText);
            }
        });
    }

    // ======= ADDING REVIEW =======
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const token = document.cookie.split(';').find(cookie => cookie.trim().startsWith('token='));

            if (!token) {
                alert('You must be logged in to leave a review.');
                return;
            }

            // Logic for submitting a review goes here
        });
    }

    // ======= OTHER PAGES LOGIC (INDEX, PLACE, ADD REVIEW) =======
    // Add more functionality for rendering the places, reviews, etc. as needed.
});

