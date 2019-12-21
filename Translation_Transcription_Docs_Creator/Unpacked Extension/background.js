// хранилище строк
let texts = [];
chrome.runtime.onMessage.addListener(messageResponse)
function messageResponse (request, sender, sendResponse) {
    console.log(request.txt)
    if (request.command == "getTexts"){ // отправка данных хранилища
        sendResponse({texts: texts, complete: true});
    } else if (request.command == "addText") { // добавление строки в хранилище
        texts.push(request.text);
    }
    else if (request.command == "clearTexts") { // очистка хранилища
        texts = [];
    }
    return true;
}
