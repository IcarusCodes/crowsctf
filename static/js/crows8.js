function notTheFlagXSS() {
    console.log("macar_atat");
    var x = document.createElement("VAR");
    var t = document.createTextNode("Some text..");
    x.appendChild(t);
    document.body.appendChild(x);
}

notTheFlagXSS();