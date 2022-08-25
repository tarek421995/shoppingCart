function cartOnload(){
  console.log('onload')
  var subtotal = 0
  var totalRowCount = 0;
  var rowCount = 0;
  item_data =[]
  var table = document.getElementById("cart");
  var rows = table.getElementsByTagName("tr");
  console.log(rows.length)
  for (var i = 0; i < rows.length; i++) {
      totalRowCount++;
      if (rows[i].getElementsByTagName("td").length > 0) {
          rowCount++;
      }
  }
  for (var i = 0; i < totalRowCount-3; i++){
    id = i+1
    var quantity = document.getElementById(id).value
    var item_slug_ = 'item_slug_';
    item_slug_ +=id;
    var item_slug_value = document.getElementById(item_slug_).value; 
    var id_price = 'id_price_'+id;
    price = document.getElementById(id_price).value
    var str_total_price = 'total_item_price_';
    str_total_price +=i+1;

    new_value = item_slug_value + '/' + quantity
    item_data.push(new_value);
    str_subtotal = document.getElementById(str_total_price).value = parseInt(quantity).toFixed(2) * parseInt(price).toFixed(2) 
    subtotal += parseInt(str_subtotal) 
  }
  document.getElementById('total_price').value  =  parseFloat(subtotal).toFixed(2)
  return item_data
}
window.onload = function() {
    cartOnload()
    $.ajax({
            type: 'POST',
            url: "/cart/quantity-update/",
            data: {"item_data": item_data},
            headers: {'X-CSRFToken': csrftoken},
            success: function (response) {
              console.log(response.data.length)
            },
            error: function (error) {
              console.log(error.responseJSON)
              $.alert({
                title: "Oops!",
                content: "SomeThing Wrong",
                theme: "modern",
              })
            }
        })
  }

  function calculate(id,price,quantity){
    var total_item_price = 'total_item_price_'+id;
    document.getElementById(total_item_price).value = parseInt(quantity).toFixed(2) * parseInt(price).toFixed(2)
    var subtotal = 0
    var quantity_value = quantity
    var item_slug_ = 'item_slug_';
    item_slug_ +=id;
    var item_slug_value = document.getElementById(item_slug_).value; 
    // console.log(item_slug_value)
    item_data = [item_slug_value + '/' + quantity_value]
    var totalRowCount = 0;
    var rowCount = 0;
    var table = document.getElementById("cart");
    var rows = table.getElementsByTagName("tr");
    for (var i = 0; i < rows.length; i++) {
        totalRowCount++;
        if (rows[i].getElementsByTagName("td").length > 0) {
            rowCount++;
        }
    }
    for (var i = 0; i < totalRowCount-3; i++){
        var str_total_price = 'total_item_price_';
        str_total_price +=i+1;
        var str_subtotal = document.getElementById(str_total_price).value;
        subtotal += parseInt(str_subtotal) 
    }
    total = document.getElementById('total_price').value = parseInt(subtotal).toFixed(2)
    document.getElementById('total_price').value  =  parseFloat(total).toFixed(2)
  }


  function updateFunc(e,path) {
    console.log(path)
    if (path == '/cart/confirm/'){
      window.location.href = path
    }else{
        id = $(e).attr('id')
        var div = document.getElementById("message");
        var quantity = document.getElementById(id).value
        var id_price = 'id_price_'+id;
        var price = document.getElementById(id_price).value
        calculate(id,price,quantity)
        if (quantity < 1){
          $.alert({
            title: 'erorr',
            content: 'quantity must be bigger than 1',
            theme: "modern",
          })
        }
      }
      setTimeout(function () {
        $.ajax({
            type: 'POST',
            url: path,
            data: {"item_data": item_data},
            headers: {'X-CSRFToken': csrftoken},
            success: function (response) { 
              console.log(response.msg)
              if (response.msg){
                var new_msg = document.createElement("div");
                new_msg.innerHTML = '<h5 class="message">'+ response.msg +'</h5>'
                div.prepend(new_msg)
                setTimeout(function () {
                  div.removeChild(new_msg)
                },5000)
                calculate(id,price,response.data)
                document.getElementById(id).value = response.data
              }    
            },
            error: function (error) {
              console.log(error.responseJSON)
              $.alert({
                title: "Oops!",
                content: "SomeThing Wrong",
                theme: "modern",
              })
            }
        })
    }, 500);
  }
  getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
