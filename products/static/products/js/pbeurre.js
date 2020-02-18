$(document).ready(function () {
//(function($) {

  // Autocompletion
  //$("search").autocomplete({
    //source: "autocomplete/",
    //minLength: 2,
  //});

  /* Search product in db with enter key
  $(".btn-save").keyup(function(ev) {
    if (ev.which == 13) {
        $(".btn-save").click();
    }
  });*/

  // Save product in db
  $(".btn-save").click(function(e) {
    e.preventDefault();

    var substitute_id = $(this).attr('substitute_id');
    var product_id = $(this).attr('product_id');
    //var token = $(this).attr('token');

    /*$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', token);
        }
    })*/

    $.ajax({

        //type: 'POST',
        url: 'results/save_in_db/',
        data: JSON.stringify({substitute_id:substitute_id, product_id: product_id}),
        contentType: 'application/json; charset=utf-8',

        success: function(data) {
            if (data.is_selected) {
                alert("Ce produit a bien été enregistré dans votre espace");
            }
            else {
                alert("Vous n'avez sélectionné aucun produit");
            }
        }
    })
  });
})
