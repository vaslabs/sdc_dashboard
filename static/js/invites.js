$('#invitation-apply a').click(function() {
	var url = '/invites/validate_invitation_token/';
	var data = {'invitation_token': $('#invitation-token-holder input').val()}
	getJSONPostResponse(url, data, function(pdata) {next_step(pdata, showUsernameTemplate);});
});

function register_click(widget_selector, url, callback, key_inputSelector) {
	$(widget_selector).click(function() {
		var data = {};
		$.each(key_inputSelector, function(key, selector) {
			data[key] = $(selector).val();
		});
		getJSONPostResponse(url, data, function(pdata) {next_step(pdata, callback);});
	});
}

function next_step(data, success_callback) {
	if (data.message == 'OK') {
		$('#invites-error-holder').css('display', 'none');
		success_callback();
	} else {
		showInvalidMessage(data.message);
	}
}

function showUsernameTemplate() {
	constructUI(2, "username", "username");
	var selectorMap = {'username':'#invitation-username-holder input'};
	register_click('#invitation-username-apply a', '/invites/username/', showEmailTemplate, selectorMap);
}

function showEmailTemplate() {
	constructUI(3, "email", "email");
	var selectorMap = {'email':'#invitation-email-holder input'};
	register_click('#invitation-email-apply a', '/invites/email/', showPasswordTemplate, selectorMap);

}

function showPasswordTemplate() {
	constructUI(4, "password", "password", true);
	var selectorMap = {'password':'#invitation-password-holder input'};
	register_click('#invitation-password-apply a', '/invites/password/', showValidationPasswordTemplate, selectorMap);
}

function passwordsMatch() {
	return $('#invitation-password-holder input').val() == $('#invitation-validationpassword-holder input').val();
}

function showValidationPasswordTemplate() {
	constructUI(5, "validationpassword", "Retype password", true);
	$('#invitation-validationpassword-apply a').click(function() {
		if (passwordsMatch()) {
			$('#invites-error-holder').css('display', 'none');

			var url = '/invites/register_user/';
			var data = {'invitation_token': $('#invitation-token-holder input').val(),
						'username':$('#invitation-username-holder input').val(),
						'password':$('#invitation-password-holder input').val(),
						'email':$('#invitation-email-holder input').val()};
			getJSONPostResponse(url, data, function(pdata) {next_step(pdata, showRegistrationSuccessTemplate);});
		} else {
			showInvalidMessage("Passwords do not match");
		}

	});
	
}

function showRegistrationSuccessTemplate() {
	$('#registration-success').css({'display':'block'});
	$('#registration-success div').css({'display':'block'});

}



function constructUI(stepIndex, widget_name, placeholder, password) {
	if (password == null) {
		password = false;
	}
	var previousStep = stepIndex - 1;
	$('#step-'+ previousStep + '-holder').css({'display':'none'});
	var stepholder = '#step-' + stepIndex + '-holder'
	jQuery('<div/>', {
	    id: 'invitation-' + widget_name + '-holder',
	    class: "small-10 columns"
	}).appendTo(stepholder);
	
	$('#invitation-' + widget_name + '-holder input').change(function() {
		$('#invites-error-holder').css('display', 'none');
	});

	jQuery('<input/>', {
		type: password ? 'password' : 'text',
		placeholder: placeholder
	}).appendTo('#invitation-'+widget_name+'-holder');

	jQuery('<div/>', {
	    id: 'invitation-' + widget_name + '-apply',
	    class: "small-2 columns"
	}).appendTo(stepholder);
	
	jQuery('<a/>', {
		href:'#',
		class: 'button postfix',
		text: 'Go'
	}).appendTo('#invitation-' + widget_name + '-apply');
	
	
}

function showInvalidMessage(message) {
	
	$('#invites-error-holder').css('display', 'block');
	$('#invites-error-holder').text(message);
}