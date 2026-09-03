"""
Bundeswettbewerb Informatik 2024 Runde 2 Aufgabe 2
Autor: Tao Zheng
"""

def read_labyrinth(content):
    # Text vorbereiten
    lines = content.strip().split("\n")
    line = 0

    # Labyrinthgröße ablesen
    n, m = map(int, lines[line].split())
    line += 1

    # Labyrinth 1:
    # Wände ablesen
    vertical_walls_1 = [list(map(int, lines[line + i].split())) for i in range(m)]
    line += m

    horizontal_walls_1 = [list(map(int, lines[line + i].split())) for i in range(m - 1)]
    line += m - 1

    # Anzahl Gruben ablesen
    num_pits_1 = int(lines[line])
    line += 1

    # Gruben ablesen
    pits_1 = []
    for i in range(num_pits_1):
        x, y = map(int, lines[line].split())
        pits_1.append((x, y))
        line += 1

    # Labyrinth 2:
    # Wände ablesen
    vertical_walls_2 = [list(map(int, lines[line + i].split())) for i in range(m)]
    line += m

    horizontal_walls_2 = [list(map(int, lines[line + i].split())) for i in range(m - 1)]
    line += m - 1

    # Anzahl Gruben ablesen
    num_pits_2 = int(lines[line])
    line += 1

    # Gruben ablesen
    pits_2 = []
    for i in range(num_pits_2):
        x, y = map(int, lines[line].split())
        pits_2.append((x, y))
        line += 1

    # Zur Dictionary umwandeln und zurückgeben.
    return {
        "labyrinth_1": {
            "vertical_walls": vertical_walls_1,
            "horizontal_walls": horizontal_walls_1,
            "pits": set(pits_1),
        },
        "labyrinth_2": {
            "vertical_walls": vertical_walls_2,
            "horizontal_walls": horizontal_walls_2,
            "pits": set(pits_2),
        },
        "dimensions": (n, m),
    }

def solve_labyrinth(dimensions, vertical_walls, horizontal_walls, pits):
    """
    solve labyrinth: Berechnet den Weg eines einzelnen Labyrinth.
    """
    n, m = dimensions
    start = (0, 0) # (x, y)
    goal = (n - 1, m - 1)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Rechts, Unten, Links, Oben
    visited = set(pits) # Besuchte Koordinaten (startet mit den Gruben, um alle Gruben zu vermeiden)
    payload = {
        "position":start, # (0, 0)
        "movement": "", # Bewegungssymbol
        "before": None, # vorherige payload um vorherige Bewegungen rekursiv aufzulisten
    }
    queue = [payload] # Warteschlange

    while queue:
        payload = queue.pop(0)
        (x, y) = payload['position']

        # Für alle 4 Richtungen probieren
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # innerhalb des Spielbereichs und noch nicht besucht
            if not 0 <= nx < n or not 0 <= ny < m or (nx, ny) in visited:
                continue
            
            if dy == 1 and horizontal_walls[y][x] == 1: # Unten
                continue
            if dx == 1 and vertical_walls[y][x] == 1: # Rechts
                continue
            if dy == -1 and horizontal_walls[y - 1][x] == 1: # Oben
                continue
            if dx == -1 and vertical_walls[y][x - 1] == 1: # Links
                continue

            # Bewegungssymbol bestimmen
            if dy == 1:
                movementletter = "S"
            if dy == -1:
                movementletter = "W"
            if dx == 1:
                movementletter = "D"
            if dx == -1:
                movementletter = "A"
            
            if (nx, ny) == goal:
                # Rekursiv durch die Befragung aller vorherigen payloads die benötigte Bewegung sowie Koordinatenliste bestimmen
                pastPositions = [(nx, ny)]
                while True:
                    movementletter = payload['movement'] + movementletter # Bewegung
                    pastPositions.insert(0, payload['position']) # Koordinatenliste
                    if payload["before"] is None:
                        return pastPositions, movementletter
                    payload = payload['before'] # zur vorherigen payload bzw. Koordinate zurückgehen
            
            visited.add((nx, ny)) # Neue Koordinaten als besucht markieren
            newPayload = {
                "position": (nx, ny),
                "movement": movementletter,
                "before": payload,
            }
            queue.append(newPayload) # Neue Koordinaten für weitere Berechnungen in die Warteschlange hinzufügen. 

    return None, None # Bei keiner Lösung

def solve_duo_labyrinth(dimensions, labyrinth1, labyrinth2, solution1, solution2, progressPuffer = 10):
    """
    solve duoo labyrinth: Berechnet Weg in zwei Labyrinthen gleichzeitig (4-Dimensionale Labyrinthe).
    """
    n, m = dimensions
    goal = (n - 1, m - 1)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Rechts, Unten, Links, Oben
    best = 0 # Rekordpunktzahl
    payload = {
        "progress1":0, # Punktzahl für Labyrinth 1
        "progress2":0, # Punktzahl für Labyrinth 2
        "position1":(0, 0), # Koordinate Labyrinth 1 (x, y)
        "position2":(0, 0), # Koordinate Labyrinth 2 (x, y)
        "movement":"", # Bewegungssymbol
        "wipeouts": (False, False), # vgl. Wipeoutsregel
        "before": None, # vorherige payload um vorherige Bewegungen rekursiv aufzulisten
    }
    visited = set() # Besuchte Koordinaten
    queue = [payload]
    while queue:
        payload = queue.pop(0)
        # Für alle 4 Richtungen
        for dx, dy in directions:
            p1 = payload["position1"]
            p2 = payload["position2"]
            np1 = None
            np2 = None
            NewWipeouts = payload['wipeouts']
            # Bewegung nach rechts
            if dx == 1:
                if (p1[0] + 1) != n and labyrinth1["vertical_walls"][p1[1]][p1[0]] == 0:
                    np1 = (p1[0] + dx, p1[1] + dy)
                if (p2[0] + 1) != n and labyrinth2["vertical_walls"][p2[1]][p2[0]] == 0:
                    np2 = (p2[0] + dx, p2[1] + dy)
            # Bewegung nach links
            if dx == -1:
                if (p1[0] - 1) >= 0 and labyrinth1["vertical_walls"][p1[1]][p1[0] - 1] == 0:
                    np1 = (p1[0] + dx, p1[1] + dy)
                if (p2[0] - 1) >= 0 and labyrinth2["vertical_walls"][p2[1]][p2[0] - 1] == 0:
                    np2 = (p2[0] + dx, p2[1] + dy)
            # Bewegung nach unten
            if dy == 1:
                if (p1[1] + 1) != m and labyrinth1["horizontal_walls"][p1[1]][p1[0]] == 0:
                    np1 = (p1[0] + dx, p1[1] + dy)
                if (p2[1] + 1) != m and labyrinth2["horizontal_walls"][p2[1]][p2[0]] == 0:
                    np2 = (p2[0] + dx, p2[1] + dy)
            # Bewegung nach oben
            if dy == -1:
                if (p1[1] - 1) >= 0 and labyrinth1["horizontal_walls"][p1[1] - 1][p1[0]] == 0:
                    np1 = (p1[0] + dx, p1[1] + dy)
                if (p2[1] - 1) >= 0 and labyrinth2["horizontal_walls"][p2[1] - 1][p2[0]] == 0:
                    np2 = (p2[0] + dx, p2[1] + dy)
            
            # Falls ein Charakter am Ziel angekommen ist -> nicht wegbewegen
            if p1 == goal:
                np1 = p1
            if p2 == goal:
                np2 = p2

            if np1 is None:
                np1 = p1
            if np2 is None: 
                np2 = p2

            # Falls Charakter auf Gruben -> zurück zum Startpunkt 
            if np1 in labyrinth1["pits"]:
                np1 = (0, 0)
                if NewWipeouts[1] == True: # Falls der Charakter im Labyrinth 2 schon mal in eine Grube gefallen ist -> Bewegung verwerfen
                    continue
                NewWipeouts = (True, False) # Der Charakter im Labyrinth 2 darf nicht mehr in eine Grube fallen.
            if np2 in labyrinth2["pits"]:
                np2 = (0, 0)
                if NewWipeouts[0] == True: # Falls der Charakter im Labyrinth 1 schon mal in eine Grube gefallen ist -> Bewegung verwerfen
                    continue
                NewWipeouts = (False, True) # Der Charakter im Labyrinth 1 darf nicht mehr in eine Grube fallen.

            # Schon bereits besucht? -> Bewegung verwerfen
            if (np1, np2) in visited:
                continue

            # Bewegungssymbol bestimmen
            if dy == 1:
                movementletter = "S"
            if dy == -1:
                movementletter = "W"
            if dx == 1:
                movementletter = "D"
            if dx == -1:
                movementletter = "A"

            # Falls beide Charaktere am Ziel angekommen sind.
            if np1 == goal and np2 == goal:
                while True:
                    # Bewegungssymbol rekursiv wiederherstellen, indem man die Bewegungen von vorherigen Stellungen anschaut
                    movementletter = payload["movement"] + movementletter
                    if payload['before'] is None: # Falls keine weiteren vorherigen Stellungen gibt -> Bewegungen zurückgeben.
                        return movementletter
                    payload = payload['before'] # Zur vorherigen Stellung zurückgehen.
            
            # Punktzahlkontrolle: Labyrinth 1
            if solution1[payload['progress1'] - 1] == np1: # Ist der Charakter zurückgegangen? -> Punktabzug
                newProgress1 = payload['progress1'] - 1
            elif payload['progress1'] + 2 != len(solution1) and solution1[payload['progress1'] + 1] == np1: # Ist der Charakter vorwärts gegangen? -> Punktbelohnung
                newProgress1 = payload['progress1'] + 1
            else:
                newProgress1 = payload['progress1'] # Keine Veränderung bzw. Punkte zurücksetzen wenn der Charakter wieder beim Startpunkt befindet.
                if np1 == (0, 0):
                    newProgress1 = 0
            # Punktzahlkontrolle: Labyrinth 2
            if solution2[payload['progress2'] - 1] == np2:
                newProgress2 = payload['progress2'] - 1
            elif payload['progress2'] + 2 != len(solution2) and solution2[payload['progress2'] + 1] == np2:
                newProgress2 = payload['progress2'] + 1
            else:
                newProgress2 = payload['progress2']
                if np2 == (0, 0):
                    newProgress2 = 0

            # Fortschrittskontrolle: Mind. 1 Labyrinth muss 1 Punkt bekommen haben.
            if newProgress1 <= payload["progress1"] and newProgress2 <= payload['progress2']:
                continue
            
            # Punktzahlkontrolle: Ist die aktuelle Punktzahl zu niedrig?
            if (newProgress1 + newProgress2 + progressPuffer) < best:
                continue
            
            # Bei neuer Rekordpunktzahl -> als Rekord speichern
            if (newProgress1 + newProgress2) > best:
                best = newProgress1 + newProgress2

            newPayload = {
                "progress1":newProgress1,
                "progress2":newProgress2,
                "position1":np1,
                "position2":np2,
                "movement":movementletter,
                "wipeouts":NewWipeouts,
                "before": payload,
            }
            visited.add((np1, np2)) # Stellung als besucht markieren
            queue.append(newPayload)

    # Bei keiner Lösung müssen die Kriterien für die Punktzahlkontrolle niedriger gestellt werden, um alternative Wege auszuprobieren.
    # Diese Zeile wurde bei keiner Beispielsaufgabe verwendet. Trotzdem als Failsafe implementiert, schließlich muss es eine Lösung geben.
    return solve_duo_labyrinth(dimensions, labyrinth1, labyrinth2, solution1, solution2, progressPuffer + 5)

def main(filename):
    # Beispielsaufgabe lesen
    with open("Beispiele\\" + filename, 'r') as f:
        content = f.read()

    # Labyrinth als Dictionary laden
    labyrinths = read_labyrinth(content)
    print(f"filename: {filename}")
    paths = [] # Positionenliste
    movements = [] # Bewegungsliste
    for key in ["labyrinth_1", "labyrinth_2"]:
        labyrinth = labyrinths[key]
        path, movement = solve_labyrinth(
            labyrinths["dimensions"],
            labyrinth["vertical_walls"],
            labyrinth["horizontal_walls"],
            labyrinth["pits"],
        )
        paths.append(path)
        movements.append(movement)
    
    # Kontrolle, ob alle Labyrinthe sich lösen lassen.
    if (paths[0] is None) and (paths[1] is None):
        print("No solutions for both.")
        return
    if (paths[0] is None):
        print("No solution for labyrinth 1")
        print(f"Amount of Actions: {len(movements[1])}")
        print(movements[1])
        return
    if (paths[1] is None):
        print("No solution for labyrinth 2")
        print(f"Amount of Actions: {len(movements[0])}")
        print(movements[0])
        return
    
    # Beide Labyrinthe unter parallelen Bedingungen lösen
    movement = solve_duo_labyrinth(
        labyrinths["dimensions"],
        labyrinths["labyrinth_1"],
        labyrinths["labyrinth_2"],
        paths[0],
        paths[1],
    )
    print(f"Amount of Actions: {len(movement)}")
    for i in movement:
        print(i, end="")
    print()
        
def timetest(filename):
    from time import time
    start = time()
    main(filename)
    end = time() - start
    print(f"Required time: {end}")

if __name__ == '__main__':
    main("labyrinthe0.txt")
    main("labyrinthe1.txt")
    main("labyrinthe2.txt")
    main("labyrinthe3.txt")
    main("labyrinthe4.txt")
    main("labyrinthe5.txt")
    main("labyrinthe6.txt")
    main("labyrinthe7.txt")
    main("labyrinthe8.txt")
    main("labyrinthe9.txt")
    main("EdgeCase_1.txt")
    #timetest("labyrinthe0.txt")
    #timetest("labyrinthe1.txt")
    #timetest("labyrinthe2.txt")
    #timetest("labyrinthe3.txt")
    #timetest("labyrinthe4.txt")
    #timetest("labyrinthe5.txt")
    #timetest("labyrinthe6.txt")
    #timetest("labyrinthe7.txt")
    #timetest("labyrinthe8.txt")
    #timetest("labyrinthe9.txt")
    #timetest("EdgeCase_1.txt")