const modalPass = document.querySelector('#modalPass')
const modalDelete = document.querySelector('#modalDelete')
const openModalPassword = document.querySelector('.btn-change-pass')
const openModalDeleteAccount = document.querySelector('.btn-del-account')
const closeModalPass = document.querySelector('.closeBtnPass')
const closeModalDelete = document.querySelectorAll('.closeBtnDelete')


openModalPassword.addEventListener('click', () => {
    fetch('/check_login', 
        {   method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                modalPass.showModal();
            } else {
                window.location.href = '/login';
            }
        })
})

openModalDeleteAccount.addEventListener('click', () => {
    fetch('/check_login',
        {  method: 'GET',
           headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                modalDelete.showModal();
            } else {
                window.location.href = '/login'
            }
        })
})

closeModalDelete.forEach( button => {
    button.addEventListener('click', () => {
        modalDelete.close()
    })
})

closeModalPass.addEventListener('click', () => {
    modalPass.close()
})