// Main JavaScript file

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Save response functionality
    const saveButtons = document.querySelectorAll('.save-response');
    saveButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const responseId = this.dataset.id;
            try {
                const response = await fetch('/save_response', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        response_id: responseId
                    })
                });
                
                if (response.ok) {
                    this.innerHTML = '<i class="fas fa-check"></i> Saved';
                    this.classList.add('bg-green-600');
                }
            } catch (error) {
                console.error('Error saving response:', error);
            }
        });
    });

    // Copy code blocks
    document.querySelectorAll('pre code').forEach(codeBlock => {
        const button = document.createElement('button');
        button.className = 'copy-code absolute top-2 right-2 bg-gray-700 text-white px-2 py-1 rounded text-sm';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.title = 'Copy code';
        
        const pre = codeBlock.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
        
        button.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(() => {
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
        });
    });

    // Auto-expand textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});

// Theme toggle (optional)
function toggleTheme() {
    const html = document.documentElement;
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}

// Check saved theme
if (localStorage.getItem('theme') === 'dark') {
    document.documentElement.classList.add('dark');
}