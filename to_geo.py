from simplekml import Kml, GroundOverlay


def create_kml_with_image(image_path, points, kml_path="output.kml"):
    kml = Kml()

    ground = kml.newgroundoverlay(name="Attached Image")
    ground.icon.href = image_path
    ground.latlonbox.north = max(pt[0] for pt in points)  
    ground.latlonbox.south = min(pt[0] for pt in points)  
    ground.latlonbox.east = max(pt[1] for pt in points)   
    ground.latlonbox.west = min(pt[1] for pt in points)   

    kml.save(kml_path)
    print(f"KML-файл сохранён в {kml_path}")
