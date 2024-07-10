const URL= "http://127.0.0.1:5000/"

//Se realiza la solicitud GET para obtener las publicaciones 
fetch(URL + 'automovil')
    .then(function (response){
        if(response.ok){
            //Si la respuesta es exitosa, se convierte de Json a objeto JS y pasa los datos a la siguiente promesa the 
            return response.json();
        }else{
            //Si hay un error, manda este mensaje de alerta 
            throw new Error('Error al obtener la publicacion');
        }
    })

    //La funcion maneja los datos obtenidos 
    .then(function(data){
        let divPublicacion = document.getElementById('grid'); //Selecciona el elemento donde se mostraran las publicaciones 

        //Se itera cada publicacion
        for (let auto of data){
            let div = document.createElement('div')
            div.classList.add('autos')

            div.innerHTML = '<a>'+auto.codigo+'</a>'+
                '<b class="marca">'+auto.marca+'</b>' + '<b class="marca">'+auto.anio+'</b>'+'<br>'+
                '<p>'+auto.transmision+'</p>'+'<p>'+auto.combustible+'</p>'+'<br>'+  
                '<b class="num"> Tel: '+auto.numetel+'</b>'+'<br>'+              
                '<b class="num" id="pre">$'+auto.precio+'</b>';

            divPublicacion.appendChild(div);
        }
    })

    //Captura y maneja errores, mostrando una alerta 
    .catch(function(error){
        alert('Error al obtener publicacion')
    });