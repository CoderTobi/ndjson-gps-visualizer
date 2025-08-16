import json
import folium

# Einlesen der NDJSON/JSONL Datei
points = []
with open("gpsdaten.ndjson") as f:
    for line in f:
        #print(line)
        data = json.loads(line)
        # Filtere ungültige Werte raus
        if data['a'] != 99.0 and data['o'] != 999.0:
            points.append((data['a'], data['o']))

# Mittelpunkt der Karte setzen (z.B. erster Punkt)
map_center = points[0]
m = folium.Map(location=map_center, zoom_start=15)

# Track hinzufügen
folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)
folium.Marker(points[0], popup="Start").add_to(m)
folium.Marker(points[-1], popup="Ende").add_to(m)

# Karte speichern
m.save("gps_visualisierung.html")