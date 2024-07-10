const URL= "http://127.0.0.1:5000/"

document.getElementById('formulario').addEventListener('submit', function(event){
    event.preventDefault(); //Se evita que se envie el form 

    var formData = new FormData(this);

    fetch(URL + 'automovil', {
        method: 'POST',
        body: formData // Aquí enviamos formData. Dado que formData puede contener archivos, no se utiliza JSON.
    })

    .then(function(response){
            if (response.ok){
                return response.json();
            } else {
                throw new Error('Error al agregar el auto');
            }
    })

        .then(function(data){
            alert('Automovil agregado correctamente')
        })

        .catch(function(error){
            alert('Error al agregar el auto');
        })

        .finally(function(){
            document.getElementById('marca').value="";
            document.getElementById('anio').value="";
            document.getElementById('precio').value="";
            document.getElementById('transmision').value="";
            document.getElementById('combustible').value="";
            document.getElementById('numetel').value="";
        });
})