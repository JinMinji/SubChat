function emoji_change(e){
// 이모지 클릭시, 내 이모지 span 내용 변경
    document.getElementById('selected_emoji').innerText = e.innerText
    document.getElementById('selected_emoji2').innerText = e.childNodes[1].value;
};

function emoji_save(){
    let new_emoji = document.getElementById('selected_emoji2').innerText;
    opener.location.href = '/profile/emoji_modify/'+new_emoji;
    window.close();
};