
// console.log(document.getElementbyId('id').innerText)

function register_finish(){
    setTimeout("document.a.submit()", 5000);
    var makeId = $('#make_id').val()
    console.log(makeId)
    var makePw = $('#make_pw').val()
    console.log(makePw)

    $.ajax({
        type: "POST",
        data: {'id_give': makeId, 'pw_give': makePw},
        url: "/register",
        success: function(response){
            console.log(response)
           if(response['result'] === 'success'){
            alert(response['msg'])
           } else{
            alert(response['msg'])
           }
            }
    })
}

function logIn(){
    setTimeout("document.a.submit()", 5000);
    var loginId = $('#login_id').val()
    var loginPw = $('#login_pw').val()
$.ajax({
    type: "POST",
    data: {'id_check': loginId, 'pw_check': loginPw},
    url: "/login",
    success: function(response){
        if (response['result']=='fail'){
            alert(response['msg'])
        }else{
        alert("잘 입력했음")
    }
    }  
    })
}
// $(document).ready(function () {
//     logIn();
// });
function loginClick(){
    $.ajax({
        type: "GET",
        url: "/login",
        data: {},
        success: function(response){
            console.log(response)
        }
    })
}