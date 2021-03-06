window.$ = window.jQuery = require('jquery');
handlebars = require("handlebars");
chartjs = require("chart.js");
_ = require("lodash")

let url ="http://localhost:8000/api/"
let TOKEN = "f0f4a0c4dcda16c1bd48365998985da0fa9d74f5"

//configure
$.ajaxSetup({
    beforeSend: function(xhr) {
        xhr.setRequestHeader('Authorization', 'Token '+ TOKEN);
    }
});

handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
        return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
});

// helpers
let render = (element_id, context) => {
    let template_account = document.getElementById(element_id).innerHTML;
    let tmpl = handlebars.compile(template_account)
    let html = tmpl(context);
    return html;
}


var build_graph = (context) => {
    var ctx = document.getElementById('myChart').getContext('2d');
    var opts =  {
        'type':'line',
        'data': {
            'labels': _.map(context.data.summary, "time"),
             'datasets': [
                 {
                    'label':' Load',
                    'data': _.map(context.data.summary, "mean_rtt_avg")
                 }
             ]
        },
		'options':{
                        responsive: false,
                        width:500,
                        height:300,
                        scaleShowGridLines: false,
                        showScale: false,
                        maintainAspectRatio: this.maintainAspectRatio,
                        barShowStroke: false}
    }
    var chart = new chartjs(ctx,opts);

}

var detail = (account_id, id , type) => {
    $.getJSON(url + `accounts/${account_id}/hosts/${id}/result/`, (resp)=>{
        let context = {
             'account_id': account_id,
             'data':resp
        }
        if ( type === "ping") {
            let res = render("detail_ping", context);
            $("#main").html(res);
            build_graph(context);
        }
        if (type==="black") {
            let res = render("detail_blacklist", context);
            $("#main").html(res);

        }
   });
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

