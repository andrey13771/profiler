const HOST_URL = 'http://localhost:5000/'
let suspiciousCounter = 0
let userId

let onInstalled = details => {
	if (details.reason === 'install') {
		// alert('sending history');
		chromep.history.search({text: '', startTime: 0, maxResults: 0})
			.then(historyItems => {
				historyItems.forEach(item => {
					$.post(`${HOST_URL}save_url`, {
						reason: 'install',
						url: item.url,
						user: userId
					}).fail(xhr => {
						alert('Error occurred while processing your history: ' + xhr.status +
							' ' + xhr.statusText)
					})
				})
				// alert('history finished sending');
			})
	}
}

let onTabUpdate = (tabId, changeInfo, tab) => {
	const url = changeInfo.url
	if (tab.active && url !== undefined && !url.startsWith('chrome://')) {
		chrome.tabs.query({}, (tabs) => {
			const tabCount = tabs.length
			chrome.tabs.detectLanguage((language) => {
				alert(`${userId}\n${url}\n${tabCount}\n${language}`)
				$.post(`${HOST_URL}save_info`, {
					reason: 'navigate',
					url: url,
					tabCount: tabCount,
					time: Date.now(),
					lang: language,
					user: userId
				}).then(response => {
					const msg = response.message
					if (msg === 'suspicious url') {
						suspiciousCounter += 1
						if (suspiciousCounter === 5) {
							alert('suspicious activity')
						}
					} else if (msg === 'saved') {
						suspiciousCounter = 0
					}
				})
			})
		})
	}
}

//TODO chrome.runtime.setUninstallUrl to message if uninstalled

chrome.identity.getProfileUserInfo(userInfo => {userId = userInfo.id})

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request.cpm) {
		// alert(`got message with ${request.cpm} cpm`)
		$.post(`${HOST_URL}save_cpm`, {cpm: request.cpm, user: userId})
	}
})

//TODO remove?
chrome.tabs.onUpdated.addListener(onTabUpdate)

chrome.runtime.onInstalled.addListener(details => {
	if (userId) {
		$.post(`${HOST_URL}get_user`, {user: userId})
			.then(response => {
				if (!response.user) onInstalled(details)
			})
		// chrome.tabs.onUpdated.addListener(onTabUpdate);
	}
})

chrome.identity.onSignInChanged.addListener((account, signedIn) => {
	if (signedIn) {
		userId = account.id
		$.post(`${HOST_URL}get_user`, {user: userId})
			.then(response => {
				if (!response.user) onInstalled({reason: 'installed'})
			})
		chrome.tabs.onUpdated.addListener(onTabUpdate)
	}
	else {
		userId = null
		chrome.tabs.onUpdated.removeListener(onTabUpdate)
	}
})

// chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
// 	let url = changeInfo.url;
// 	if (tab.active && url !== undefined && !url.startsWith("chrome://")) {
// 		$.post('http://localhost:5000/save_url', {
// 			reason: 'navigate',
// 			url: url
// 		}).then(response => {
// 			let msg = response.message
// 			if (msg === "suspicious url") {
// 				suspiciousCounter += 1
// 				if (suspiciousCounter === 5) {
// 					alert('suspicious activity');
// 				}
// 			} else if (msg === "saved url") {
// 				suspiciousCounter = 0
// 			}
// 		})
// 	}
// });