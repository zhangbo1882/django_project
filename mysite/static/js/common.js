function processButn(){
    var elePass = document.getElementById("password");
    var eleUPass = document.getElementById("uPassword");
    var eleCheckCode = document.getElementById("checkcode");
    if(elePass){
        eleUPass.value = $.md5(elePass.value);
        elePass.disabled = true;    
    }
    if(eleCheckCode){
        //alert(eleCheckCode.value);
    }
}

function processReg(){
    var elePass = document.getElementById("password");
    var eleUPass = document.getElementById("uPassword");
  
    if(elePass){
        eleUPass.value = $.md5(elePass.value);
        elePass.disabled = true;    
    }
}

function sendMessage(){
    var eleMobile = document.getElementById("mobile");
    if(eleMobile && eleMobile.value == ''){
        eleMobile.focus();
        return false;
    }
    var data = {
      "mobile" : eleMobile.value
    };
    var callBack = function(result){
        if(result == 200){
            alert("验证码已经发送，请在5分钟内使用");
        }else{
            alert("发送验证码失败");
        }
    }
     $.get("/account/sendsms/", data, callBack, "json");
 }