const endbtn = document.body.querySelector('.endbtn');
const itemsToHide = document.body.querySelectorAll('.alert'); 

itemToClose = document.querySelectorAll('.alert')
endbtn.addEventListener('click', () => {
    itemsToHide.forEach(element => {
        element.hidden = true;
    });
})