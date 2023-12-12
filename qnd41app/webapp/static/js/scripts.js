/* ---------------------------------------------------------------------- */
/*	LOADER
/* ---------------------------------------------------------------------- */
$(window).load(function() {
	"use strict";
	$("#loading").fadeOut("1000", function() {
	// Animation complete
		$('#loading img').css("display","none");
		$('#loading').css("display","none");
		$('#loading').css("background","none");
		$('#loading').css("width","0");
		$('#loading').css("height","0");
		$('.animate').waypoint(function() {
			var animation = $(this).attr("data-animate");
			$(this).addClass(animation);
			$(this).addClass('animated');
		}, { offset: '95%' }); 
		
	});
});

$(document).ready(function(){
	"use strict";
	
	/* ---------------------------------------------------------------------- */
	/*	MAP HEIGHT & CANVAS
	/* ---------------------------------------------------------------------- */
	function divHeight(){
		var windowHeight = $(window).height();
		var homepageHeight = $('#home').height();
		
		if (windowHeight >= homepageHeight){
			$('.home-content').css("height", (windowHeight));
			$('.map-content').css("height", (windowHeight));
			$('#canvas').css("height", (windowHeight));
		} else{
			$('.home-content').css("height", (homepageHeight+50));
			$('.map-content').css("height", (homepageHeight+50));
			$('#canvas').css("height", (homepageHeight+50));
		}
	}
	
	divHeight();
	
	$(window).resize(function() {
		divHeight();
	});
	
	/* ---------------------------------------------------------------------- */
	/*	DIV HOME POSITION
	/* ---------------------------------------------------------------------- */
	function homePosition(){
		var windowHeight = $(window).height();
		var homepageHeight = $('#home').height();
		
		if (windowHeight >= homepageHeight){
			$('#home').css("margin-top", ((windowHeight-homepageHeight))/2);
		} else {
			$('#home').css("margin-top", "0");
		}
	}
		
	homePosition();

	$(window).resize(function() {		
		homePosition()	
	});
	
	/* ---------------------------------------------------------------------- */
	/*  DIV CONTACTFORM POSITION
	/* ---------------------------------------------------------------------- */
	function contactPosition(){
		var footerHeight = $('footer').height();
		var contactHeight = $('.contact').height();
		var windowtWidth = $(window).width();
		var mapContentHeight = $('.map-content').height();
		
		if (windowtWidth >= 478){
			var difference = mapContentHeight - footerHeight;
			$('.contact').css("margin-top", ((difference-contactHeight)/2));
		} else {
			$('.contact').css("margin-top", '0');
		}
	}
	
	contactPosition();
	
	$(window).resize(function() {
		contactPosition();
	});	
	
	/* ---------------------------------------------------------------------- */
	/*	SCROLL MEET-US
	/* ---------------------------------------------------------------------- */
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();

	if (windowWidth <= 480){
		$('.meet-us').css("height", (windowHeight-70));
	}
	
	/* ---------------------------------------------------------------------- */
	/*	SCROLL PAGE WITH EASING EFFECT
	/* ---------------------------------------------------------------------- */
	
  	/*
  	$('#link-map').bind('click', function(e) {
	    e.preventDefault();
	    var target = this.hash;
	    $.scrollTo(target, 750, {
	    	easing: 'swing',
	    	axis: 'y'
	    });
	});
	$('#home-top').bind('click', function(e) {
	    e.preventDefault();
	    $.scrollTo(0, 1250, {
	    	easing: 'swing',
	    	axis: 'y'
	    });
	});
  	*/
	
	$('#link-map').on('click', function(event) {   
	    var target = $(this.getAttribute('href'));
	    if( target.length ) {
	        event.preventDefault();
	        $('html, body').stop().animate({
	            scrollTop: target.offset().top
	        }, 1000);
	    }	    	    
	});
	
	$('#home-top').on('click', function(event) {
		event.preventDefault();
        $('html, body').stop().animate({
            scrollTop: 0
        }, 1000);	
	});
	
	
	/* ---------------------------------------------------------------------- */
	/*	CLOSE COOKIES MESSAGE
	/* ---------------------------------------------------------------------- */
	$(".close-cookies").click(function() {
		$("#cookies-message").addClass('fadeOutDown');
		setTimeout ( function () {
			$("#cookies-message").fadeOut();
		},500 );
	});
		
	/* ---------------------------------------------------------------------- */
	/*	COUNTDOWN
	/* ---------------------------------------------------------------------- */
	if ( $.fn.countdown ) {
		var now = new Date();
		var date = new Date('2023','11','31','00','00','00'); // new Date( year , month , day , hour , minutes , seconds)
		var difference = date - now; 
		var countTo = difference + now.valueOf();
		$('.timer').countdown(countTo, function(event) {
			var $this = $(this);
			switch(event.type) {
				case "seconds":
				case "minutes":
				case "hours":
				case "days":
				case "weeks":
				case "daysLeft":
					$this.find('span.'+event.type).html(event.value);
					break;
				case "finished":
					$this.fadeOut();
					setTimeout ( function () { //if you want add a text
						$this.text("The countdown is ended!");
						$this.fadeIn();
					},1500 );
					break;
			}
			if ( ($('.days').html()) == 1 ){
				$('.daysText').text(" day ");
			}else{
				$('.daysText').text(" days ");
			}
			if ( ($('.hours').html()) == 1 ){
				$('.hoursText').text(" hour ");
			}else{
				$('.hoursText').text(" hours ");
			}
			if ( ($('.minutes').html()) == 1 ){
				$('.minutesText').text(" minute ");
			}else{
				$('.minutesText').text(" minutes ");
			}
			if ( ($('.seconds').html()) == 1 ){
				$('.secondsText').text(" second ");
			}else{
				$('.secondsText').text(" seconds ");
			}
		});
	}
	
	/* ---------------------------------------------------------------------- */
	/*	SUSCRIPTION FORM
	/* ---------------------------------------------------------------------- */
    $('.success-message').hide();
    $('.error-message').hide();

    $('.subscribe form').submit(function() {
        var postdata = $('.subscribe form').serialize();
        $.ajax({
            type: 'POST',
            url: 'php/sendmail.php',
            data: postdata,
            dataType: 'json',
            success: function(json) {
                if(json.valid == 0) {
                    $('.success-message').hide();
                    $('.error-message').hide();
                    $('.error-message').html(json.message);
                    $('.error-message').fadeIn().delay(3000).fadeOut();
                }
                else {
                    $('.error-message').hide();
                    $('.success-message').hide();
                    $('.subscribe form').hide().delay(3000).fadeIn();
                    $('.subscribe form input').val('');
                    $('.success-message').html(json.message);
                    $('.success-message').fadeIn().delay(2000).fadeOut();
                }
            }
        });
        return false;
    });
    
    /* ---------------------------------------------------------------------- */
	/*	CONTACT FORM
	/* ---------------------------------------------------------------------- */
    $('.success-message-2').hide();
    $('.error-message-2').hide();
    
	var $contactform 	= $('#contactform'),
		$success		= 'Your message has been sent. Thank you!';
		
	$contactform.submit(function(){
		$.ajax({
		   type: "POST",
		   url: "php/contact.php",
		   data: $(this).serialize(),
		   success: function(msg)
		   {
				if(msg == 'SEND'){
					$('.error-message-2').hide();
                    $('.success-message-2').hide();
                    $contactform.hide().delay(3000).fadeIn();
                    $('#contactform input').val('');
                    $('#contactform textarea').val('');
                    $('.success-message-2').html('<div class="success-message-2">'+ $success +'</div>');
                    $('.success-message-2').fadeIn().delay(2000).fadeOut();
				}
				else{
					$('.success-message-2').hide();
                    $('.error-message-2').hide();
                    $('.error-message-2').html('<div class="error-message-2">'+ msg +'</div>');
                    $('.error-message-2').fadeIn().delay(3000).fadeOut();
				}
			}
		 });
		return false;
	});	
	
	/* ==============================================
    COUNTDOWN
    =============================================== */
	if ( $.fn.TimeCircles ) {
		countDownCircular();
		function countDownCircular() {
			$("#DateCountdown").TimeCircles({
			    "animation": "smooth",
			    "bg_width": 0.1,
			    "fg_width": 0.016666666666666666,
			    "circle_bg_color": "#fff",
			    "time": {
			        "Days": {
			            "text": "days",
			            "color": "#fff",
			            "show": true
			        },
			        "Hours": {
			            "text": "hours",
			            "color": "#fff",
			            "show": true
			        },
			        "Minutes": {
			            "text": "minutes",
			            "color": "#fff",
			            "show": true
			        },
			        "Seconds": {
			            "text": "seconds",
			            "color": "#fff",
			            "show": true
			        }
			    }
			});
		};
		$(window).resize(function() {		
			$("#DateCountdown").TimeCircles().rebuild();
		});
	}
	
	/* ---------------------------------------------------------------------- */
	/*	GOOGLE MAPS
	/* ---------------------------------------------------------------------- */
	var $map 				= $('#map'),
		$address 			= 'Paseo de la Castellana, 1, 28046, Madrid'; //Here, you put your adress

		$map.gMap({
			address: $address,
			zoom: 14,
			scrollwheel: false,
		    navigationControl: false,
		    mapTypeControl: false,
		    scaleControl: false,
		    draggable: false,
		    mapTypeId: google.maps.MapTypeId.ROADMAP
		});
		
	/* ---------------------------------------------------------------------- */
	/*  TOOLTIP
	/* ---------------------------------------------------------------------- */
	$('.footer-social a').tooltip();	
			
});
