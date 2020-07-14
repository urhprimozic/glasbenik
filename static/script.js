
function loading_dots(){
    var dots = window.setInterval( function() {
        var wait = document.getElementById("wait");
        if ( wait.innerHTML.length > 3 ) 
            wait.innerHTML = "";
        else 
            wait.innerHTML += ".";
        }, 100);
    }

function showPage() {
    document.getElementById("loader").style.display = "none";
    }
function loader() {
        document.getElementById("loader").style.display = "block";
    }
function loader_long() {
    document.getElementById("loader").style.display = "block";
    document.getElementById("opozorilo").style.display = "block";
}
function opozorilo(a) {
    if(a == 1) document.getElementById("opozorilo").style.display = "block";
    else document.getElementById("opozorilo").style.display = "none";
    }