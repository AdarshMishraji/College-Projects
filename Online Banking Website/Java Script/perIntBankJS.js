function right () {
    document.getElementById( "error" ).innerHTML = "";
}
function goto () {
    document.getElementById( "submitbtn" ).style.borderStyle = "inset";
    var x = document.getElementById( "accno" ).value;
    var y = document.getElementById( "amnt" ).value;
    if ( x.length == 16 && y <= 20000 && y >= 0 )
    {
        right();
        window.alert( "Rs." + document.getElementById( "amnt" ).value + " sent to the acc no: " + document.getElementById( "accno" ).value );
        window.location.replace( "home.html" );
    }
    else
    {
        document.getElementById( "error" ).innerHTML = "There was something wrong in the input fields.";
        document.getElementById( "accno" ).focus();
    }
} 