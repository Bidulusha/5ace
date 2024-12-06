import geojson

def create_html_file():
    with open('output.geojson', 'r') as fcc_file:
        fcc_data = geojson.load(fcc_file)


    html = '''<!DOCTYPE html>
    <html>
    <head>
        <title>Display GeoJSON and Image Overlay</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
        <style>
            #map { height: 100vh; }
        </style>
    </head>
    <body>
        <url = "output.json">
        <div id="map"></div>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"> </script>

        <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
        <script type="module">
            // Инициализация карты
            var map = L.map('map').setView(''' + str([fcc_data['features'][0]['geometry']['coordinates'][0][3][1], fcc_data['features'][0]['geometry']['coordinates'][0][3][0]]) + ''', 5); // Центр карты
    ''' + 'const geojson_data = ' + str(fcc_data) + '''
            //Добавление базового слоя карты
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            // Загрузка GeoJSON файла
                L.geoJSON(geojson_data).addTo(map);
            // Наложение изображения
            var bounds = ['''+ str([fcc_data['features'][0]['geometry']['coordinates'][0][3][1], fcc_data['features'][0]['geometry']['coordinates'][0][3][0]]) + ',' + str([fcc_data['features'][0]['geometry']['coordinates'][0][1][1], fcc_data['features'][0]['geometry']['coordinates'][0][1][0]]) + ''']; 
            L.imageOverlay('pic2/2024-10-24_04-42-28_SXC3-227_1.jpg', bounds).addTo(map);
        </script>
    </body>
    </html>
    '''
    with open('map.html', 'w') as f:
        f.write(html)