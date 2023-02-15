function register_finish(){
    var makeId = $('#make_id').val()
    var makePw = $('#make_pw').val()
    $.ajax({
        type: "POST",
        data: {'id_give': makeId, 'pw_give': makePw},
        url: "/register",
        success: function(response){
           if(response['result'] == 'success'){
            alert(response['msg'])
            register_pass()
        } else{
            alert(response['msg'])
            register_fail()
        }
    }
})
}

var registerForm = document.getElementById("register_form")
function register_pass(){
    registerForm.action = "/"
    registerForm.method = "GET"
    registerForm.submit();

}
function register_fail(){
    registerForm.action = "/"
    registerForm.method = "GET"
    registerForm.submit();
}
function logIn(){
    var loginId = $('#login_id').val()
    var loginPw = $('#login_pw').val()
$.ajax({
    type: "POST",
    data: {'id_check': loginId, 'pw_check': loginPw},
    url: "/login",
    success: function(response){
        if (response['result']=='fail'){
            alert(response['msg'])
            login_pass()
        }else{
        alert("로그인 완료!")
        login_fail()
    }
    }  
    })
}
var loginForm = document.getElementById("login_form")
function login_pass(){
    loginForm.action = "/"
    loginForm.method = "GET"
    loginForm.submit();

}
function login_fail(){
    loginForm.action = "/register"
    loginForm.method = "GET"
    loginForm.submit();
}

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