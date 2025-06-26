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
