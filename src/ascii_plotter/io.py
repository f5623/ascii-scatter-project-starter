import csv

def load_points(path):
    
    points = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            point_type = row["type"]

            x = float(row["value1"])

            y = float(row["value2"])
            
            points.append((point_type, x, y))

    return points

