const modal = document.querySelector('#modal')
const openModal = document.querySelectorAll('.btn-join')
const closeModal = document.querySelector('.closeBtn')

openModal.forEach(button => {
    button.addEventListener('click', () => {
        modal.showModal();
    })
})

closeModal.addEventListener('click', () => {
    modal.close()
})