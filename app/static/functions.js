function doubleCheck(price) {
    var StringValue = parseFloat(price);
    if (price <= 0) {
        alert("Nothing to checkout");
        return false;
    }
    var agree = confirm("Are you sure you're ready to checkout?\nYou will be charged $" +
        StringValue.toFixed( 2 ))

    if (!agree) {
        return false;
    }
    this.form.submit();

}

function change(quantity, item_id, type) {
    if (type == 1) {
        quantity += 1;
    }
    else {
        quantity -= 1;
    }
    if (quantity < 0) {
        return;
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/edit_cart_quantity');
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    let json = JSON.stringify({
        quantity: quantity,
        item_id: item_id
    })
    xhr.send(json);
    xhr.onload = function() {
        if (xhr.status != 200) { // HTTP error?
            // handle error
            return;
        }
        location.reload();
    };
    xhr.onerror = function() {
        return;
    };
}

function formatPrice(price) {
    var StringValue = parseFloat(price);
    document.write(StringValue.toFixed( 2 ));
}


$(document).ready( function () {
    $('#myTable').DataTable();
} );