chrome.identity.getProfileUserInfo(userInfo => {
	$("#greeting").html("Hello, " + "<b>" + userInfo.email + "</b>" +
		"<br>" + "Profiler is recording your history")
})


// window.onload = function() {
// 	document.querySelector('#greeting').addEventListener('mouseover', function() {
// 			chrome.identity.getAuthToken({interactive: true}, function(token) {
// 				console.log(token);
// 			});
// 	});
// };