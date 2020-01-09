$(document).ready(function() {
    $("#submitButton").click(function(){
        $('.carousel').carousel(2); 
        document.getElementById('iframe').setAttribute('src', window.location + "testing?link=" + document.getElementById('getRequestInput').value);   
        console.log('FOXX afkhaduahskajshdkajshd gibdek');
    }); 
});