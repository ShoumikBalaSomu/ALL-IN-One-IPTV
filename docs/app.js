document.querySelectorAll('.sidebar nav a').forEach(link => {
    link.addEventListener('click', (e) => {
        document.querySelectorAll('.sidebar nav a').forEach(l => l.classList.remove('active'));
        e.target.classList.add('active');
    });
});
