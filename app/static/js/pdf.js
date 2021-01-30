function generatePdf(){
const element = document.getElementById('statement')
html2pdf()
.from(element)
.save()

}