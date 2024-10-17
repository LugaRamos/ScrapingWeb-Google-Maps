var map;
var coordenadas = {};
var marcador;

function initMap() {

    // Inicializar o mapa
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -25.532227, lng: -48.666324 },
        zoom: 15,
        mapTypeId: 'satellite',
    });

    CaixaDeBusca();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var localizacao = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(localizacao);
            colocarMarcador(localizacao);
        }, function() {
            alert('Não foi possível obter a sua localização atual.');
        });
    } else {
        alert('Seu navegador não suporta geolocalização.');
    }

    // Adicionar evento de clique no mapa
    map.addListener('click', function(e) {
        coordenadas = e.latLng;
        document.getElementById('latitudeInput').value = coordenadas.lat();
        document.getElementById('longitudeInput').value = coordenadas.lng();
        document.getElementById('latitude').textContent = coordenadas.lat();
        document.getElementById('longitude').textContent = coordenadas.lng();
        colocarMarcador(coordenadas);
    });
    
}

// Função para colocar um marcador no mapa
function colocarMarcador(localizacao) {
    // Se já existe um marcador, remover antes de adicionar um novo
    if (marcador) {
        marcador.setMap(null);
    }
    marcador = new google.maps.Marker({
        position: localizacao,
        map: map
    });
}

function CaixaDeBusca() {
    var input = document.getElementById('caixa-de-busca').value;
    var geocoder = new google.maps.Geocoder();
    
    geocoder.geocode({ 'address': input }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var location = results[0].geometry.location;
            map.setCenter(location);
            colocarMarcador(location);
            document.getElementById('latitudeInput').value = location.lat();
            document.getElementById('longitudeInput').value = location.lng();
            document.getElementById('latitude').textContent = location.lat();
            document.getElementById('longitude').textContent = location.lng();

            // Inicializar o Place Picker
            var placePicker = new google.maps.places.PlacePicker(document.getElementById('placePicker'));
            
            // Definir evento de lugar selecionado
            placePicker.addListener('place_changed', function() {
                var place = placePicker.getPlace();
                if (!place.geometry) {
                    console.log("O local selecionado não possui geometria.");
                    return;
                }
                map.setCenter(place.geometry.location);
                colocarMarcador(place.geometry.location);
                document.getElementById('latitudeInput').value = place.geometry.location.lat();
                document.getElementById('longitudeInput').value = place.geometry.location.lng();
                document.getElementById('latitude').textContent = place.geometry.location.lat();
                document.getElementById('longitude').textContent = place.geometry.location.lng();
            });
        }
    });
}


// Função para retornar as coordenadas capturadas
function getCoordenadas() {
    return coordenadas;
}

// Adiciona o evento ao botão apenas após a página carregar
window.onload = function() {
    var btn = document.getElementById("tutorialBtn");

    // Adiciona o evento de clique ao botão de tutorial
    btn.addEventListener("click", function() {
        ChamaModal();
    });
};

function ChamaModal() {
    var modal = document.getElementById("tutorialModal");
    var span = document.getElementsByClassName("close")[0];

    // Exibe o modal ao clicar no botão
    modal.style.display = "block";

    // Fecha o modal ao clicar no "X"
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Fecha o modal ao clicar fora da área do modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}



