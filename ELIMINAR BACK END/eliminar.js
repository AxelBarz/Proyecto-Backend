const URL = "http://127.0.0.1:5000/";

function eliminarAuto(codigo) {
    if (confirm('¿Estas seguro que quieres eliminar la siguiente publicacion?')) {
        fetch(URL + `automovil/${codigo}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    obtenerPublicacion();
                    alert('Publicacion eliminada correctamente');
                }
            })
            .catch(error => {
                alert(error.message);
            });
    }
}

function obtenerPublicacion() {
    fetch(URL + 'automovil')
        .then(response => {
            if (response.ok) { return response.json(); }
        })
        .then(data => {
            const autoTabla = document.getElementById('item-list').getElementsByTagName('tbody')[0];
            autoTabla.innerHTML = '';

            data.forEach(automovil => {
                const columna = autoTabla.insertRow();
                columna.innerHTML = ` 
                    <td align="center">${automovil.codigo}</td>
                    <td align="center">${automovil.marca}</td>
                    <td align="center">${automovil.precio}</td>
                    <td align="center">${automovil.numetel}</td>
                    <td align="center"><button onclick="eliminarAuto(${automovil.codigo})" id="el"><img src="img/basura.png" alt="basura"></button></td>
                `;
            });
        })
        .catch(error => {
            console.log('Error:', error);
            alert('Error al obtener las publicaciones.');
        });
}

document.addEventListener('DOMContentLoaded', obtenerPublicacion);
