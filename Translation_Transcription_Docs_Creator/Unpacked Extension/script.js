const docx = require('docx')
const yandexTranslate = require('yandex-translate')("trnsl.1.1.20191130T143926Z.1596b48f1725caed.ed03eca52699e536b4a7c1d520615dead8f960fa")
const saveAs = require("file-saver")
let doc = new docx.Document();
let paragraph = new docx.Paragraph({
    children: []
});
// переменная, в которую будут заливаться все строки
let texts = [];
// словарь транскрипций
TextToIPA = {};
(function () {
    'use strict';
    // Objects
    // Create the ipadict if one does not currently exist. This is important,
    // as reloading the dict takes long, so if one already exists, let it be.
    if (typeof TextToIPA._IPADict !== 'object') {
        TextToIPA._IPADict = {};
    }
    // Create a constructor for an IPAWord that makes displaying them and
    // associated errors much easier.
    function IPAWord(error, text) {
        this.error = error;
        this.text = text;
    }
    // Functions
    // Parse the dictionary. Only used by `loadDict`.
    if (typeof TextToIPA._parseDict !== 'function') {
        TextToIPA._parseDict = function (lines) {
            console.log('TextToIPA: Beginning parsing to dict...');

            // Fill out the IPA dict by
            // 1) regexing the word and it's corresponding IPA translation into an array
            // 2) using the word as the key and the IPA result as the pair
            for (var i in lines) {
                var arr = lines[i].split(/\s+/g);
                TextToIPA._IPADict[arr[0]] = arr[1];
            }
            console.log('TextToIPA: Done parsing.');
        };
    }
    // Load the dictionary. Can be on the local machine or from a GET request.
    if (typeof TextToIPA.loadDict !== 'function') {
        TextToIPA.loadDict = function (location) {
            console.log('TextToIPA: Loading dict from ' + location + '...');

            if (typeof location !== 'string') {
                console.log('TextToIPA Error: Location is not valid!');
            } else {
                var txtFile = new XMLHttpRequest();
                txtFile.open('GET', location, true);
                txtFile.onreadystatechange = function() {
                    // If document is ready to parse...
                    if (txtFile.readyState == 4) {
                        // And file is found...
                        if (txtFile.status == 200 || txtFile.status == 0) {
                            // Load up the ipa dict
                            TextToIPA._parseDict(txtFile.responseText.split('\n'));
                        }
                    }
                };
                txtFile.send(null);
            }
        };
    }
    // Lookup function to find an english word's corresponding IPA text
    if (typeof TextToIPA.lookup !== 'function') {
        TextToIPA.lookup = function (word) {
            if (Object.keys(TextToIPA._IPADict).length === 0) {
                console.log('TextToIPA Error: No data in TextToIPA._IPADict. Did "TextToIPA.loadDict()" run?');
            } else {
                // It is possible to return undefined, so that case should not be ignored
                if ( typeof TextToIPA._IPADict[word] != 'undefined' ) {
                    var error = null;
                    var text = TextToIPA._IPADict[word];
                    return new IPAWord(error, text);
                } else {
                    return new IPAWord('undefined', '');
                }
            }
        };
    }
}());

// вывод в файл
async function exportFile(){
     let wordSetName = document.getElementById("wordSetName").value
     if (wordSetName == '') {
         alert("Введите название набора");
         return;
     }
     // из background.js получаем набор строк для импорта
     // и переводим их в формат, читаемый docx-ом
    await sendMessagePromise({command: "getTexts", txt: "get texts"})
    for (let text of texts) {
        text = new docx.TextRun(text);
        text.break();
        paragraph.addChildElement(text)
    }
    doc.addSection({
         properties: {},
         children: [paragraph]
     })
    docx.Packer.toBlob(doc);
    docx.Packer.toBlob(doc).then((blob) => {
        saveAs(blob, wordSetName+".docx");
    })
    // после эккспорта обнуляет все переменные, так как больше эти данные нам не нужны
    paragraph = new docx.Paragraph({children: []});
    doc = new docx.Document();
    chrome.runtime.sendMessage({command: "clearTexts", txt: "clear texts"});
    texts = [];
}
// promise для запроса строк
function sendMessagePromise(item) {
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage(item, function (response) {
            if (response.complete) {
                texts = response.texts
                resolve();
            } else {
                reject('Something wrong')
            }
        })
    })
}

function addWord(){
    // считываем данные слова с полей
    let word = document.getElementById("word").value;
    let transcription = document.getElementById("transcription").value;
    let translation = document.getElementById("translation").value;
    if (word == '') {
        alert("Введите слово")
        return
    }
    if(translation == '') {
        alert("Введите перевод")
        return
    }
    // составляем строку
    let text = `${word} — `;
    if (transcription !== '') {
        text += `[${transcription}] — `;
    }
    text += translation;
    // отправляем строку в хранилище на background page
    chrome.runtime.sendMessage({command: "addText", text: text, txt: "add Text"});
}

function translate(){
    // считываем слово для перевода с поля word
    let word = document.getElementById("word").value;
    // перевод с помощью yandexTranslate
    yandexTranslate.translate(word, {to: 'ru'}, function (err,res) {
        let trans = res.text[0];
        document.getElementById('transcription').value = TextToIPA.lookup(word).text;
        document.getElementById("translation").value = trans;
    })
}

document.getElementById("translate").onclick = translate;
document.getElementById("export").onclick = exportFile;
document.getElementById("addSet").onclick = addWord;
document.addEventListener('DOMContentLoaded', function () {
    // скрипт для считывания выделенного текста
    chrome.tabs.executeScript( null, {"code": "window.getSelection().toString()"}, function (selection) {
        var selectedText = selection[0];
        TextToIPA.loadDict('./ipaDict.txt');
        document.getElementById("word").value = selectedText;
        translate();
    });
});
