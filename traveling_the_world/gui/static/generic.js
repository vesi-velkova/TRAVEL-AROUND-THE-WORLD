window.onload = function(){
    var items = document.querySelectorAll('.list-item input');
    for (var i=0; i<items.length; i++){
        // Remove element on x-button click
        var remove_button = items[i].parentElement.querySelector('.remove-item');
        remove_button.onclick = function(event){
            var row = this.parentElement;
            var input = row.querySelector('input');
            fetch('/remove_item?id=' + input.dataset.id).then(function (response) {
                if (response.ok) {return response.json();}
                return Promise.reject(response);
            }).then(function (data) {
                row.remove();
            }).catch(function (err) {
                console.warn('Unable to toggle the item state.', err);
            });
            event.stopPropagation();
        }
    }
}