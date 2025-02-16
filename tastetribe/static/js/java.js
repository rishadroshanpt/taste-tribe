








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
    
    












    // Get all buttons with class 'toggle-button'
    document.addEventListener("DOMContentLoaded", function() {
        // Get all buttons with class 'toggle-button'
        const buttons = document.querySelectorAll('.toggle-button');
        
        // Function to check screen size and toggle content visibility
        function toggleVisibility() {
            // Only execute the toggle behavior if screen size is less than 500px
            if (window.innerWidth < 500) {
                buttons.forEach(button => {
                    button.addEventListener('click', function() {
                        // Get the target section (either "dishes" or "users")
                        const target = this.getAttribute('data-target');
                        
                        // Hide both sections
                        document.getElementById('dishes').style.display = 'none';
                        document.getElementById('users').style.display = 'none';
                        
                        // Show the clicked target section
                        document.getElementById(target).style.display = 'block';
                    });
                });
            } else {
                // If the screen width is greater than or equal to 500px, make sure both sections are visible
                document.getElementById('dishes').style.display = 'block';
                document.getElementById('users').style.display = 'block';
                // Remove event listeners to avoid unnecessary toggling
                buttons.forEach(button => {
                    button.removeEventListener('click', toggleVisibility);
                });
            }
        }
    
        // Check on page load
        toggleVisibility();
        
        // Check whenever the window is resized
        window.addEventListener('resize', toggleVisibility);
    });
    





