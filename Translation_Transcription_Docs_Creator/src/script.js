const docx = require('docx')
const FileSaver = require('file-saver');
const mammoth = require("mammoth");
let doc = new docx.Document();
let paragraph = new docx.Paragraph({
    children: []
});

function exportFile(){
     let wordSetName = document.getElementById("wordSetName").value
     if (wordSetName == '') {
         alert("Введите название набора");
         return;
     }
     doc.addSection({
         properties: {},
         children: [paragraph]
     })
    docx.Packer.toBlob(doc);
    docx.Packer.toBlob(doc).then((blob) => {
        saveAs(blob, wordSetName+".docx");
    })
    paragraph = new docx.Paragraph({children: []});
    doc = new docx.Document();

}

function addWord(){
    let word = document.getElementById("word").value;
    let transcription = document.getElementById("transcription").value;
    let translation = document.getElementById("translation").value;
    if (word == '') {
        alert("Введите слово")
        return
    }
    if (transcription == '') {
        alert("Введите транскрипцию")
        return
    }
    if(translation == '') {
        alert("Введите перевод")
        return
    }
    let text = (`${word} - [${transcription}] - ${translation}`);

    text = new docx.TextRun(text);
    text.break();

    paragraph.addChildElement(text)

}

function addWordSet() {
    let path = document.getElementById("getWordSet").value;
    console.log(path);
    mammoth.extractRawText({path}).then((result) => {
        paragraph.addChildElement(new docx.TextRun(result.value))
    })
}
document.getElementById("export").onclick = exportFile
document.getElementById("addSet").onclick = addWord
