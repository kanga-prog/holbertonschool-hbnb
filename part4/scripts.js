document.addEventListener('DOMContentLoaded', () => {
    const places = [
        { id: 1, name: 'Place 1', price: 100, description: 'Description of Place 1' },
        { id: 2, name: 'Place 2', price: 200, description: 'Description of Place 2' },
        { id: 3, name: 'Place 3', price: 150, description: 'Description of Place 3' },
    ];

    const priceFilter = document.getElementById('price-filter');
    const placesList = document.getElementById('places-list');

    // Populate the price filter
    for (let i = 50; i <= 200; i += 50) {
        let option = document.createElement('option');
        option.value = i;
        option.textContent = `$${i}`;
        priceFilter.appendChild(option);
    }

    // Populate the places list
    places.forEach(place => {
        let card = document.createElement('div');
        card.classList.add('place-card');
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p>Price: $${place.price}/night</p>
            <button class="details-button">View Details</button>
        `;
        placesList.appendChild(card);
    });

    // Example of adding more dynamic functionality here as needed
});
