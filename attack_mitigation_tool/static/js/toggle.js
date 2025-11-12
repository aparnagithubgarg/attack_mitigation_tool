// JavaScript for handling code toggle functionality

document.addEventListener('DOMContentLoaded', function() {
    // Handle toggle switches for secure/vulnerable mode
    const securityToggle = document.getElementById('security-toggle');
    if (securityToggle) {
        securityToggle.addEventListener('change', function() {
            // Submit the form to toggle security mode
            this.form.submit();
        });
    }

    // Handle code tab switching
    const codeTabs = document.querySelectorAll('[data-bs-toggle="tab"]');
    codeTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Highlight code in the newly activated tab
            setTimeout(() => {
                if (typeof Prism !== 'undefined') {
                    Prism.highlightAll();
                }
            }, 100);
        });
    });

    // Add explanations toggle
    const explanationToggles = document.querySelectorAll('.explanation-toggle');
    explanationToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const explanationElement = document.getElementById(targetId);
            
            if (explanationElement) {
                // Toggle visibility
                if (explanationElement.classList.contains('d-none')) {
                    explanationElement.classList.remove('d-none');
                    this.textContent = 'Hide Explanation';
                } else {
                    explanationElement.classList.add('d-none');
                    this.textContent = 'Show Explanation';
                }
            }
        });
    });

    // Handle demo buttons with confirmation
    const dangerousButtons = document.querySelectorAll('.btn-danger-confirm');
    dangerousButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('This action will execute potentially dangerous code. Are you sure you want to continue?')) {
                e.preventDefault();
                return false;
            }
        });
    });
});

// Function to toggle between vulnerable and secure code views
function toggleCodeView(attackType) {
    const vulnerableCode = document.getElementById(`${attackType}-vulnerable-code`);
    const secureCode = document.getElementById(`${attackType}-secure-code`);
    const toggleButton = document.getElementById(`${attackType}-toggle-button`);
    
    if (vulnerableCode && secureCode && toggleButton) {
        if (vulnerableCode.classList.contains('d-none')) {
            // Show vulnerable code
            vulnerableCode.classList.remove('d-none');
            secureCode.classList.add('d-none');
            toggleButton.textContent = 'Show Secure Code';
            toggleButton.classList.remove('btn-success');
            toggleButton.classList.add('btn-danger');
        } else {
            // Show secure code
            vulnerableCode.classList.add('d-none');
            secureCode.classList.remove('d-none');
            toggleButton.textContent = 'Show Vulnerable Code';
            toggleButton.classList.remove('btn-danger');
            toggleButton.classList.add('btn-success');
        }
        
        // Re-highlight code
        if (typeof Prism !== 'undefined') {
            Prism.highlightAll();
        }
    }
}

// Function to show/hide attack details
function toggleAttackDetails(attackId) {
    const detailsElement = document.getElementById(`${attackId}-details`);
    const toggleButton = document.getElementById(`${attackId}-details-toggle`);
    
    if (detailsElement && toggleButton) {
        if (detailsElement.classList.contains('d-none')) {
            // Show details
            detailsElement.classList.remove('d-none');
            toggleButton.textContent = 'Hide Details';
        } else {
            // Hide details
            detailsElement.classList.add('d-none');
            toggleButton.textContent = 'Show Details';
        }
    }
}