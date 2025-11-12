// Main JavaScript file for the Attack Mitigation Tool

// Initialize on document load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle code highlighting if Prism.js is available
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }

    // Generic form submission handlers
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Prevent form submission if it has the 'prevent-default' class
        if (form.classList.contains('prevent-default')) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                // Additional form handling can be added here
            });
        }
    });

    // Add copy to clipboard functionality for code snippets
    setupCodeCopyButtons();
});

// Copy to clipboard functionality for code snippets
function setupCodeCopyButtons() {
    // Add copy buttons to all code blocks
    document.querySelectorAll('pre').forEach(block => {
        // Only add button if it doesn't already have one
        if (!block.querySelector('.copy-button')) {
            const button = document.createElement('button');
            button.className = 'copy-button btn btn-sm btn-outline-secondary';
            button.type = 'button';
            button.innerText = 'Copy';
            
            // Position the button
            button.style.position = 'absolute';
            button.style.top = '5px';
            button.style.right = '5px';
            
            // Make sure the pre is positioned relatively
            if (window.getComputedStyle(block).position === 'static') {
                block.style.position = 'relative';
            }
            
            block.appendChild(button);
            
            // Add click event
            button.addEventListener('click', function() {
                const code = block.querySelector('code') || block;
                const text = code.innerText;
                
                // Copy text to clipboard
                navigator.clipboard.writeText(text).then(() => {
                    // Change button text temporarily
                    button.innerText = 'Copied!';
                    button.classList.remove('btn-outline-secondary');
                    button.classList.add('btn-success');
                    
                    // Reset button text after 2 seconds
                    setTimeout(() => {
                        button.innerText = 'Copy';
                        button.classList.remove('btn-success');
                        button.classList.add('btn-outline-secondary');
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy code: ', err);
                    button.innerText = 'Error!';
                    button.classList.remove('btn-outline-secondary');
                    button.classList.add('btn-danger');
                    
                    // Reset button text after 2 seconds
                    setTimeout(() => {
                        button.innerText = 'Copy';
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-outline-secondary');
                    }, 2000);
                });
            });
        }
    });
}

// Function to toggle between code tabs
function switchCodeTab(tabId) {
    const tabs = document.querySelectorAll('.code-tab');
    const tabContents = document.querySelectorAll('.code-tab-content');
    
    // Hide all tab contents
    tabContents.forEach(content => {
        content.classList.remove('active');
        content.classList.add('d-none');
    });
    
    // Deactivate all tabs
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Activate the selected tab
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Show the corresponding content
    const selectedContent = document.getElementById(tabId + '-content');
    if (selectedContent) {
        selectedContent.classList.remove('d-none');
        selectedContent.classList.add('active');
    }
}

// Function to handle asynchronous requests with a loading indicator
function sendAsyncRequest(url, method, data, onSuccess, onError) {
    // Show loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator text-center my-3';
    loadingIndicator.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Processing request...</p>
    `;
    
    // Find a container to add the loading indicator
    const container = document.querySelector('.content-container') || document.body;
    container.appendChild(loadingIndicator);
    
    // Create request options
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    // Add body for POST requests
    if (method.toUpperCase() === 'POST' && data) {
        options.body = JSON.stringify(data);
    }
    
    // Build URL with query parameters for GET requests
    let requestUrl = url;
    if (method.toUpperCase() === 'GET' && data) {
        const params = new URLSearchParams();
        for (const key in data) {
            params.append(key, data[key]);
        }
        requestUrl += '?' + params.toString();
    }
    
    // Send request
    fetch(requestUrl, options)
        .then(response => {
            // Remove loading indicator
            container.removeChild(loadingIndicator);
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (onSuccess && typeof onSuccess === 'function') {
                onSuccess(data);
            }
        })
        .catch(error => {
            // Remove loading indicator
            if (container.contains(loadingIndicator)) {
                container.removeChild(loadingIndicator);
            }
            
            console.error('Error:', error);
            if (onError && typeof onError === 'function') {
                onError(error);
            }
        });
}