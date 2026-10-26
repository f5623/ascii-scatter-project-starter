"""ASCII-Scatter-Plot für das Terminal (Person B).

Erwartet Punkte im vereinbarten Format:
    [("A", 1.2, 7.8), ("B", 2.7, 5.1), ...]
also (Kategorie, x-Wert, y-Wert).
"""

from rich.console import Console
from rich.text import Text

# Jede Kategorie bekommt eine eigene Farbe.
STYLES = {
    "A": "bold cyan",
    "B": "bold magenta",
    "C": "bold green",
    "D": "bold yellow",
}

# Das Console-Objekt schreibt (farbig) ins Terminal.
console = Console()


def scale(value, minimum, maximum, size):
    """Rechnet einen Datenwert auf eine Terminal-Position (0 bis size-1) um."""
    # Sonderfall: alle Werte gleich -> sonst Division durch null.
    if maximum == minimum:
        return 0

    # Anteil zwischen 0.0 (Minimum) und 1.0 (Maximum).
    relative = (value - minimum) / (maximum - minimum)

    # Auf die verfügbaren Positionen hochrechnen und runden.
    # size - 1, weil die Indizes bei 0 beginnen (z. B. 0 bis 39 bei size=40).
    return round(relative * (size - 1))


def render_scatter(points, width=40, height=15):
    """Zeichnet die Punkte als farbigen ASCII-Scatter-Plot ins Terminal."""
    # Ohne Punkte gibt es nichts zu zeichnen (und min()/max() würden abstürzen).
    if not points:
        console.print("Keine Punkte zum Anzeigen.")
        return

    # 1. Wertebereich der Daten bestimmen.
    min_x = min(x for _, x, _ in points)
    max_x = max(x for _, x, _ in points)
    min_y = min(y for _, _, y in points)
    max_y = max(y for _, _, y in points)

    # 2. Leeres Grid anlegen: height Zeilen mit je width Leerzeichen.
    #    Wichtig: List Comprehension, NICHT [[" "] * width] * height,
    #    sonst wären alle Zeilen dieselbe Liste.
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # 3. Punkte ins Grid eintragen.
    for point_type, x, y in points:
        x_pos = scale(x, min_x, max_x, width)
        y_pos = scale(y, min_y, max_y, height)

        # y umdrehen: Im Terminal ist Zeile 0 oben,
        # im Diagramm sollen große y-Werte oben stehen.
        row = height - 1 - y_pos

        # Erst Zeile (y), dann Spalte (x).
        if grid[row][x_pos] == " ":
            grid[row][x_pos] = point_type
        else:
            # Stelle schon belegt -> Kollision markieren.
            grid[row][x_pos] = "*"

    # 4. Grid Zeile für Zeile farbig ausgeben.
    for grid_row in grid:
        line = Text()
        for symbol in grid_row:
            if symbol in STYLES:
                line.append(symbol, style=STYLES[symbol])
            else:
                line.append(symbol)
        console.print(line)


# Wird nur ausgeführt, wenn die Datei direkt gestartet wird,
# nicht beim Import aus einer anderen Datei.
if __name__ == "__main__":
    # Feste Beispieldaten -> unabhängig vom CSV-Loader von Person A.
    example_points = [
        ("A", 1.2, 7.8),
        ("B", 2.7, 5.1),
        ("C", 4.8, 8.4),
        ("D", 8.2, 2.0),
    ]
    render_scatter(example_points)