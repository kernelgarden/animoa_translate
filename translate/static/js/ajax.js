PassForm = function() {

    $(':input')
     .not(':button, :submit, :reset, :hidden')
     .val('')
     .removeAttr('checked')
     .removeAttr('selected');

     $('.added').each(function() {
        $(this).remove();
     })

    $.get('/work/rand_anime',function(data) {
        $('.added_ani_num').val(data.ani_num);
        $('input[name=title]').val(data.title);
        $('.added_genres').append(data.genres);
    });

    $('.title').focus();
};

$.get('/work', function() {
	$.get('/work/rand_anime',function(data) {
		$('.added_ani_num').val(data.ani_num);
		$('input[name=title]').val(data.title);
		$('.added_genres').append(data.genres);
	});
/*
	$.get('/image?ani_num=1429', function(data) {
		$('.added_img').attr('src', "data:image/*;base64," + data);

	})

	$.ajax({
		type: 'GET',
		url: '/image?ani_num=1429',
		dataType: 'image/png',
		success: function(data) {
			$('.added_img').attr('src', "data:image/png;base64," + data);

		}
	});
	*/
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