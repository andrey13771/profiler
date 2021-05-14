let now
let finish
let keypress = []
let keyup = []

let sendTimings = () => {
    if (keypress.length > 3) chrome.runtime.sendMessage({'keypress': keypress, 'keyup': keyup})
    keypress = []
    keyup = []
}

window.addEventListener('keypress', evt => {
    if (evt.repeat) {return}
    if (Date.now() - now > 5000) sendTimings()
    keypress.push({'code': evt.code, 'timestamp': evt.timeStamp, 'alt': evt.altKey,
        'shift': evt.shiftKey, 'ctrl': evt.ctrlKey, 'meta': evt.metaKey})
})

window.addEventListener('keyup', evt => {
    keyup.push({'code': evt.code, 'timestamp': evt.timeStamp})
    now = Date.now()
})