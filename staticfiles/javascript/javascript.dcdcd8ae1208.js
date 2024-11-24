//This file contains js for django project. Written on JQuery, using ajax

$(document).ready(function()
{
let smooth = true;
let height = 0;
let all_sticky_sidebars;
  
	let anim = smooth ? 'smooth' : 'auto';
  if($("#article-system")[0] !== undefined){
      $("html, body").animate({
        scrollTop: $("#article-system").offset().top - 90
      }, // second param is how much, does it need to scroll down
        1000);
    }

$(".is-invalid").nextAll("#error_1_id_start_date").first().attr("background-image", '0');

// scrolling top function
$("#scroll-top").click(function(){
  $("html, body")[0].scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
});
$("#scroll-bot").click(function(){
  $("footer")[0].scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
});

$(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

});

// Reputation of forum post logic
function onPostThumbs(user_id, post_id, user_action){
  

    let csrftoken = $.cookie('csrftoken');

    let data = {user_id, post_id, user_action};


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);

            }

        }
    });

    $.ajax({
      url: `ajax/`,
      data: data,
      type: 'post',
      success: function(result)
      {

        $('#people_voted_counter').text(result.people_voted);
        $('#repa').text(result.reputation)
        console.log("success!")
        console.log(result.current_relation_reputation)
        if(result.current_relation_reputation == 1){


          $('#like').removeClass('far').addClass('fas');
          $('#dislike').removeClass('fas').addClass('far')
        }
        else if(result.current_relation_reputation == -1){
          // change green icon class to not bold
          // change red icon class to bold
          $('#like').removeClass('fas').addClass('far');
          $('#dislike').removeClass('far').addClass('fas')
        }
        else{
          // change both icons to not bold class
          $('#like').removeClass('fas').addClass('far');
          $('#dislike').removeClass('fas').addClass('far')


        }

      }
});

}


// ajax function for user assessesment

function onUserThumbs(user_appraiser_id, user_assessed_id, user_action){
  let csrftoken = $.cookie('csrftoken');

  let data = {user_appraiser_id, user_assessed_id, user_action};

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);

          }

      }
  });

// User reputation ajax
$.ajax({
      url: `ajax/`,
      data: data,
      type: 'post',
      success: function(result)
      {
        // Change reputation, when request is success
        $('#repa').text(result.reputation)

        if(result.current_relation_reputation == 1){

          // change green icon class to bold
          // change red icon class to not bold
          $('#like').removeClass('far').addClass('fas');
          $('#dislike').removeClass('fas').addClass('far')
        }
        else if(result.current_relation_reputation == -1){
          // change green icon class to not bold
          // change red icon class to bold
          $('#like').removeClass('fas').addClass('far');
          $('#dislike').removeClass('far').addClass('fas')
        }
        else{
          // change both icons to not bold class
          $('#like').removeClass('fas').addClass('far');
          $('#dislike').removeClass('fas').addClass('far')


        }

      }
  });


}
