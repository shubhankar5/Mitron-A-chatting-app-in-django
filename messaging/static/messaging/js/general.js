$(function(){
	if( window.location.pathname == $('#home-url').attr('href') ){
		new WOW().init();
	}

	$('.nav-item').each(function(){
		if( $(this).find('a').attr('href') == window.location.pathname ){ 
			$(this).addClass('active');
		}else{
			x = $(this);
			$(this).find('div').find('a').each(function(){
				if( $(this).attr('href') == window.location.pathname ){
					x.addClass('active');
				}
			});	
		}
	});
		
	$(window).click(function(event){
		if (!event.target.matches('#notification-icon')){
		    var dropdown = document.getElementById('notification-body');
		    if (dropdown.classList.contains('show')){
		    	dropdown.classList.remove('show');
		    }
		}
		if(!event.target.matches('#search-results-users') && !event.target.matches('#search-users')){
			$('#search-results-users').hide();
		}
		if(!event.target.matches('#start-chat-results') && !event.target.matches('#start-chat')){
			$('#start-chat-results').hide();
		}
	});

	$('body').on('mouseover', '.message-div', function(){
		if($(this).data('liked')=='False'){
			$(this).children('.like-button').show();
		}
	});

	$('body').on('mouseout', '.message-div', function(){
		if($(this).data('liked')=='False'){
			$(this).children('.like-button').hide();
		}
	});

	$('.cancel-button').click(function(){
  		window.history.back();
  	});

  	$(".alert").fadeTo(5000, 1).slideUp(800);
});
