
var genre =
[
    '3D 애니', 'SF', '구조물', '갱스터', '다큐멘터리',
    '단편', '드라마', '레이싱', '로맨스', '로봇', '마법',
    '메이드', '메카닉', '뮤지컬', '미스테리', '범죄물',
    '서부영화', '성인물', '스릴러', '스포츠', '시대물',
    '아동물', '액션', '어드벤쳐', '위인전', '전쟁물',
    '코메디', '클레이메이션', '학원물', '호러물', '판타지',
    '변신', 'BL', '일상'
];

var precise =
[
    'TV', 'TV-Movies', 'OVA', 'ONA', 'Movie',
    'Game', 'Music Video', 'PV'
];

var ba_class =
[
    'BA-7', 'BA-13', 'BA-17', 'BA-R'
];

for(var i=0; i < genre.length; i++)
    $('.genre').append(
        '<div class="col-md-2"><input type="checkbox" name="genre" value="' + genre[i] + '" />' + '<label>' + genre[i] + '</label>');
for(var i=0; i < ba_class.length; i++)
    $('.ba_class').append(
        '<input type="radio" name="ba_class" value="' + ba_class[i] + '" />' + '<label>' + ba_class[i] + '</label>');

for(var i=0; i < precise.length; i++)
    $('.precise').append('<input type="radio" name="precise" value="' + precise[i] + '" />' + '<label>' + precise[i] + '</label>');

var CharacterCount = 0;
$('.add-character-btn').click(function()
    {
        CharacterCount++;
        $('.character-form-div').append('<div class="added character_info"><button type="button" id="character-'+ CharacterCount + '" class="minus-button glyphicon glyphicon-minus btn btn-default" onclick="RemoveForm(this.id)"></button><label>캐릭터 이미지</label><input class="added_character_img" type="file" name="pic" accept="image/jpg"><input class="cha_name add-form form-control col-md-6" type="text" placeholder="캐릭터 이름" /><input class="cha_voice add-form form-control col-md-6" type="text" placeholder="성우" /><textarea class="cha_desc add-form form-control col-md-12" placeholder="캐릭터 설명"></textarea></div>');
    });

var OstCount = 0;
$('.add-ost-btn').click(function()
    {
        OstCount++;
        $('.ost-form-div').append('<div class="added ost_info"><button type="button" id="ost-'+ OstCount + '" class="minus-button glyphicon glyphicon-minus btn btn-default" onclick=RemoveForm(this.id)></button><select class="ost_type"><option value="1">오프닝</option><option value="2">엔딩</option><option value="3">수록곡</option></select><input class="ost_name add-form form-control" type="text" placeholder="곡 이름" /></div>');
    });

var RemoveForm = function(id) {
    $('#'+id).parent().remove();
}

var ResetChecked = function(id) {
    $('#'+id).parent().find("input:radio").removeAttr('checked');
}


ClearForm = function() {

    $(':input')
     .not(':button, :submit, :reset, :hidden, :checkbox, :radio')
     .val('');

    $(':input')
     .not(':button, :submit, :reset, :hidden')
     .removeAttr('checked')
     .removeAttr('selected');

    $('.added').each(function() {
        $(this).remove();
    })

    $('.added_genres').html('');

    $('.title').focus();
};

form_data = function() {
    var jsonObj = [];

    // ost value
    var ost_obj = [];
    $(".ost_info").each(function() {
        var ost_name = $(this).children('.ost_name').val();
        var ost_type = $(this).find('.ost_type option:selected').val();
        
        var item = {};
        item["name"] = ost_name;
        item["type"] = ost_type;
        ost_obj.push(item);
    });

    // character value
    var character_obj = [];
    character_image = [];
    $('.character_info').each(function() {
        var cha_name = $(this).children('.cha_name').val();
        var cha_voice = $(this).children('.cha_voice').val();
        var cha_desc = $(this).children('.cha_desc').val();
        
        var cha_img = $(this).children('.added_character_img').val();
        var cha_has_img = 0;        

        if(cha_img != "") {
            cha_has_img = 1;
        }  

        var item = {};
        item["name"] = cha_name;
        item["desc"] = cha_desc;
        item["voice_name"] = cha_voice;
        item["has_image"] = cha_has_img;
        character_obj.push(item);
        
        var img_info = {};
        img_info["ani_num"] = $('.added_ani_num').val();
        img_info["character_name"] = cha_name;

        character_image.push(img_info);
    });

    var ba_class_value, precise_value, nation_value;
    if( $('input:radio:checked[name=ba_class]').val() == undefined ) ba_class_value=""
        else ba_class_value=$('input:radio:checked[name=ba_class]').val();
    if( $('input:radio:checked[name=precise]').val() == undefined ) precise_value=""
        else precise_value=$('input:radio:checked[name=precise]').val();
    if( $('input:radio:checked[name=nation]').val() == undefined ) nation_value=""
        else nation_value=$('input:radio:checked[name=nation]').val();
    
    jsonObj.push({
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

$('.pass-button').click(function()
{
    ClearForm();
    GetRandomAnime();
    console.log('pass');
})
$('.form-submit').click(function()
{
    var episode = $('.check-format-episode-num');
    var runningtime = $('.check-format-running-time');
    var year = $('.check-format-year');
    var check1 = /^[0-9]*$/;
    var check2 = /^(\d{4}|[ ]{0,4})$/;
    if(!check1.test(episode.val()))
    {
        episode.css({
            'border-color': 'red'
        }).focus();
    } else {
        episode.css({
            'border-color': '#ccc'
        })
    }
    if(!check1.test(runningtime.val())) 
    {
        runningtime.css({
            'border-color': 'red'
        }).focus();
    } else {
        runningtime.css({
            'border-color': '#ccc'
        })
    }
    if(!check2.test(year.val())) 
    {
        year.css({
            'border-color': 'red'
        }).focus();
    } else {
        year.css({
            'border-color': '#ccc'
        })
    }

    if(check1.test(episode.val()) && check1.test(runningtime.val()) && check2.test(year.val()))
    {
        form_data();
        PostAnimeData();
        ClearForm();
        GetRandomAnime();
        console.log('submit');
        console.log(jsonString);
    } else {
        episode.focus();
    }

});




