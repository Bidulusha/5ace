import geojson

def create_geojson_with_image(image_url, points, geojson_path="output.geojson"):
    polygon = geojson.Polygon([[
        (points[0][1], points[0][0]),  # Верхний левый угол
        (points[1][1], points[1][0]),  # Верхний правый угол
        (points[3][1], points[3][0]),  # Нижний правый угол
        (points[2][1], points[2][0]),  # Нижний левый угол
        (points[0][1], points[0][0])   # Замыкаем полигон
    ]])

    # Свойства изображения
    properties = {
        "image": image_url
    }

    # Создаём Feature
    feature = geojson.Feature(geometry=polygon, properties=properties)

    # GeoJSON-объект
    feature_collection = geojson.FeatureCollection([feature])

    # Сохраняем GeoJSON
    with open(geojson_path, "w") as f:
        geojson.dump(feature_collection, f, indent=2)
    print(f"GeoJSON-файл сохранён в {geojson_path}")
