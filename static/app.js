$(document).ready(function() {
  // Click function to open navbar when hamburger icon is clicked
  $('.navbar-burger').on('click', function(event) {
    event.preventDefault();
    // Toggles 'is-active' class to show or hide navbar
    $('.navbar-burger').toggleClass('is-active');
    $('.navbar-menu').toggleClass('is-active');
  });

  // Click function to open modal when user wants to delete a review
  $('.modal-button').on('click', function(event) {
    event.preventDefault();
    $('.modal').toggleClass('is-active');
  });

  // Click function to close delete review modal
  $('.modal-close').on('click', function(event) {
    event.preventDefault();
    $('.modal').toggleClass('is-active');
  });

  $('.button').each(function(){
    var toggle_div_id = 'description_' + $(this).attr('id');
    $(this).click(function(){
        $('#'+toggle_div_id).toggle(700)
    });
  });


  // $('.button_1').on('click', function(e){
  //   e.preventDefault();
  //   $('description_button_1').toggle(700)
  //     // .not($('description_button_2'+toggle_div_id)).hide();
  //   });
  // });


});

