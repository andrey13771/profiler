chrome.identity.getProfileUserInfo(userInfo => {
	$("#greeting").html("Hello, " + "<b>" + userInfo.email + "</b>" +
		"<br>" + "Account Warden is recording your activity")
})


// window.onload = function() {
// 	document.querySelector('#greeting').addEventListener('mouseover', function() {
// 			chrome.identity.getAuthToken({interactive: true}, function(token) {
// 				console.log(token);
// 			});
// 	});
// };