const codigo = document.formulario.codigo.value.trim();
if (codigo === "" || isNaN(codigo) || codigo.length != 8) {
  document.formulario.codigo.focus();
  parrafo.innerHTML = "CODIGO INCORRECTO";
  return false;
}






 //var codigosvalidos = ["1234"];

         //  <!-- function validar() {
                //var codigoingresado = document.getElementById("codigo").value;

               // if (codigosValidos.includes(codigoingresado)) {
               //     location.href = "file:///C:/Users/lupef/OneDrive/Escritorio/FORMULARIO%20BACK%20END/formulario.html";
               // } else {
               //     alert("Código incorrecto.\n Reintentar");
               // }
          //  }