	
	function reloadActions() {

		$("a[rel=popover]").popover();

		$("#plugin_feedbacks_submit").hide(); // standartmaeßig verstecken
		$("#plugin_feedbacks_feedback_message").hide(); // standartmaeßig verstecken
		$("#left_signs").hide(); // standartmaeßig verstecken
		$("#plugin_feedbacks_boxes label").addClass("btn btn-link"); // Buttonmaeßig machen
		$('#plugin_feedbacks_feedback_message').bind("keyup mouseup paste input", function(){
			var len = $(this).val().length;
			var curValue = $(this).val();
			if (140 - len < 0) {
				$(this).val(curValue.substring(0,140));
			} else {
				$("#left_signs").html(140-len);
			}
			
			if (len >= 1 && $('input[name=feeling]:checked').length) {
				$("#plugin_feedbacks_submit").show();
			} else {
				$("#plugin_feedbacks_submit").hide();
			}
		});
		
		
		
		$("#plugin_feedbacks_boxes input").change(function(){
			
			if( $("#plugin_feedbacks_feedback_message").is(':hidden') ) {
				$("#plugin_feedbacks_feedback_message").slideDown();
				$("#left_signs").show();
			}
			
			
			if ($(this).is(':checked')) {
				
				if ($(this).attr("id") == "feelingunhappy") {
					$("label[for=feelinghappy]").removeClass("btn-success").addClass("btn-link");
					$(this).next("label").addClass("btn-danger").removeClass("btn-link");
				} else {
					$("label[for=feelingunhappy]").removeClass("btn-danger").addClass("btn-link");
					$(this).next("label").addClass("btn-success").removeClass("btn-link");
				}
			}
			
			if ($('#plugin_feedbacks_feedback_message').val().length >= 1 && $('input[name=feeling]:checked').length) {
				$("#plugin_feedbacks_submit").show();
			} else {
				$("#plugin_feedbacks_submit").hide();
			}			
		});
	}
