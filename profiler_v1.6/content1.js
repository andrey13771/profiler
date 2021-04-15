// let start
let now
let finish
// let charCount = 0
let keypress = []
let keyup = []

let sendTimings = () => {
    // console.log(keypress, keyup)
    if (keypress.length > 3) chrome.runtime.sendMessage({'keypress': keypress, 'keyup': keyup})
    keypress = []
    keyup = []
    // if (charCount > 3) {
    //     const intervalInMinutes = (now - start) / 60000
    //     const cpm = charCount / intervalInMinutes
        // alert(`${charCount} characters in ${intervalInMinutes * 60} seconds`)
        // chrome.runtime.sendMessage({cpm: cpm})
    // }
    // start = finish
    // now = finish
    // charCount = 1
}

window.addEventListener('keypress', evt => {
    if (evt.repeat) {return}
    // finish = Date.now()
    // if (!start) {
    //     now = Date.now()
    //     start = now
    // }
    if (Date.now() - now > 5000) sendTimings()
    // keypress.push([evt.code, evt.timeStamp, evt.altKey, evt.shiftKey, evt.ctrlKey, evt.metaKey])
    keypress.push({'code': evt.code, 'timestamp': evt.timeStamp, 'alt': evt.altKey,
        'shift': evt.shiftKey, 'ctrl': evt.ctrlKey, 'meta': evt.metaKey})
    // if (finish - now > 5000) sendCPM()
    // else {
    //     charCount++
    //     now = finish
    // }
})

window.addEventListener('keyup', evt => {
    // keyup.push([evt.code, evt.timeStamp])
    keyup.push({'code': evt.code, 'timestamp': evt.timeStamp})
    // finish = Date.now()
    now = Date.now()
    // if (!start) {
    //     start = finish
    //     now = finish
    // }
    // if (finish - now > 5000) sendCPM()
    // else {
    //     charCount++
    //     now = finish
    // }
})