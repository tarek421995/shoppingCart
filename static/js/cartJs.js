$(document).ready(function(){  
  var productForm = $(".form-product-ajax")
  productForm.submit(function(event){
      console.log('submitting')
      event.preventDefault();
      var thisForm = $(this)
      var actionEndpoint = thisForm.attr("data-endpoint")
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();
      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          console.log('success')
          var submitSpan = thisForm.find(".submit-span")
          if (data.added){
            submitSpan.html('<a class="btn btn-link" class="text-uppercase" href="/cart/">In cart<i class="bi bi-arrow-up"></i></a><button type="submit" class="btn btn-secondry">Remove?</button>')
          } else {
            submitSpan.html("<button type='submit'class='btn btn-info'>Add to cart<i class='bi bi-arrow-right'></i></button>")
           }
          var navbarCount = $(".navbar-cart-count")
          navbarCount.text(data.cartItemCount)
          var currentPath = window.location.href

          if (currentPath.indexOf("cart") != -1) {
            refreshCart()
          }
        },
        error: function(errorData){
          $.alert({
            title: "Oops!",
            content: "An error occurred",
            theme: "modern",
          })
        }
      })
  })


})