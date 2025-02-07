
// window.onload = function() {
//     // Check if a scroll position is saved in localStorage and directly scroll to it
//     if (localStorage.getItem('scrollPosition')) {
//         window.scrollTo(0, parseInt(localStorage.getItem('scrollPosition')));
//     }

//     // Save the scroll position when any like button is clicked
//     document.querySelectorAll('.like-button').forEach(button => {
//         button.addEventListener('click', function() {
//             localStorage.setItem('scrollPosition', window.scrollY);
//         });
//     });

//     // Optional: Save scroll position for specific action buttons
//     document.querySelector('#your-action-button').addEventListener('click', function() {
//         localStorage.setItem('scrollPosition', window.scrollY);
//     });

//     setTimeout(function() {
//         localStorage.removeItem('scrollPosition');
//     }, 1000); 
// };


window.onload = function() {
    // Check if a scroll position is saved in localStorage and directly scroll to it
    if (localStorage.getItem('scrollPosition')) {
        window.scrollTo(0, parseInt(localStorage.getItem('scrollPosition')));
    }

    // Save the scroll position when any like button is clicked
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            // Save the current scroll position to localStorage before the page reloads/redirects
            localStorage.setItem('scrollPosition', window.scrollY);
        });
    });

    // Optionally: Save scroll position for specific action buttons (if you have other actions)
    document.querySelector('#your-action-button')?.addEventListener('click', function() {
        localStorage.setItem('scrollPosition', window.scrollY);
    });

    // Remove scroll position from localStorage after a redirect (to avoid restoring it unnecessarily)
    const navigationEntries = window.performance.getEntriesByType('navigation');
    if (navigationEntries.length > 0 && navigationEntries[0].type === 'reload') {
        // If the page load is a reload (not a normal page load), remove the scroll position
        localStorage.removeItem('scrollPosition');
    }
};


















document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star");
    const hiddenRatingInput = document.getElementById("dish-rating");
    const currentRatingText = document.getElementById("current-rating");

    stars.forEach(star => {
        star.addEventListener("click", function() {
            // Get the rating value (1 to 5)
            const ratingValue = this.getAttribute("data-value");

            // Set the rating value in the hidden input field
            hiddenRatingInput.value = ratingValue;

            // Update the displayed current rating text
            currentRatingText.textContent = `${ratingValue} out of 5`;

            // Highlight the stars based on the rating
            updateStarColors(ratingValue);
            
            // Optionally, you can send the rating to the server here via AJAX or form submission
            // Example:
            // sendRatingToServer(ratingValue);
        });
    });

    // Function to update the star colors based on the rating
    function updateStarColors(ratingValue) {
        stars.forEach(star => {
            if (parseInt(star.getAttribute("data-value")) <= ratingValue) {
                star.style.color = "gold"; // Highlight selected stars
            } else {
                star.style.color = "gray"; // Unselected stars
            }
        });
    }
});


// function sendRatingToServer(ratingValue) {
//     const dishId = {{ i.pk }}; // Replace this with the actual dish ID
//     const userId = {{ user.id }}; // Replace with the user ID if applicable

//     fetch('/submitRating/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             dishId: dishId,
//             userId: userId,
//             rating: ratingValue,
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log("Rating submitted successfully:", data);
//     })
//     .catch(error => {
//         console.error("Error submitting rating:", error);
//     });
// }
