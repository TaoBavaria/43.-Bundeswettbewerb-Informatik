"""
Bundeswettbewerb Informatik 2024 Runde 1 Aufgabe 2
Autor: Tao Zheng
"""

#--------------------------------------------------------
def mathfunction(x):
    # vgl. Geogebra Grafik
    if x <= 0.1: return 0.5
    if x < 2.5:
        return 0.5*(-1/3*(x-0.1)+1)
    else:
        return 0.1

def diff(lower, higher) -> float:
    factor = 1
    delta = abs(lower - higher)
    output = mathfunction(delta)
    # Erwartet: Gleichung entspricht nicht die Werteverhältnis und sind mind. 0.5 Werteinheiten entfernt
    expected = not ((delta >= 0.5) and (lower > higher))
    if not expected:
        factor += 0.2
    # Unerwartete Ergebnisse Umrechnung
    if not expected and delta < 0.9:
        output = 1.3/3
    elif not expected and delta >= 0.9:
        output = 0.8 - output
    return output * factor

def main(m,k,examsHistory,k_var):
    Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tasks = {}
    for i in range(m):
        tasks.update({Letters[i]:0.0})
    del Letters

    # Die Schwierigkeitsgradwerte ausrechnen
    # Für alle vergangenen Prüfungen
    for exams in examsHistory:
        pendingTasksUpdates = tasks.copy()
        # Für alle Distanzen
        for distance in range(1,len(exams)):
            # Für einzelne Gleichungen
            for pointer in range(len(exams) - distance):
                pointerLetter = exams[pointer]
                targetLetter = exams[pointer + distance]
                pendingTasksUpdates[pointerLetter] -= diff(tasks[pointerLetter], tasks[targetLetter])
                pendingTasksUpdates[targetLetter] += diff(tasks[pointerLetter], tasks[targetLetter])
            # Nachdem alle Veränderungen für eine Distanz ausgerechnet wurden, Ergebnis speichern.
            tasks = pendingTasksUpdates

    # Gewünschte Prüfungen sortieren und ausgeben
    sorted_tasks = sorted(tasks.keys(), key=tasks.get)
    targetKeys = [key for key in sorted_tasks if key in k_var]
    print(targetKeys[0], end="")
    for i in range(k-1):
        # Ausnahmefall: zwei Gleichungen haben die gleiche Wert
        if tasks[targetKeys[i]] == tasks[targetKeys[i + 1]]:
            print(" = ", end=targetKeys[i + 1])
        else:
            print(" < ", end=targetKeys[i + 1])
    print()
    # Tatsächliche Schwierigkeitswert ausdrucken.
    for key in targetKeys:
        print(f"{key}: {tasks[key]}")

if __name__ == '__main__':
    with open("A2_Schwierigkeiten\\schwierigkeiten5.txt") as f:
        n,m,k = [int(var) for var in f.readline().split(" ")]
        examsHistory = [next(f)[0:-1].strip(" ").split(" < ") for i in range(n)]
        # .strip(" ") ist da, um ein Problem mit der schwierigkeiten2.txt Datei zu reparieren
        k_var = next(f).split(" ")
    main(m, k, examsHistory, k_var)