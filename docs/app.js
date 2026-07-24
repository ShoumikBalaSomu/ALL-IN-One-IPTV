document.addEventListener('DOMContentLoaded', () => {
    // Basic search functionality for docs
    const searchInput = document.getElementById('doc-search');
    const sections = document.querySelectorAll('.doc-section');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            sections.forEach(section => {
                const text = section.innerText.toLowerCase();
                if (text.includes(query)) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        });
    }

    // Code copy buttons
    document.querySelectorAll('pre').forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.innerText = 'Copy';
        block.appendChild(button);

        button.addEventListener('click', () => {
            const code = block.querySelector('code').innerText;
            navigator.clipboard.writeText(code).then(() => {
                button.innerText = 'Copied!';
                setTimeout(() => button.innerText = 'Copy', 2000);
            });
        });
    });
});
