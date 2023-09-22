// if homepage, then hide navbar on load
if ( window.location.pathname == '/' ){
  if ($('.smart-scroll').length > 0) { // check if element exists
    $(window).on('load', function() {
      $('.smart-scroll').removeClass('scrolled-down').addClass('scrolled-up');
    });
    $(window).on('scroll', function() {
        scroll_top = $(this).scrollTop();
        if(scroll_top == 0) {
            $('.smart-scroll').removeClass('scrolled-down').addClass('scrolled-up');
        }
        else {
            $('.smart-scroll').removeClass('scrolled-up').addClass('scrolled-down');
        }
    });
  }
}

// Check for element id 'particles-enabled'
if ( document.getElementById('particles-enabled')) {
  particlesJS.load("particle-div1", "/static/js/particles.json", function() {
    console.log("callback - particles.js config loaded");
  });
}

$('.slick-carousel').slick({
  centerMode: true,
  prevArrow:"<div class=\"carousel-control w-auto\" role=\"button\"><span class=\"fa fa-chevron-left fa-5x p-1\" style=\"background-color: white;\"></span></div>",
  nextArrow:"<div class=\"carousel-control w-auto\" role=\"button\" style=\"right:0;\"><span class=\"fa fa-chevron-right fa-5x p-1\" style=\"background-color: white;\"></span></div>",
  dots: true,
  infinite: true,
  speed: 300,
  slidesToShow: 4,
  initialSlide: 1,
  slidesToScroll: 1,
  autoplay: true,
  variableWidth: true,
  swipeToSlide: true,
  responsive: [
    {
      breakpoint: 2000,
      settings: {
        slidesToShow: 3,
        initialSlide: 1,
      }
    },
    {
      breakpoint: 1400,
      settings: {
        slidesToShow: 2,
        initialSlide: 0,
      }
    },
    {
      breakpoint: 768,
      settings: {
        slidesToShow: 2,
        initialSlide: 0,
      }
    }
    // You can unslick at a given breakpoint now by adding:
    // settings: "unslick"
    // instead of a settings object
  ]
});

// enable tooltips everywhere (via Popper, bundles with bootstrap)
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

// handle carousel buttons, loop if last element
$('.carousel .carousel-item').each(function(){
    var minPerSlide = 3;

    var next = $(this).next();
    if (!next.length) {
    next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));
    
    for (var i=0;i<minPerSlide;i++) {
        next=next.next();
        if (!next.length) {
        	next = $(this).siblings(':first');
      	}
        
        next.children(':first-child').clone().appendTo($(this));
      }
});

// if browse page, toggle advanced search
if ( window.location.pathname.indexOf("/browse") == 0 ){
  $('#advancedSearchCollapse').click(function(){
    if ($('#advancedSearchCollapseIcon').hasClass('fa-chevron-down')) {
      $('#advancedSearchCollapseIcon').removeClass('fa-chevron-down').addClass('fa-chevron-up')
    } 
    else {
      $('#advancedSearchCollapseIcon').removeClass('fa-chevron-up').addClass('fa-chevron-down')
    }
});
}

$('.custom-file-input').on('change', function() { 
  let fileName = $(this).val().split('\\').pop(); 
  $(this).next('.custom-file-label').addClass("selected").html(fileName); 
});