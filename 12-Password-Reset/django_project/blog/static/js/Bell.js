var down = false;

function startshakebell() {
    document.getElementById("Bell").className = "fas fa-bell fa-beat fa-shake";
}
  
function stopshakebell() {
    document.getElementById("Bell").className = "fas fa-bell";
}

function BellClicked() {
    var box = document.getElementById("Box");
    if (down) {
        box.style.height = '0px';
        box.style.display = 'none';
        down = false;
    } else {
        box.style.height = 'auto';
        box.style.display = 'block';
        down = true;
    }
}