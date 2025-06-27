/*
Show and hide the navigation bar whenever the 'Menu' button is clicked on portrait mode,
do not hide the navigation bar on landscape mode
*/
// Check for clicks on the 'Menu' button
$("button.menu").click(function () {
    // Check if the navigation bar is showing(display: flex) or if it's hidden(display: none)
    // and change the 'Menu' button's icon accordingly
    if ($("div.links-container").css("display") === "flex") {
        $("svg.menu-icon").html([
            '<path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 ',
            '.5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 ',
            '0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5',
            '0 0 1-.5-.5"/> Menu'
        ].join(""));
    } else {
        $("svg.menu-icon").html([
            '<path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 ',
            '.708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 ',
            '0 0 1-.708-.708L7.293 8z"/> Menu'
        ].join(""));
    }
    // Animate the navigation bar's show/hide process to slide out/in
    $("div.links-container").slideToggle();
})


// If the page orientation changes from landscape to portrait mode
// and the navigation bar is not hidden, hide the navigation bar, and
// if the page orientation changes from portrait to landscape mode and the
// navigation bar is hidden, unhide the navigation bar
var screenOrientation = window.matchMedia("(orientation: portrait)");
screenOrientation.addEventListener("change", detectChange)


function detectChange(portraitState) {
    if (portraitState.matches) {
        $("div.links-container").css("display", "none");
        $("svg.menu-icon").html([
            '<path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 ',
            '.5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 ',
            '0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5',
            '0 0 1-.5-.5"/> Menu'
        ].join(""));
    } else {
        if ($("div.links-container").css("display") === "none") {
            $("div.links-container").css("display", "flex");
        }
    }
}


detectChange(screenOrientation);






//$(".betan").click(function () {
//    fetch("http://127.0.0.1:5000/flow/api").then(function (response) {
//        return response.json();
//    }).then(function (data) {
//        $(".details-shower").html([
//            ("Your first name is " + data["first name"] + ", your last name "),
//            ("is " + data["last name"] + ", and your email is " + data["email"] + ", "),
//            ("Your is image is " + "<img width='500vw' height='500vw' src='" + data["picture url"] + "'>" )
//        ].join(""));
//    })
//})









