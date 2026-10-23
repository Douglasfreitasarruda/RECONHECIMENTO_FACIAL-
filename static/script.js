const formReconhecimento = document.getElementById("formReconhecimento");
const btnReconhecer = document.getElementById("btnReconhecer");
const scannerRing = document.getElementById("scannerRing");
const statusTexto = document.getElementById("statusTexto");
const subStatusTexto = document.getElementById("subStatusTexto");

if (formReconhecimento && btnReconhecer && scannerRing) {
  formReconhecimento.addEventListener("submit", function () {
    btnReconhecer.disabled = true;
    btnReconhecer.textContent = "Validando acesso...";
    scannerRing.classList.remove("success", "error");
    scannerRing.classList.add("scanning");

    statusTexto.textContent = "Validando identidade";
    subStatusTexto.textContent = "Aproxime o rosto e aguarde a leitura facial...";
  });
}