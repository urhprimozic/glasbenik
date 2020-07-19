function playButton(x, a){
    if(a == 1) x.style.filter = "invert(81%) sepia(83%) saturate(1373%) hue-rotate(326deg) brightness(100%) contrast(103%)";
    else x.style.filter = "none";
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