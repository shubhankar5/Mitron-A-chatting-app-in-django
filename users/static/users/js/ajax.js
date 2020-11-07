function get_notifications(){ 
	$.get($('#notification-count').attr('ajax-url'),
	{
		'mode' : 'count'
	},
	function(data){
		$('#notification-count').html(data);
	},
	'html'
	);

	$.get($('#notification-body').attr('ajax-url'),
	{
		'mode' : 'body'
	},
	function(data){
		$('#notification-body').html(data);
	},
	'html'
	);
}

function search_friends(){
	$.get($('#search-friends').attr('ajax-url'),
	{
		'search_text' : $('#search-friends').val(),
		'mode' : 'friends',
	},
	function(data){
		$('#search-results-friends').html(data);
	},
	'html'
	);
}

$(function(){
	$.ajaxSetup({
	    error: function(xhr){
	    	if (xhr.status >=400){
	        	alert('Error!\n Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText);
	    	}
	    }
	});

	if( $('body').attr('user-status') == 'True'){
		get_notifications();

		setInterval(function(){
			get_notifications();
		}, 5000);
		
		$('body').on('click', '#notification-icon', function(){
			document.getElementById('notification-body').classList.toggle('show');
			$.get($(this).attr('ajax-url'),
			{
				'last' : $('#notification-count-value').attr('last'),
			},
			function(data){
				if(data.response == 'success'){
					get_notifications();
				}
			}
			);
		});
	}

	$('#search-users').keyup(function(){
		$.get($(this).attr('ajax-url'),
			{
				'search_text' : $(this).val(),
			},
			function(data){
				$('#search-results-users').show();
				$('#search-results-users').html(data);
			},
			'html'
		);
	});

	$('body').on('click', '#view-all-button', function () {
		window.location = $('#view-all-button').attr('ajax-url') + 'keyword='+ $('#search-users').val();
	});

	$('body').on('click', '#remove-picture', function (){
		$.get($(this).attr('ajax-url'),
		{
			'mode' : $(this).attr('id')
		},
		function(){
			location.reload();
		}
		);
	});

	if( window.location.pathname == $('#friends-url').attr('href') ){	
		search_friends();
		$('#search-friends').keyup( search_friends );
	}

	$('.ajax-friend-button').click(function(){
		$.post($(this).attr('ajax-url'),
		{
			'user_id' : $(this).attr('user-id'),
			'choice' : $(this).attr('id'),
			'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
		},
		function(){
			location.reload();
  		},
  		'json'
  		);
  	});

	$('.block-button').click(function(){
		$.get($(this).attr('ajax-url'),
		function(){
			location.reload();
  		},
  		'json'
  		);
  	});
});