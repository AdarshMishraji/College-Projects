function load () {
    wrong();
}
function wrong () {
    document.getElementById( "paybtn" ).disabled = true;
    document.getElementById( "paybtn" ).style.opacity = "0.5";
}
function right () {
    document.getElementById( "paybtn" ).disabled = false;
    document.getElementById( "result" ).innerHTML = "";
    document.getElementById( "paybtn" ).style.opacity = "1";
}
function validAcc () {
    var accno = document.getElementById( "accno" ).value;
    if ( /[0-9]/.test( accno ) == true && ( accno.length != 16 ) )
    {
        document.getElementById( "result" ).innerHTML = "Account No. should be of 16 numeric characters.";
        wrong();
        document.getElementById( "accno" ).focus();
        return false;
    }
    else
    {
        document.getElementById( "result" ).innerHTML = "";
        // right();
        return true;
    }
}
function validCard () {
    var card = document.getElementById( "cardno" ).value;
    if ( /[0-9]/.test( card ) == true && ( card.length != 16 ) )
    {
        document.getElementById( "result" ).innerHTML = "Card No. should be of 16 numeric characters.";
        wrong();
        document.getElementById( "cardno" ).focus();
        return false;
    }
    else
    {
        document.getElementById( "result" ).innerHTML = "";
        // right();
        return true;
    }
}

function goto () {
    var rupee = document.getElementById( "rupee" ).value.length;
    var name = document.getElementById( "name" ).value.length;
    if ( validAcc() == true && validCard() == true && rupee == 0 && name == 0 )
    {
        document.getElementById( "result" ).innerHTML = "Some input fields have undesired values.";

        return false;
    }
    else
    {
        alert( "Deposited..." );
        window.location.replace( "home.html" );
        return true;
    }
}