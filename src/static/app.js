document.addEventListener('DOMContentLoaded', () => {
    const fetchEmailsButton = document.getElementById('fetch-emails');
    const emailList = document.getElementById('email-list');

    fetchEmailsButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/emails');
            const emails = await response.json();
            emailList.innerHTML = '';
            emails.forEach(email => {
                const li = document.createElement('li');
                li.textContent = email.snippet;
                emailList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching emails:', error);
        }
    });
});