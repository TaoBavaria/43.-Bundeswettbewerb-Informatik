"""
Bundeswettbewerb Informatik 2024 Runde 2 Aufgabe 2 - Zusatz
Autor: Tao Zheng
"""

def read_labyrinth(content):
    # Text vorbereiten
    lines = content.strip().split("\n")
    line = 0

    # Labyrinthgröße ablesen
    try:
        n, m, nlab = map(int, lines[line].split())
    except ValueError:
        n, m = map(int, lines[line].split())
        nlab = 2
    line += 1

    dimensions = (n, m)
    labyrinths = []
    for i in range(nlab):
        # Wände ablesen
        vertical_walls = [list(map(int, lines[line + j].split())) for j in range(m)]
        line += m

        horizontal_walls = [list(map(int, lines[line + j].split())) for j in range(m - 1)]
        line += m - 1

        # Anzahl Gruben ablesen
        num_pits = int(lines[line])
        line += 1

        # Gruben ablesen
        pits = []
        for j in range(num_pits):
            x, y = map(int, lines[line].split())
            pits.append((x, y))
            line += 1
        labyrinths.append(
                {
                "vertical_walls": vertical_walls,
                "horizontal_walls": horizontal_walls,
                "pits": set(pits),
            }
        )

    #print(labyrinths)
    # Zur Dictionary umwandeln und zurückgeben.
    return dimensions, labyrinths

def solve_labyrinth(dimensions, vertical_walls, horizontal_walls, pits):
    """
    solve labyrinth: Berechnet den Weg eines einzelnen Labyrinths.
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

def solve_n_labyrinth(dimensions, labyrinths, solutions, progressPuffer = 11):
    """
    solve n labyrinth: Berechnet Weg in n Labyrinthen gleichzeitig (2*n-dimensionale Labyrinthe).
    """
    n, m = dimensions
    goal = (n - 1, m - 1)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Rechts, Unten, Links, Oben
    best = 0 # Rekordpunktzahl
    nLabyrinths = len(labyrinths)
    payload = {
        "progress":[0 for _ in range(nLabyrinths)], # Punktzahl
        "positions":[(0,0) for _ in range(nLabyrinths)], # Koordinate Labyrinth
        "movements":"", # Bewegungssymbol
        "wipeouts": (False,)*nLabyrinths, # vgl. Wipeoutregel
        "before": None, # vorherige payload um vorherige Bewegungen rekursiv aufzulisten
    }
    visited = set() # Besuchte Koordinaten
    queue = [payload]
    while queue:
        payload = queue.pop(0)
        #print(payload)
        for dx, dy in directions:
            nps = []
            cancel = False
            newWipeouts = payload['wipeouts']
            for LabId in range(nLabyrinths):
                p = payload["positions"][LabId]
                np = None
                # Bewegung nach rechts
                if dx == 1:
                    if (p[0] + 1) != n and labyrinths[LabId]["vertical_walls"][p[1]][p[0]] == 0:
                        np = (p[0] + dx, p[1] + dy)
                # Bewegung nach links
                if dx == -1:
                    if (p[0] - 1) >= 0 and labyrinths[LabId]["vertical_walls"][p[1]][p[0] - 1] == 0:
                        np = (p[0] + dx, p[1] + dy)
                # Bewegung nach unten
                if dy == 1:
                    if (p[1] + 1) != m and labyrinths[LabId]["horizontal_walls"][p[1]][p[0]] == 0:
                        np = (p[0] + dx, p[1] + dy)
                # Bewegung nach oben
                if dy == -1:
                    if (p[1] - 1) >= 0 and labyrinths[LabId]["horizontal_walls"][p[1] - 1][p[0]] == 0:
                        np = (p[0] + dx, p[1] + dy)
                
                # Falls ein Charakter am Ziel angekommen ist -> nicht wegbewegen
                if p == goal:
                    np = p

                if np is None:
                    np = p

                # Falls Charakter auf Gruben -> zurück zum Startpunkt 
                if np in labyrinths[LabId]["pits"]:
                    np = (0, 0)
                    newWipeouts = newWipeouts[:LabId] + (True,) + newWipeouts[LabId + 1:]
                    if not (False in newWipeouts): # Falls alle Charaktere schon mal in eine Grube gefallen sind -> Bewegung verwerfen
                        cancel = True
                        break
                    
                nps.append(np)

            if cancel:
                #print("cancel called")
                continue
            # Schon bereits besucht? -> Bewegung verwerfen
            if tuple(nps) in visited:
                #print(visited)
                #print("visited failed")
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

            # Falls alle Charaktere am Ziel angekommen sind.
            #if not (False in (i == goal for i in nps)):
            if not (False in (i == goal for i in nps)):
                while True:
                    # Bewegungssymbol rekursiv wiederherstellen, indem man die Bewegungen von vorherigen Stellungen anschaut
                    movementletter = payload["movements"] + movementletter
                    if payload['before'] is None: # Falls keine weiteren vorherigen Stellungen gibt -> Bewegungen zurückgeben.
                        return movementletter
                    payload = payload['before'] # Zur vorherigen Stellung zurückgehen.
            
            # Punktzahlkontrolle
            newProgressList = []
            for nLab in range(nLabyrinths):
                if solutions[nLab][payload['progress'][nLab] - 1] == nps[nLab]: # Ist der Charakter zurückgegangen? -> Punktabzug
                    newProgress = payload['progress'][nLab] - 1
                elif payload['progress'][nLab] + 2 != len(solutions[nLab]) and solutions[nLab][payload['progress'][nLab] + 1] == nps[nLab]: # Ist der Charakter vorwärts gegangen? -> Punktbelohnung
                    newProgress = payload['progress'][nLab] + 1
                else:
                    newProgress = payload['progress'][nLab] # Keine Veränderung bzw. Punkte zurücksetzen wenn der Charakter wieder beim Startpunkt befindet.
                    if nps[nLab] == (0, 0):
                        newProgress = 0
                newProgressList.append(newProgress)

            # Fortschrittskontrolle: Mind. 1 Labyrinth muss 1 Punkt bekommen haben.
            if not (True in (payload['progress'][nLab] <= newProgressList[nLab] for nLab in range(nLabyrinths))):
                #print("Failed progression")
                continue
            
            # Punktzahlkontrolle: Ist die aktuelle Punktzahl zu niedrig?
            if (sum(newProgressList) + progressPuffer) < best:
                #print("Missed highscore")
                continue
            
            # Bei neuer Rekordpunktzahl -> als Rekord speichern
            if sum(newProgressList) > best:
                best = sum(newProgressList)

            newPayload = {
                "progress":newProgressList, # Punktzahl
                "positions": nps, # Koordinate Labyrinth
                "movements": movementletter, # Bewegungssymbol
                "wipeouts": newWipeouts, # vgl. Wipeoutregel
                "before": payload, # vorherige payload um vorherige Bewegungen rekursiv aufzulisten
            }
            visited.add(tuple(nps)) # Stellung als besucht markieren
            queue.append(newPayload)

    # Bei keiner Lösung müssen die Kriterien für die Punktzahlkontrolle niedriger gestellt werden, um alternative Wege auszuprobieren.
    # Diese Zeile wurde bei keiner Beispielsaufgabe verwendet. Trotzdem als Failsafe implementiert, schließlich muss es eine Lösung geben.
    #return solve_n_labyrinth(dimensions, labyrinths, solutions, progressPuffer + 5)
    return ""
def main(filename):
    # Beispielsaufgabe lesen
    with open("Beispiele\\" + filename, 'r') as f:
        content = f.read()

    # Labyrinth als Dictionary laden
    dimensions, labyrinths = read_labyrinth(content)
    print(f"filename: {filename}")
    paths = [] # Positionenliste
    movements = [] # Bewegungsliste
    for i in range(len(labyrinths)):
        labyrinth = labyrinths[i]
        path, movement = solve_labyrinth(
            dimensions,
            labyrinth["vertical_walls"],
            labyrinth["horizontal_walls"],
            labyrinth["pits"],
        )
        paths.append(path)
        movements.append(movement)
        print(movement)
    

    # Kontrolle, ob alle Labyrinthe sich lösen lassen.
    newLabyrinths = []
    newPaths = []
    for i, path in enumerate(paths):
        if path is None:
            print(f"Labyrinth {i} is not solveable.")
        else:
            newLabyrinths.append(labyrinths[i])
            newPaths.append(path)
    if len(labyrinths) == 1:
        print("There is only one labyrinth to solve.")
    if len(labyrinths) == 0:
        print("There is no labyrinth to solve.")
        return
    
    # Alle Labyrinthe unter parallelen Bedingungen lösen
    movement = solve_n_labyrinth(
        dimensions,
        newLabyrinths,
        newPaths,
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
    #main("labyrinthe0.txt")
    #main("labyrinthe1.txt")
    #main("labyrinthe2.txt")
    #main("labyrinthe3.txt")
    #main("labyrinthe4.txt")
    #main("labyrinthe5.txt")
    #main("labyrinthe6.txt")
    #main("labyrinthe7.txt")
    #main("labyrinthe8.txt")
    #main("labyrinthe9.txt")
    #main("EdgeCase_1.txt")
    #main("Custom_n-lab1.txt")
    #main("Custom_n-lab2.txt")
    #main("Custom_n-lab3-failure.txt")
    timetest("Custom_n-lab1.txt")
    timetest("Custom_n-lab2.txt")
    timetest("Custom_n-lab3-failure.txt")