
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
















