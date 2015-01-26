form_data = function() {
	var jsonObj = [];

	// ost value
	var ost_obj = [];
    $(".ost_info").each(function() {
        var ost_name = $(this).children('.ost_name').val();
        var ost_type = $(this).children('.ost_type option:selected').val();
        
        var item = {};
        item["name"] = ost_name;
        item["type"] = ost_type;
        ost_obj.push(item);
    });

    // character value
    var character_obj = [];
    $('.character_info').each(function() {
    	var cha_name = $(this).children('.cha_name').val();
    	var cha_voice = $(this).children('.cha_voice').val();
    	var cha_desc = $(this).children('.cha_desc').val();

    	var item = {};
    	item["name"] = cha_name;
    	item["desc"] = cha_desc;
    	item["voice_name"] = cha_voice;
    	character_obj.push(item);
    });

    var ba_class_value, precise_value, nation_value;
    if( $('input:radio:checked[name=ba_class]').val() == undefined ) ba_class_value=""
    	else ba_class_value=$('input:radio:checked[name=ba_class]').val();
    if( $('input:radio:checked[name=precise]').val() == undefined ) precise_value=""
    	else precise_value=$('input:radio:checked[name=precise]').val();
    if( $('input:radio:checked[name=nation]').val() == undefined ) nation_value=""
    	else nation_value=$('input:radio:checked[name=nation]').val();
    
	jsonObj.push({//ani_id: int,
		title: $('input[name=title]').val(),
		origin_title: $('input[name=origin_title]').val(),
		en_title: $('input[name=en_title]').val(),
		sub_title: $('input[name=sub_title]').val(),
		director: $('input[name=director]').val(),
		production: $('input[name=production]').val(),
		copyright: $('input[name=copyright]').val(),
		genres: $('input:checkbox:checked[name=genre]').map(function () { return this.value }).get(),
		year: $('input[name=year]').val() * 1,
		ba_class: ba_class_value, 
		precise: precise_value,
		epi_num: $('input[name=epi_num]').val() * 1,
		running_time: $('input[name=running_time]').val() * 1, 
		nation: nation_value, 
		ost: ost_obj,
		plot: $('textarea[name=plot]').val(),
		intro: $('textarea[name=intro]').val(),
		characters: character_obj,
        ani_num: $('.added_ani_num').val()
	})

	jsonString = JSON.stringify(jsonObj);
}