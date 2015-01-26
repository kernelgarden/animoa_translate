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

PostAnimeData = function() {
	$.ajax({
		type: 'POST',
		url: '/work/',
		data: jsonString,
		dataType: 'json',
		error: function (error) {
			console.log('error : ' + error);
		}
	});


/*
	var anime_image = $('.added_img').files;
	var data = false;
	data = new FormData();

	data.append("type", 0);
	data.append("ani_num", $(".added_ani_num").val());
	data.append("file", anime_image);
	$.ajax({
		type: 'POST',
		url: '/image',
		data: data
	})
	console.log(data);
*/
/*
	for(var i=0; i < img_info.length; i++) {
		$.ajax({
			type: 'POST',
			url: '/image?type=1&ani_num=' + $(".added_ani_num") + '(&' + img_info[i] + ')',
			data: // 애니 이미지
	}
*/
}

$.get('/work', function() {
	console.log('work page');
	GetRandomAnime();
});