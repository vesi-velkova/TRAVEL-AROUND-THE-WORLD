window.onload = function(){
    var removeButtons = document.querySelectorAll('.remove-item');
    removeButtons.forEach(function(button)
    {
        button.addEventListener('click', function(event)
        {
            event.preventDefault();
            var listItemContainer = this.parentElement;
            var itemId = this.dataset.id;
            console.log(itemId);
            fetch('/remove_item?id=' + itemId).then(function (response) {
                if (response.ok) {return response.json();}
                    return Promise.reject(response);
                }).then(function (data) {
                    listItemContainer.remove();
                    console.log(data);
                    location.reload();
                }).catch(function (err) {
                    console.warn('Unable to toggle the item state.', err);
                    console.error('Error removimg item:', err);
                });
        });
    });
};
