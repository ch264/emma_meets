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



  // function to toggle between reviews and favorites on profile page
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


  // bubbles
  // Created for an Articles on:
// https://www.html5andbeyond.com/bubbling-text-effect-no-canvas-required/

  // // Define a blank array for the effect positions. This will be populated based on width of the title.
  // var bArray = [];
  // // Define a size array, this will be used to vary bubble sizes
  // var sArray = [4,6,8,10];
  // // Push the header width values to bArray
  // for (var i = 0; i < $('.bubbles').width(); i++) {
  //     bArray.push(i);
  // }
  
  // // Function to select random array element
  // // Used within the setInterval a few times
  // function randomValue(arr) {
  //     return arr[Math.floor(Math.random() * arr.length)];
  // }

  // // setInterval function used to create new bubble every 350 milliseconds
  // setInterval(function(){
  //     // Get a random size, defined as variable so it can be used for both width and height
  //     var size = randomValue(sArray);
  //     // New bubble appeneded to div with it's size and left position being set inline
  //     // Left value is set through getting a random value from bArray
  //     $('.bubbles').append('<div class="individual-bubble" style="left: ' + randomValue(bArray) + 'px; width: ' + size + 'px; height:' + size + 'px;"></div>');
  //     // Animate each bubble to the top (bottom 100%) and reduce opacity as it moves
  //     // Callback function used to remove finsihed animations from the page
  //     $('.individual-bubble').animate({
  //         'bottom': '100%',
  //         'opacity' : '-=0.7'
  //     }, 3000, function(){
  //         $(this).remove()
  //     }
  //     );
  // }, 350);

});

