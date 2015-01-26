GetRandomAnime = function () {
	$.ajax({
    	type: 'GET',
    	url: '/work/rand_anime',
    	success: function(data) {
	        $('.added_ani_num').val(data.ani_num);
	        $('input[name=title]').val(data.title);
	        $('.added_genres').append(data.genres.join(', '));

	        $('.added_img').attr('src','/image?ani_num=' + data.ani_num);
    	}
    });
}

PassForm = function() {

    $(':input')
     .not(':button, :submit, :reset, :hidden')
     .val('')
     .removeAttr('checked')
     .removeAttr('selected');

     $('.added').each(function() {
        $(this).remove();
     })

     $('.added_genres').html('');

     GetRandomAnime();

    $('.title').focus();
};

$.get('/work', function() {

	GetRandomAnime();
	
	$('.form-submit').click(function() {
		form_data();
		console.log(jsonString)
		$.ajax({
			type: 'POST',
			url: '/work/',
			data: jsonString,
			dataType: 'json',
			success: function(data) {
				data: jsonString
				console.log(data);
			}
		});
	});
});