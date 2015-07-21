$(document).ready(function() {
	$("input[name='usage_table']").click(function() {
		if (this.id == "custom_usage") {
			$("#custom_table").show('fast');
		} else {
			$("#custom_table").hide('fast');
		}
	});
});


$(document).ready(function() {
	$("input[name='compression_method']").click(function() {
		if (this.id == "rank") {
			$("#input_rank").show('fast');
			$("#input_usage").hide('fast');
		} else {
			$("#input_usage").show('fast');
			$("#input_rank").hide('fast');
		}
	});
});



function selectUsageTable() {
	var show_upload_button = document.getElementById("custom_table");
	show_upload_button.setAttribute("style", "display:block");
}


function postEmailWarning() {
	var invalid_email = document.getElementById("invalid_email");
	invalid_email.setAttribute("style", "color:white;", "font-size:20px;");
	invalid_email.innerHTML = "The input is not a valid email address";
}

function removeEmailWarning() {
	var invalid_email = document.getElementById("invalid_email");
	invalid_email.innerHTML = "";
}

function myFunction() {
	var email = document.getElementsByName("submitter_email")[0].value;
	var alpha_num_pattern = /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i;
	var result = email.match(alpha_num_pattern);
	if (email.match(alpha_num_pattern) != null) {
		removeEmailWarning()
	} else {
		postEmailWarning()
	}
	console.log(email);
	console.log(result);
}