$(document).ready(function () {

  // Autocompletion
  $(".searchInput").autocomplete ({
    source: "/products/autocomplete/",
    minLength: 1,
  });

  // Save product in db
  $(".btn-save").click(function(e) {
    e.preventDefault();
    //var form = $(this).closest("form");
    var substitute_id = $(this).attr('data-subid');
    var product_id = $(this).attr('data-prodid');
    var token = $(this).attr('data-token');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', token);
        }
    })

    $.ajax({
        type: 'POST',
        url: 'results/save_in_db/',
        data: JSON.stringify({substitute_id:substitute_id, product_id:product_id}),
        contentType: 'application/json; charset=utf-8',

        success: function(data) {
            if (data.is_created) {
                toastr.success(data, "Ce produit a bien été enregistré dans votre espace");
            }
            else if (data.is_in_db) {
                toastr.error(data, "Cette substitution est déjà dans votre espace");
            }
        }
    })
  });
})
