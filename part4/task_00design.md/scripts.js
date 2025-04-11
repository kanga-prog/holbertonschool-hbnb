document.addEventListener('DOMContentLoaded', () => {
    const places = [
        { id: 1, name: 'Beautiful Beach House', price: 100, description: 'Nice place with a view.', host: 'Alice', amenities: ['WiFi', 'Parking'] },
        { id: 2, name: 'Cozy Cabin', price: 200, description: 'Luxurious spot downtown.', host: 'Bob', amenities: ['Pool', 'WiFi'] },
        { id: 3, name: 'Modern Apartment', price: 150, description: 'Cozy and affordable.', host: 'Charlie', amenities: ['Breakfast', 'WiFi'] },
    ];

    const reviews = {
        1: [
            { user: 'wilfried pano', comment: 'Great stay!', rating: 5 },
            { user: 'kanga kouakou brice', comment: 'Pretty good.', rating: 4 }
        ],
        2: [
            { user: 'Nordine', comment: 'Loved it!', rating: 5 }
        ],
        3: [
            {user : 'tchong et Arthur', comment : 'is very beautiful space.' , rating : 4}
        ]
    };

    // Helper: Get URL params
    function getParam(name) {
        const url = new URL(window.location.href);
        return url.searchParams.get(name);
    }

    // ========== INDEX PAGE ==========
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter && placesList) {
        // Populate filter
        for (let i = 50; i <= 300; i += 50) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `$${i}`;
            priceFilter.appendChild(option);
        }

        // Render places
        function renderPlaces(maxPrice = null) {
            placesList.innerHTML = '';
            let filteredPlaces = maxPrice ? places.filter(p => p.price <= maxPrice) : places;

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

            // Add event listeners to "View Details" buttons
            document.querySelectorAll('.details-button').forEach(button => {
                button.addEventListener('click', () => {
                    const placeId = button.getAttribute('data-id');
                    window.location.href = `place.html?id=${placeId}`;
                });
            });
        }

        renderPlaces();

        // Filtering logic
        priceFilter.addEventListener('change', () => {
            const maxPrice = parseInt(priceFilter.value);
            renderPlaces(maxPrice);
        });
    }

    // ========== PLACE DETAILS PAGE ==========
    const placeDetailsSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');
    const reviewForm = document.getElementById('review-form');

    if (placeDetailsSection && reviewsSection) {
        const placeId = parseInt(getParam('id'));
        const place = places.find(p => p.id === placeId);

        if (place) {
            // Show place details
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

            // Show reviews
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
                        <p>Rating: ${review.rating}/5</p>
                    `;
                    reviewsSection.appendChild(reviewCard);
                });
            }
        }
    }

    // ========== ADD REVIEW PAGE ==========
    const addReviewButton = document.querySelector('.submit-review-button');
    if (addReviewButton && document.getElementById('place-id')) {
        addReviewButton.addEventListener('click', () => {
            const placeIdInput = document.getElementById('place-id').value.trim();
            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (placeIdInput && reviewText && rating) {
                alert(`Review submitted for place ID ${placeIdInput}:\n"${reviewText}" with rating ${rating}`);
                // You would normally send this to a server here.
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // ========== LOGIN PAGE ==========
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            if (email && password) {
                // Simulated login
                localStorage.setItem('user', JSON.stringify({ email }));
                alert(`Welcome, ${email}!`);
                window.location.href = 'index.html';
            } else {
                alert('Please enter email and password.');
            }
        });
    }

    // ========== REVIEW FORM ON place.html ==========
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const user = JSON.parse(localStorage.getItem('user'));
            if (!user) {
                alert('You must be logged in to leave a review.');
                return;
            }
            const text = document.getElementById('review-text').value.trim();
            if (text) {
                alert(`Thanks for your review: "${text}"`);
                // Normally you would send this to a server here
                document.getElementById('review-text').value = '';
            }
        });
    }
});
