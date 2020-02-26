window.$ = window.jQuery = require('jquery');
handlebars = require("handlebars");

let url ="http://localhost:8000/api/"
let TOKEN = "45dd454f58fae44d5289e49ca2823de424df1afb"



//configure
$.ajaxSetup({
    beforeSend: function(xhr) {
        xhr.setRequestHeader('Authorization', 'Token '+ TOKEN);
    }
});

// helpers

let render = (element_id, context) => {
    let template_account = document.getElementById(element_id).innerHTML;
     let tmpl = handlebars.compile(template_account)
        let html = tmpl(context);
    return html;

}




var detail = (account_id, id) => {
     $.getJSON(url + `accounts/${account_id}/hosts/${id}`, (resp)=>{
        let res = "detail";
        $("#main").html(res);
    })


}

var fetch_account = (id) => {
     $.getJSON(url + "accounts/"+ id + "/hosts/", (resp)=>{
         let context = {
             'account_id': id,
             'data': resp,
         }
        let res = $("<div>").html(render("list_hosts", context));
        $("#main").html(res);
    })

}


var main = ()=>{
    $.getJSON(url + "accounts/", (resp)=>{
        let res = $("<div>").html(render("list_account", resp));
        $("#main").html(res);
    })

}

window.fetch_account = fetch_account;
window.main = main
window.detail = detail

$(document).ready(()=>{
    console.log("document ready");
    main();
});

