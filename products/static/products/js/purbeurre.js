(function($) {
  "use strict"; // Start of use strict

// Product search in database

  // Launche the search with enter key
  $("searcharea").keyup(function(ev) {
    if (ev.which == 13) {
        $("#getSearch").click();
    }
  });

  // Launche the search with click button
  $("getSearch").click(function(e) {
    e.preventDefault();

    var user_search = $("input[id='search2']").val();

    // process the search
    $.ajax({

        type: 'POST',
        url: '/results/save_in_db',
        data: JSON.stringify({'product':user_search}),
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


  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

})(jQuery); // End of use strict
