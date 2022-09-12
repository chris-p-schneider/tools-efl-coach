// teflc-scripts.js
/*eslint-env browser*/

///////////////////////////////////////////
// NAV BAR HIDE & SHOW
var navHidden = false;
function toggleNav() { // eslint-disable-line no-unused-vars
    "use strict";
    if (navHidden === false) {
        document.getElementById("nav").style.maxHeight = "0px";
        document.getElementById("nav").style.overflow = "hidden";
        navHidden = true;
    } else if (navHidden === true) {
        document.getElementById("nav").style.maxHeight = "100px";
        document.getElementById("nav").style.overflow = "visible";
        navHidden = false;
    }
}

///////////////////////////////////////////
// APP ICON STYLING ON HOVER
function iconDisplay(icon) { // eslint-disable-line no-unused-vars
    "use strict";
    var appIcon = icon.children;
    appIcon[0].children[0].style.opacity = "100%";
    appIcon[1].style.zIndex = "-1";
}
function iconRevert(icon) { // eslint-disable-line no-unused-vars
    "use strict";
    var appIcon = icon.children;
    appIcon[0].children[0].style.opacity = "50%";
    appIcon[1].style.zIndex = "2";
}

///////////////////////////////////////////
// ADDS FADE OUT ANIMATION CLASS
function alertFadeOut(alert) {
    if (alert.classList.contains("alert-success")) {
        alert.className = "alert-success no-select fade-out";
    }
    else if (alert.classList.contains("alert-fail")) {
        alert.className = "alert-fail no-select fade-out";
    }
    else if (alert.classList.contains("alert")) {
        alert.className = "alert no-select fade-out";
    }
    else if (alert.classList.contains("font18")) {
        alert.className = "status-para font18 no-select fade-out";
    }
    else if (alert.classList.contains("font16")) {
        alert.className = "status-para font16 no-select fade-out";
    }
    // alert.style.display = "none";
}
// HIDES ALERT ELEMENT
function removeAlert(alert) {
    alert.style.display = "none";
}
// CLEAR ALERTS
function clearAlert(alert) { // eslint-disable-line no-unused-vars
    "use strict";
    alertFadeOut(alert);
    setTimeout(removeAlert, 500, alert);
}

///////////////////////////////////////////
// NEW PROFILE PIC UPLOAD
function uploadPic() { // eslint-disable-line no-unused-vars
    "use strict";
    var photoUpload = document.getElementsByClassName("user-form-photo");
    photoUpload[0].click();
    //alert("hey");
}

///////////////////////////////////////////
// CONFIRM DELETE BUTTON
let confirmDeleteBool = false;
function confirmDelete() {
    "use strict";
    let deleteButton = document.getElementById("delete-list-button");
    if (confirmDeleteBool === false) {
        deleteButton.className = "inline-block";
        confirmDeleteBool = true;
    } else {
        deleteButton.className = "hidden";
        confirmDeleteBool = false;
    }
}

///////////////////////////////////////////
// YOUTUBE CLICK
var showVideoBool = false;
function youtubeClick() {
    "use strict";
    var youtubeVideo = document.getElementById("hot-seat-youtube");
    if (showVideoBool === false) {
        youtubeVideo.style.zIndex = "5";
        showVideoBool = true;
    }
    else {
        youtubeVideo.style.zIndex = "-5";
        showVideoBool = false;
    }
}

///////////////////////////////////////////
//WORD VERIFICATION FUNCTIONS

///////////////////////////////////////////
// WORD VERIFICATION UPLOAD IMAGE BUTTON
function wordVerificationImageUpload() { // eslint-disable-line no-unused-vars
    "use strict";
    var photoUpload = document.getElementById("word-verification-image-upload");
    photoUpload.click();
}



///////////////////////////////////////////
// TESTING

// CHECK WINDOW SIZE
// window.onresize = function() {
    // let w = window.innerWidth,
        // h = window.innerHeight,
        // Test element here:
        // a = document.getElementById("window-size");

    //  a.innerHTML = w + "w &times " + h + "h";
// }
