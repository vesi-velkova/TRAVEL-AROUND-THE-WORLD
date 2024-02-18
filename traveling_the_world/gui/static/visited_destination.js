window.onload = function(){
    var items = document.querySelectorAll('.list-item input');
    for (var i=0; i<items.length; i++){
        items[i].onchange = function(){
            if (this.checked){
                this.parentElement.classList.add("visited-item");
            }
            else{
                this.parentElement.classList.remove("visited-item");
            }
        }
        items[i].parentElement.onclick = function(){
            input = this.querySelector('input');
            state = input.checked ? 0 : 1;
            console.log(state)
            fetch('/visit_item?id=' + input.dataset.id + '&state=' + state).then(function (response) {
                if (response.ok) {return response.json();}
                return Promise.reject(response);
            }).then(function (data) {
                console.log(data['state']);
                input.checked = data['state'];
                input.onchange();
            }).catch(function (err) {
                console.warn('Unable to toggle the country state.', err);
            });
        }
        items[i].onchange();
    }
}