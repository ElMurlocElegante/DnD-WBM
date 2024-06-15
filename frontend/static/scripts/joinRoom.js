const modal = document.querySelector('#modal')
const openModal = document.querySelectorAll('.btn-join')
const closeModal = document.querySelector('.closeBtn')

openModal.forEach(button => {
    button.addEventListener('click', () => {
        fetch('http://localhost:5001/api/check_login', 
            {   method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
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
