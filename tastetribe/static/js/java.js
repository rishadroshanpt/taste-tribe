
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







    document.addEventListener("DOMContentLoaded", function () {
        const likeButtons = document.querySelectorAll('.like-button');

        likeButtons.forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault();  // Prevent the default link behavior

                const dishId = this.getAttribute('data-dish-id');  // Get the dish ID
                const likeIcon = document.getElementById(`like-icon-${dishId}`);
                const likeCountSpan = document.getElementById(`like-count-${dishId}`);

                fetch(`/add_like/${dishId}/`, {
                    method: 'GET',  // Use 'POST' for adding/removing likes
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,  // Include CSRF token
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.liked) {
                        likeIcon.classList.remove('fa-regular', 'fa-heart');
                        likeIcon.classList.add('fa-solid', 'fa-heart', 'redheart');
                    } else {
                        likeIcon.classList.remove('fa-solid', 'fa-heart', 'redheart');
                        likeIcon.classList.add('fa-regular', 'fa-heart');
                    }
                    likeCountSpan.textContent = data.likes_count;  // Update the like count
                })
                .catch(error => console.error('Error:', error));
            });
        });
    });












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


    // Attach a click event listener to each button for toggling the visibility
    document.querySelectorAll('.toggleBtn').forEach((button, index) => {
        button.addEventListener('click', function() {
            // Get the corresponding dish details container
            var dishDetails = document.querySelectorAll('.dishDet3')[index];
            
            // Toggle visibility
            if (dishDetails.style.display === 'none' || !dishDetails.style.display) {
                dishDetails.style.display = 'block'; // Show content
                button.textContent = 'See Less';   // Change button text to "Show Less"
            } else {
                dishDetails.style.display = 'none'; // Hide content
                button.textContent = 'See More ...';   // Change button text to "Show More"
            }
        });
    });








    let timeout;

    document.getElementById('searchInput').addEventListener('input', function() {
        clearTimeout(timeout);
    
        const query = this.value;  // Get the value from the search input field
    
        timeout = setTimeout(() => {
            fetch(`/search_dishes/?q=${query}`)
                .then(response => response.text())  // Expecting HTML as response
                .then(html => {
                    const resultsList = document.getElementById('searchResults');  // The container where results will be rendered
                    resultsList.innerHTML = html;  // Replace previous results with the new HTML
                })
                .catch(error => console.error('Error fetching search results:', error));
        }, 300);  // Wait for 300ms after the last input before sending the request
    });
    
    






