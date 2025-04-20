document.addEventListener('DOMContentLoaded', () => {

    // ========== [0] MOCK DE DONNÉES PAR DÉFAUT ==========
    const defaultPlaces = [
        { id: 1, name: 'Beautiful Beach House', price: 100, description: 'Nice place with a view.', host: 'Alice', amenities: ['WiFi', 'Parking'] },
        { id: 2, name: 'Cozy Cabin', price: 200, description: 'Luxurious spot downtown.', host: 'Bob', amenities: ['Pool', 'WiFi'] },
        { id: 3, name: 'Modern Apartment', price: 150, description: 'Cozy and affordable.', host: 'Charlie', amenities: ['Breakfast', 'WiFi'] },
    ];

    // ========== [1] OUTILS UTILITAIRES ==========

    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    function getParam(paramName) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(paramName);
    }

    // ========== [2] AUTHENTIFICATION ==========
    
    const loginLink = document.getElementById('login-link');

    function checkAuthentication() {
        const token = getCookie('token');
        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
            renderPlaces(); // fallback local
        } else {
            if (loginLink) loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    // ========== [3] PAGE D'ACCUEIL : INDEX ==========

    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://localhost:5000/api/places', {
                headers: { Authorization: `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Échec récupération places');
            const places = await response.json();
            renderPlaces(null, places);
        } catch (error) {
            console.error('Erreur de récupération des places :', error);
        }
    }

    function renderPlaces(maxPrice = null, placeData = null) {
        if (!placesList) return;
        placesList.innerHTML = '';
        const data = placeData || defaultPlaces;
        const filtered = maxPrice ? data.filter(p => p.price <= maxPrice) : data;

        filtered.forEach(place => {
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

        document.querySelectorAll('.details-button').forEach(button => {
            button.addEventListener('click', () => {
                const placeId = button.getAttribute('data-id');
                window.location.href = `place.html?id=${placeId}`;
            });
        });
    }

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

    // ========== [4] PAGE DETAILS D'UN PLACE ==========

    const placeDetailsSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');
    const token = getCookie('token');

    if (placeDetailsSection && reviewsSection) {
        const placeId = parseInt(getParam('id'));

        // Infos du lieu
        fetch(`http://localhost:5000/api/places/${placeId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => {
            if (!res.ok) throw new Error('Failed to load place details');
            return res.json();
        })
        .then(place => {
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

            const reviewForm = document.getElementById('review-form');
            if (reviewForm && !document.getElementById('place-id')) {
                const hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.id = 'place-id';
                hidden.value = placeId;
                reviewForm.appendChild(hidden);
            }
        })
        .catch(err => {
            placeDetailsSection.innerHTML = `<p>Error loading place details: ${err.message}</p>`;
        });

        // Avis
        fetch(`http://localhost:5000/api/places/${placeId}/reviews`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        .then(res => {
            if (!res.ok) throw new Error('Failed to load reviews');
            return res.json();
        })
        .then(reviews => {
            reviewsSection.innerHTML = '<h3>Reviews</h3>';
            if (reviews.length === 0) {
                reviewsSection.innerHTML += '<p>No reviews yet.</p>';
            } else {
                reviews.forEach(review => {
                    const card = document.createElement('div');
                    card.className = 'review-card';
                    card.innerHTML = `
                        <p><strong>${review.user}</strong></p>
                        <p>${review.comment}</p>
                        <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                    `;
                    reviewsSection.appendChild(card);
                });
            }
        })
        .catch(err => {
            reviewsSection.innerHTML = `<p>Error loading reviews: ${err.message}</p>`;
        });
    }

    // ========== [5] FORMULAIRE D'AJOUT D'AVIS ==========

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const placeId = parseInt(document.getElementById('place-id')?.value);
            const reviewText = document.getElementById('review-text')?.value.trim();
            const rating = parseInt(document.getElementById('rating')?.value);
            const user = JSON.parse(localStorage.getItem('user'));
            const token = getCookie('token');

            if (!placeId || !reviewText || !rating) {
                alert('Please fill in all fields.');
                return;
            }

            if (!user) {
                alert('You must be logged in to leave a review.');
                return;
            }

            try {
                const res = await fetch(`http://localhost:5000/api/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify({ comment: reviewText, rating })
                });

                if (!res.ok) {
                    const err = await res.json();
                    alert('Failed to submit review: ' + (err.msg || res.statusText));
                    return;
                }

                alert(`Thanks, ${user.email}, for your review!`);
                document.getElementById('review-text').value = '';
                document.getElementById('rating').value = '';
                window.location.reload();

            } catch (error) {
                console.error('Error submitting review:', error);
                alert('An error occurred while submitting your review.');
            }
        });
    }

    // ========== [6] FORMULAIRE LOGIN ==========
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                alert('Please enter email and password.');
                return;
            }

            try {
                const res = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (!res.ok) {
                    const err = await res.json();
                    alert('Login failed: ' + (err.msg || res.statusText));
                    return;
                }

                const data = await res.json();
                document.cookie = `token=${encodeURIComponent(data.access_token)}; path=/`;
                alert(`Welcome, ${email}!`);
                window.location.href = 'index.html';

            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login.');
            }

            document.getElementById('password').value = '';
        });
    }

    // ========== [7] FORMULAIRE REGISTER ==========

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
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
                const res = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await res.json();
                if (!res.ok) {
                    alert(data.msg || 'Registration failed.');
                    return;
                }

                alert('Registration successful! You can now login.');
                window.location.href = 'login.html';

            } catch (error) {
                console.error('Registration error:', error);
                alert('An error occurred during registration.');
            }

            document.getElementById('password').value = '';
        });
    }

    // ========== [8] INITIALISATION ==========
    checkAuthentication();
});
// ========== [9] FORMULAIRE ADD_REVIEW.HTML ==========
const addReviewForm = document.getElementById('review-form');
if (addReviewForm && window.location.pathname.includes('add_review.html')) {
    addReviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const token = getCookie('token');
        const user = JSON.parse(localStorage.getItem('user'));
        const placeId = parseInt(document.getElementById('place-id')?.value);
        const review = document.getElementById('review')?.value.trim();
        const rating = parseInt(document.getElementById('rating')?.value);

        if (!user || !token) {
            alert("Vous devez être connecté pour laisser un avis.");
            return;
        }

        if (!placeId || !review || !rating) {
            alert("Veuillez remplir tous les champs.");
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/api/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ comment: review, rating })
            });

            const result = await response.json();

            if (!response.ok) {
                alert("Erreur: " + (result.msg || response.statusText));
                return;
            }

            alert(`Merci pour votre avis sur le lieu ${placeId} !`);
            window.location.href = `place.html?id=${placeId}`;

        } catch (err) {
            console.error("Erreur lors de l'envoi de l'avis:", err);
            alert("Une erreur s'est produite.");
        }
    });
}
