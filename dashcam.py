import json
import folium

def speed_color(speed):
    """Gibt eine Farbe anhand der Geschwindigkeit zurück."""
    if speed < 30:
        return 'pink'
    elif speed < 50:
        return 'blue'
    elif speed < 80:
        return 'green'
    elif speed < 100:
        return 'orange'
    else:
        return 'red'

# GPS-Daten laden und filtern
points = []
with open("gpsdaten.ndjson") as f:
    for line in f:
        data = json.loads(line)
        # Nur gültige Werte nehmen
        if data['a'] != 99.0 and data['o'] != 999.0:
            points.append(data)

if not points:
    raise ValueError("Keine gültigen GPS-Punkte gefunden.")

# Karte zentrieren
map_center = (points[0]['a'], points[0]['o'])
m = folium.Map(location=map_center, zoom_start=15)

# Liniensegmente mit Farben je nach Geschwindigkeit zeichnen
for i in range(len(points)-1):
    p1 = points[i]
    p2 = points[i+1]
    line = [(p1['a'], p1['o']), (p2['a'], p2['o'])]
    color = speed_color(p1['s'])
    folium.PolyLine(line, color=color, weight=5, opacity=0.8).add_to(m)

# Start/Ende markieren
folium.Marker((points[0]['a'], points[0]['o']), popup="Start", icon=folium.Icon(color="green")).add_to(m)
folium.Marker((points[-1]['a'], points[-1]['o']), popup="Ende", icon=folium.Icon(color="red")).add_to(m)

m.save("gps_visualisierung.html")
print("Karte gespeichert als gps_visualisierung.html")