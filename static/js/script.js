/* static/js/script.js */

$(document).ready(function(){
    var ws = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/ws");
    
    ws.onmessage = function(event) {
        var message = event.data;
        $('#messages').append('<p>' + message + '</p>');
    };
});
