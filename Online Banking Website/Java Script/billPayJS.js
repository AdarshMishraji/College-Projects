function goto () {
    document.getElementById( "paybtn" ).style.borderStyle = "inset";
    if (document.getElementById("billno").value.length==0||document.getElementById("rupee").value.length==0)
    {   
        document.getElementById( "error" ).innerHTML = "Above Fields are blank.";
        document.getElementById( "error" ).style.color = "red";
        document.getElementById( "error" ).style.textDecoration = "underline";
        document.getElementById( "paybtn" ).style.borderStyle = "outset";
    }
    else
    {
        document.getElementById( "error" ).innerHTML = "";
        alert( "Bill had paid successfully!!." );
        window.location.replace( "home.html" );
    }
}
