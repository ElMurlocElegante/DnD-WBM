const modal = document.querySelector('#modal')
const openModal = document.querySelectorAll('.btn-join')
const closeModal = document.querySelector('.closeBtn')

openModal.forEach(button => {
    
    button.addEventListener('click', () => {
        fetch('/delete_character', 
            {   method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    character_id: button.value
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.logged_in) {
                    modal.showModal();
                } else {
                    window.location.href = '/login';
                }
            })
    })
})

closeModal.addEventListener('click', () => {
    modal.close()
})
