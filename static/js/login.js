
// console.log(document.getElementbyId('id').innerText)

function signIn(){
    var makeId = $('#make_id').val()
    var makePw = $('#make_pw').val()
    var makeEmail = $('#make_email').val()
    $.ajax({
        type: "POST",
        data: {'id_give': makeId, 'pw_give': makePw, 'email_give': makeEmail},
        url: "/signin",
        success: function(response){
            console.log(response)

        }
    })
}

function logIn(){
    var loginId = $('#login_id').val()
    var loginPw = $('#login_pw').val()
$.ajax({
    type: "POST",
    data: {'id_check': loginId, 'pw_check': loginPw},
    url: "/login",
    success: function(response){
        console.log(response)

    }
    })
}