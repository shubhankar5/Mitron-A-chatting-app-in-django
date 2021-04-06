function start_chat_search(){
	$.get($('#start-chat').data('ajaxUrl'),
	{
		'search_text' : $('#start-chat').val(),
		'mode' : 'start',
	},
	function(data){
		$('#start-chat-results').show();
		$('#start-chat-results').html(data);
	},
	'html'
	);
}

function load_requested_messages(id, load=$('#requested-message-body').scrollTop()){
	$.get($('#requested-message').data('ajaxUrl'),
	{
		'id' : id
	},
	function(data){
		$('#requested-message').html(data);
		if(load===true)
			$('#requested-message-body').scrollTop($('#requested-message-body')[0].scrollHeight);
		else{
			$('#requested-message-body').scrollTop(load);
		}
	},
	'html'
	);
}

function load_typing_box(id){
	$.get($('#typing-box').data('ajaxUrl'),
	{
		'id' : id,
	},
	function(data){
		$('#typing-box').html(data);
		// To add emojionearea uncomment the following; Might not work sometimes
		// $('#message-text').emojioneArea();
		// $('#message-text')[0].emojioneArea.setFocus();
		// To add emojionearea comment the following
		$('#message-text')[0].focus();
	},
	'html'	
	)
}

function load_requested(id, load){
	$('#welcome').hide();
	load_requested_messages(id, load);
	load_typing_box(id);
	var chats = setInterval(function(){
					var h1 = $('#requested-message-body')[0].scrollHeight;
					var t = $('#requested-message-body').scrollTop(); 
					var h2 = $('#requested-message-body').height();
					var offset = h1*0.075;
					if(h1-t-offset<h2){
						$('#bottom-button').hide();
						load_requested_messages(id, t);
					}
					else{
						$('#bottom-button').show();
					}
				}, 5000);
	return chats;
}

function message_logs(){
	$.get($('#message-logs').data('ajaxUrl'),
	function(data){
		$('#message-logs').html(data);
	},
	'html'	
	)
}

function bottom_check(){
	var h1, t, h2;
	h1 =  $('#requested-message-body')[0].scrollHeight;
	t = $('#requested-message-body').scrollTop(); 
	h2 =  $('#requested-message-body').height();
	if((h1-t)==h2)
		return true;
	else
		return false;	
}

$(function(){
	var id, load, chats=null;
	if( window.location.pathname == $('#home-url').attr('href') ){
		message_logs();
		setInterval(function(){
						message_logs();
					}, 5000);
		$('#start-chat').keyup( start_chat_search );
		$('#start-chat').click( start_chat_search );
	}

	$('body').on('click', '.chat-button', function(){
		id = $(this).data('userId');
		load=true;
		chats = load_requested(id, load);
	});

	$('body').on('click', '.message-to,.message-from', function(){
		id = $(this).data('userId');
		load=true;
		if(chats)
			clearInterval(chats);
		chats = load_requested(id, load);
		

	});

	$('body').on('click', '.unseen', function(){
		$.get($(this).data('ajaxUrl'),
		{
			'id' : $(this).children().data('userId')
		},
		function(){
			message_logs();
		}
		);
	});

	$('body').on('click', '#send-text', function(){
		// To add emojionearea uncomment the following one line; Might not work sometimes
		// var text = $('#message-text')[0].emojioneArea.getText();
		// To add emojionearea comment the following one line
		var text = $('#message-text').val();
		if(text!='' && text!=null){
			var new_text = text;
			if(text.length>35){
				var start=0;
				new_text='';
				while(start<text.length){
					new_text += (text.slice(start, start+35)+'\n');
					start+=35;
				}
			}
			$.post($('#send-text').data('ajaxUrl'),
			{
				'text' : new_text,
				'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
			},
			function(data){
				if( data.response == 'Sent' ){
					if(bottom_check())
						load_requested_messages(id, true);
					else
						load_requested_messages(id);
					message_logs();
					// To add emojionearea uncomment the following one line; Might not work sometimes
					// $('#message-text')[0].emojioneArea.setText('');
					// To add emojionearea comment the following one line
					$('#message-text').val('');
				}else{
					alert('Could not send your message. Try again later!');
				}
	  		},
	  		'json'
	  		);
		}
	});

	$('body').on('focus', '#message-text', function(){
		var shiftDown = false;
		$('#message-text').keydown(function(e){
			var key = e.which;
			if(key == 16){
				shiftDown = true;
			}
		});

		$('#message-text').keyup(function(e){
			var key = e.which;
			if(key == 13){
				e.preventDefault();
				if(!shiftDown){
					// To add emojionearea uncomment the following one line; Might not work sometimes
					// var text = $('#message-text')[0].emojioneArea.getText();
					// To add emojionearea comment the following one line
					var text = $('#message-text').val();
					if(text!='' && text!=null){
						var new_text = text;
						if(text.length>35){
							var start=0;
							new_text='';
							while(start<text.length){
								new_text += (text.slice(start, start+35)+'\n');
								start+=35;
							}
						}
						$.post($('#send-text').data('ajaxUrl'),
						{
							'text' : new_text,
							'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
						},
						function(data){
							if( data.response == 'Sent' ){
								if(bottom_check())
									load_requested_messages(id, true);
								else
									load_requested_messages(id);
								message_logs();
								// To add emojionearea uncomment the following one line; Might not work sometimes
								// $('#message-text')[0].emojioneArea.setText('');
								// To add emojionearea comment the following one line
								$('#message-text').val('');
							}else{
								alert('Could not send your message. Try again later!');
							}
				  		},
				  		'json'
				  		);
					}
				}
			}else if(key == 16){
				shiftDown = false;
			}
		});
	});

	$('body').on('submit', '#image-form', function(){
		$('#imageModal').modal('hide');
  		event.preventDefault();
		var formData = new FormData(this);
  		$.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            success: function (data) {
                if( data.response == 'Sent' ){
					if(bottom_check())
						load_requested_messages(id, true);
					else
						load_requested_messages(id);
					message_logs();
				}else{
					alert('Could not send your message. Try again later!');
				}
            },
            cache: false,
            contentType: false,
            processData: false
        });
	});

	$('body').on('click', '.message-div', function(){
		$(this).children('.like-button').hide();
		$.get($(this).data('ajaxUrl'),
		{
			'id' : $(this).data('val')
		},
		function(){
			load_requested_messages(id);
		});
	});

	$('body').on('click', '#bottom-button', function(){
		load_requested_messages(id, true);
	});
});
