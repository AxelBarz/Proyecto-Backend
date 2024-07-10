const URL= "http://127.0.0.1:5000/";

let codigo='';
let marca='';
let anio='';
let precio='';
let transmision='';
let combustible='';
let numeroTelefono='';
let mostrarDatosAutos = false;

document.getElementById('codigoForm').addEventListener('submit', obtenerPublicacion);
document.getElementById('formulario').addEventListener('submit', guardarCambios);

function obtenerPublicacion(event){
    event.preventDefault();
    codigo=document.getElementById('codigo').value;
    fetch(URL+'automovil/'+codigo)
        .then(response => {
            if(response.ok){
                return response.json();
            } else {
                throw new Error('Error al obtener la publicación');
            }
        })
        .then(data => {
            if (data) {
                marca = data.marca;
                anio = data.anio;
                precio = data.precio;
                transmision = data.transmision;
                combustible = data.combustible;
                numeroTelefono = data.numetel;
                mostrarDatosAutos = true;
                mostrarFormulario();
            } else {
                throw new Error('Código no encontrado');
            }
        })
        .catch(error => {
            alert('Código no encontrado');
            console.error('Error:', error);
        });
}

function mostrarFormulario(){
    if (mostrarDatosAutos){
        document.getElementById('marca').value = marca;
        document.getElementById('anio').value = anio;
        document.getElementById('precio').value = precio;
        document.getElementById('transmision').value = transmision;
        document.getElementById('combustible').value = combustible;
        document.getElementById('numero').value = numeroTelefono;

        document.querySelector('.conteiner').style.display = 'block';
    } else {
        document.querySelector('.conteiner').style.display = 'none';
    }
}

function guardarCambios(event){
    event.preventDefault();

    const formData = new FormData();
    formData.append('codigo', codigo);
    formData.append('marca', document.getElementById('marca').value);
    formData.append('anio', document.getElementById('anio').value);
    formData.append('precio', document.getElementById('precio').value);
    formData.append('transmision', document.getElementById('transmision').value);
    formData.append('combustible', document.getElementById('combustible').value);
    formData.append('numetel', document.getElementById('numero').value);

    fetch(URL+'automovil/'+codigo, {
        method: 'PUT',
        body: formData,
    })
    .then(response => {
        if(response.ok){
            return response.json();
        } else {
            throw new Error('Error al guardar los cambios del auto');
        }
    })
    .then(data => {
        alert('Automóvil actualizado correctamente');
        limpiarFormulario();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar el automóvil');
    });
}

function limpiarFormulario(){
    document.getElementById('codigo').value = '';
    document.getElementById('marca').value = '';
    document.getElementById('anio').value = '';
    document.getElementById('precio').value = '';
    document.getElementById('transmision').value = '';
    document.getElementById('combustible').value = '';

    codigo = '';
    marca = '';
    anio = '';
    precio = '';
    transmision = '';
    combustible = '';
    numeroTelefono = '';
    mostrarDatosAutos = false;

    document.querySelector('.container').style.display = 'none';
}
