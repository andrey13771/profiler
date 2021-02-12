let suspicious_counter = 0;
let userId;

chrome.identity.getProfileUserInfo(info => {
	userId = info.id;
})

chrome.runtime.onInstalled.addListener(function(details) {
	if (details.reason === 'install') {
		// alert('sending history');
		chromep.history.search({text: '', startTime: 0, maxResults: 0})
			.then(historyItems => {
					historyItems.forEach(item => {
						$.post('http://localhost:5000/save_url', {
							reason: 'install',
							url: item.url
						}).fail(xhr => {
							alert('Error occured while processing your history: ' + xhr.status +
								' ' + xhr.statusText);
						});
					});
					// alert('history finished sending');
				});
	}
});


chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
	let url = changeInfo.url;
	if (tab.active && url !== undefined && !url.startsWith("chrome://")) {
		$.post('http://localhost:5000/save_url', {
			reason: 'navigate',
			url: url
		}).then(response => {
			let msg = response.message
			if (msg === "suspicious url") {
				suspicious_counter += 1
				if (suspicious_counter === 5) {
					alert('suspicious activity');
				}
			} else if (msg === "saved url") {
				suspicious_counter = 0
			}
		})
	}
});