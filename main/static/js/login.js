document.addEventListener('DOMContentLoaded', function() {
    const authWrapper = document.querySelector('.auth-wrapper');
    const loginTrigger = document.querySelector('.login-trigger');
    const registerTrigger = document.querySelector('.register-trigger');
    const loginForm = document.querySelector('.credentials-panel.signin form');

    // Notification function
    function showNotification(message, type) {
        debugger
        // Remove existing notifications
        const existingNotif = document.querySelector('.notification');
        if (existingNotif) {
            existingNotif.remove();
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.classList.add('notification', type);
        notification.innerHTML = `
            <span>${message}</span>
            <button class="close-btn">&times;</button>
        `;

        // Add to page
        document.body.insertBefore(notification, document.body.firstChild);

        // Close button functionality
        notification.querySelector('.close-btn').addEventListener('click', function() {
            notification.remove();
        });

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Handle Django messages
    const djangoMessages = document.querySelectorAll('.django-message');
    console.log('Found Django messages:', djangoMessages.length);
    
    if (djangoMessages.length > 0) {
        djangoMessages.forEach(msg => {
            const messageText = msg.textContent.trim();
            const messageType = msg.getAttribute('data-type') || 'error';
            
            console.log('Showing message:', messageText, 'Type:', messageType);
            showNotification(messageText, messageType);
        });
    }

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value.trim();

            if (!username || !password) {
                e.preventDefault();
                showNotification('Please enter both username and password', 'error');
            }
        });
    }

    if (registerTrigger) {
        registerTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            authWrapper.classList.add('toggled');
        });
    }

    if (loginTrigger) {
        loginTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            authWrapper.classList.remove('toggled');
        });
    }
});