const fileInput = document.getElementById("file");
const fileName = document.getElementById("fileName");
const dropZone = document.getElementById("dropZone");
if (fileInput) fileInput.addEventListener("change", () => fileName.textContent = fileInput.files.length ? fileInput.files[0].name : "No file selected");
if (dropZone) {
  ["dragenter","dragover"].forEach(n => dropZone.addEventListener(n,e=>{e.preventDefault();dropZone.style.transform="scale(1.01)";}));
  ["dragleave","drop"].forEach(n => dropZone.addEventListener(n,e=>{e.preventDefault();dropZone.style.transform="scale(1)";}));
  dropZone.addEventListener("drop", e => { if(e.dataTransfer.files.length){fileInput.files=e.dataTransfer.files;fileName.textContent=e.dataTransfer.files[0].name;} });
}
function confirmDelete(){ return confirm("Delete this study material?"); }
