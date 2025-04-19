document.addEventListener('DOMContentLoaded', () => {
    const defaultPlaces = [
        { id: 1, name: 'Beautiful Beach House', price: 100, description: 'Nice place with a view.', host: 'Alice', amenities: ['WiFi', 'Parking'] },
        { id: 2, name: 'Cozy Cabin', price: 200, description: 'Luxurious spot downtown.', host: 'Bob', amenities: ['Pool', 'WiFi'] },
        { id: 3, name: 'Modern Apartment', price: 150, description: 'Cozy and affordable.', host: 'Charlie', amenities: ['Breakfast', 'WiFi'] },
    ];

    // ========== INDEX PAGE ==========

    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    const loginLink = document.getElementById('login-link');

    // Récupération du cookie
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // Vérification de l'authentification et récupération des places
    function checkAuthentication() {
        const token = getCookie('token');
        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
            renderPlaces(); // fallback avec données mock
        } else {
            if (loginLink) loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    // Appel API pour récupérer les places
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://localhost:5000/api/places', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            if (!response.ok) throw new Error('Échec récupération places');
            const places = await response.json();
            renderPlaces(null, places);
        } catch (error) {
            console.error('Erreur de récupération des places :', error);
        }
    }

    // Fonction pour afficher les places (avec ou sans filtre)
    function renderPlaces(maxPrice = null, placeData = null) {
        placesList.innerHTML = '';
        const data = placeData || defaultPlaces;
        const filteredPlaces = maxPrice ? data.filter(p => p.price <= maxPrice) : data;

        filteredPlaces.forEach(place => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.innerHTML = `
                <h3>${place.name}</h3>
                <p>${place.description}</p>
                <p>Price: $${place.price}/night</p>
                <button class="details-button" data-id="${place.id}">View Details</button>
            `;
            placesList.appendChild(card);
        });

        // Redirection vers la page de détails
        document.querySelectorAll('.details-button').forEach(button => {
            button.addEventListener('click', () => {
                const placeId = button.getAttribute('data-id');
                window.location.href = `place.html?id=${placeId}`;
            });
        });
    }

    // Filtrage des places par prix
    if (priceFilter && placesList) {
        for (let i = 50; i <= 300; i += 50) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `$${i}`;
            priceFilter.appendChild(option);
        }

        priceFilter.addEventListener('change', () => {
            const maxPrice = parseInt(priceFilter.value);
            renderPlaces(maxPrice);
        });
    }

    // ========== PLACE DETAILS ==========

    const placeDetailsSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');

    if (placeDetailsSection && reviewsSection) {
        const placeId = parseInt(getParam('id'));
        const place = defaultPlaces.find(p => p.id === placeId);

        if (place) {
            placeDetailsSection.innerHTML = `
                <div class="place-details">
                    <h2>${place.name}</h2>
                    <div class="place-info">
                        <p><strong>Host:</strong> ${place.host}</p>
                        <p><strong>Price:</strong> $${place.price}/night</p>
                        <p><strong>Description:</strong> ${place.description}</p>
                        <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
                    </div>
                </div>
            `;

            const placeReviews = reviews[placeId] || [];
            reviewsSection.innerHTML = '<h3>Reviews</h3>';
            if (placeReviews.length === 0) {
                reviewsSection.innerHTML += `<p>No reviews yet.</p>`;
            } else {
                placeReviews.forEach(review => {
                    const reviewCard = document.createElement('div');
                    reviewCard.className = 'review-card';
                    reviewCard.innerHTML = `
                        <p><strong>${review.user}</strong></p>
                        <p>${review.comment}</p>
                        <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                    `;
                    reviewsSection.appendChild(reviewCard);
                });
            }
        }
    }

    // ========== ADD REVIEW ==========

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const placeId = parseInt(document.getElementById('place-id')?.value.trim());
            const reviewText = document.getElementById('review-text')?.value.trim();
            const rating = document.getElementById('rating')?.value;

            const placeExists = places.some(p => p.id === placeId);
            const user = JSON.parse(localStorage.getItem('user'));

            if (!placeId || !reviewText || !rating) {
                alert('Please fill in all fields.');
                return;
            }

            if (!placeExists) {
                alert('This place ID does not exist.');
                return;
            }

            if (!user) {
                alert('You must be logged in to leave a review.');
                return;
            }

            alert(`Thanks, ${user.email}, for your review on place ID ${placeId}:
"${reviewText}" with rating ${rating} stars`);
            document.getElementById('review-text').value = '';
            document.getElementById('rating').value = '';
        });
    }

    // ========== LOGIN ==========

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const passwordInput = document.getElementById('password');
            const password = passwordInput.value.trim();

            if (!email || !password) {
                alert('Please enter email and password.');
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (!response.ok) {
                    const error = await response.json();
                    alert('Login failed: ' + (error.msg || response.statusText));
                    return;
                }

                const data = await response.json();
                document.cookie = `token=${encodeURIComponent(data.access_token)}; path=/`;

                alert(`Welcome, ${email}!`);
                window.location.href = 'index.html';

            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login.');
            }

            passwordInput.value = '';
        });
    }

    // ========== REGISTER ==========

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value.trim();
            const passwordInput = document.getElementById('password');
            const password = passwordInput.value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (!email || !password || !confirmPassword) {
                alert('Please fill in all fields.');
                return;
            }

            if (password !== confirmPassword) {
                alert('Passwords do not match.');
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    alert(data.msg || 'Registration failed.');
                    return;
                }

                alert('Registration successful! You can now login.');
                window.location.href = 'login.html';

            } catch (error) {
                console.error('Registration error:', error);
                alert('An error occurred during registration.');
            }

            passwordInput.value = '';
        });
    }

    checkAuthentication();
});
