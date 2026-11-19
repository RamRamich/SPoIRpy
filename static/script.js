async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        
        const container = document.getElementById('users-list');
        if (!container) return;
        
        container.innerHTML = '';
        
        for (const user of users) {
            const li = document.createElement('li');
            li.textContent = `${user.id}: ${user.username} (${user.email})`;
            container.appendChild(li);
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadUsers);