$(document).ready(function() {

        $( ".smiley_box .slider" ).slider({
            value:1,
            min: 1,
            max: 5,
            step: 1,
            slide: function( event, ui ) {
                $(event.target).prev("input").val( ui.value );
            }
        });
        $(".smiley_box input").hide();
	
});