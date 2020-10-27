function increment(item_id) {
    var value = parseInt(document.getElementById('inc').value, 10);
    value = isNaN(value) ? 0 : value;
    alert(item_id)
    value++;
    /*
    params = item_id
    let xhr = new XMLHttpRequest();
    xhr.open('POST', "/edit_cart_quantity", true)
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {//Call a function when the state changes.
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText);
        }
        xhr.send(params);
    }

     */
}

