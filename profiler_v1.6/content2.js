let start
let now
let finish
let charCount = 0

let sendCPM = () => {
    if (charCount > 3) {
        const intervalInMinutes = (now - start) / 60000
        const cpm = charCount / intervalInMinutes
        // alert(`${charCount} characters in ${intervalInMinutes * 60} seconds`)
        chrome.runtime.sendMessage({cpm: cpm})
    }
    start = finish
    now = finish
    charCount = 1
}

window.addEventListener('keydown', event => {
    finish = Date.now()
    if (!start) {
        start = finish
        now = finish
    }
    if (finish - now > 5000) sendCPM()
    else {
        charCount++
        now = finish
    }
})