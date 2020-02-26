window.$ = window.jQuery = require('jquery');

url ="http://localhost:8000/api/"
TOKEN = "45dd454f58fae44d5289e49ca2823de424df1afb"


$.ajaxSetup({
    beforeSend: function(xhr) {
        xhr.setRequestHeader('Authorization', 'Token '+ TOKEN);
    }
});

$(document).ready(()=>{
    console.log("document ready");

    $.getJSON(url + "accounts/", (resp)=>{
        console.log(resp);
    })

});

