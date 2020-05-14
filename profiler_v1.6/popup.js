chrome.identity.getProfileUserInfo(info => {
	$("#greeting").html("Hello, " + "<b>" + info.email + "</b>" +
		"<br>" + "Profiler is recording your history")
})