function emoji_change(e){
// 이모지 클릭시, 내 이모지 span 내용 변경
    document.getElementById('selected_emoji').innerText = e.innerText;
};

function emoji_save(){
    let new_emoji = document.getElementById('selected_emoji').innerText;
    window.location.href = '/accounts/emoji_modify/'+new_emoji;
};