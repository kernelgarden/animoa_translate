
var genre =
[
    '3D 애니', 'SF', '구조물', '갱스터', '다큐멘터리', '단편', '드라마', '레이싱', '로맨스', '로봇', '마법', '메이드', '메카닉', '뮤지컬', '미스테리', '범죄물', '서부영화', '성인물', '스릴러', '스포츠', '시대물', '아동물', '액션', '어드벤쳐', '위인전', '전쟁물', '코메디', '클레이메이션', '학원물', '호러물', '판타지', '변신', 'BL(Boys Love)'
];

var precise =
[
    'TV', 'TV-Movies', 'OVA', 'ONA', 'Movie', 'Game', 'Music Video'
];

var ba_class =
[
    'BA-7', 'BA-13', 'BA-17', 'BA-R'
];

for(var i=0; i < genre.length; i++)
    $('.genre').append('<div class="col-md-2"><input type="checkbox" name="genre" value="' + genre[i] + '" />' + '<label>' + genre[i] + '</label>');
for(var i=0; i < ba_class.length; i++)
    $('.ba_class').append('<input type="radio" name="ba_class" value="' + ba_class[i] + '" />' + '<label>' + ba_class[i] + '</label>');

for(var i=0; i < precise.length; i++)
    $('.precise').append('<input type="radio" name="precise" value="' + precise[i] + '" />' + '<label>' + precise[i] + '</label>');

var CharacterCount = 0;
$('.add-character').click(function()
    {
        ++CharacterCount;
        $('.character-form-div').append('<div><button type="button" id="character-'+ CharacterCount + '" class="minus-button glyphicon glyphicon-minus btn btn-default" onclick=RemoveForm(this.id)></button><label>캐릭터 이미지</label><input type="file" name="pic" accept="image/jpg"><div class="character_info"><input class="cha_name add-form form-control col-md-6" type="text" placeholder="캐릭터 이름" /><input class="cha_voice add-form form-control col-md-6" type="text" placeholder="성우" /><textarea id="character-focus-' + CharacterCount + '"class="cha_desc add-form form-control col-md-12" placeholder="캐릭터 설명"></textarea></div></div>');
        setTimeout(function(){
            $('#character-focus-' + CharacterCount).focus();
        }, 0);
    });

var OstCount = 0;

$('.add-ost').click(function()
    {
        ++OstCount;
        $('.ost-form-div').append('<div><button type="button" id="ost-'+ OstCount + '" class="minus-button glyphicon glyphicon-minus btn btn-default" onclick=RemoveForm(this.id)></button><div class="ost_info"><select class="ost_type"><option value="1">오프닝</option><option value="2">엔딩</option><option value="3">수록곡</option></select><input id="ost_focus-' + OstCount + '" class="ost_name add-form form-control" type="text" placeholder="곡 이름" /></div></div>');
        setTimeout(function(){
            $('#ost-focus-' + OstCount).focus();
        }, 0);
    });

var RemoveForm = function(id) {
    $('#'+id).parent().remove();
}

var ResetChecked = function(id) {
    $('#'+id).parent().find("input:radio").removeAttr('checked');
}

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
            console.log('submit');
        } else {
            console.log('fuck');
        }

    });
$(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
});



