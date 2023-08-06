/* <script src="{{ url_for('static',filename='js/csharpRouting.js') }}"></script> */


/* SECTION - [data-controller] & [data-action] */
elements = document.querySelectorAll("[data-controller]");
elements.forEach(element => {
    
    actionString = "/";
    
    if(element.dataset.controller != null && element.dataset.action != null) {
        actionString += element.dataset.controller + "/" + element.dataset.action + "/";
        element.removeAttribute("data-controller");
        element.removeAttribute("data-action");
    }
    else{
        actionString = "Missing [data-controller] OR [data-action]";
    }

    // Check what element type we are dealing with, to set the correct attribute
    switch(element.nodeName) {
        case "A":
            console.log("A");
            element.href = actionString;
            break;

        case "FORM":
            console.log("FORM");
            element.action = actionString;
            break;
    }    
});