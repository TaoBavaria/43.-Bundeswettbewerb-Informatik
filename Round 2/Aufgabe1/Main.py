"""
Bundeswettbewerb Informatik 2024 Runde 2 Aufgabe 1
Autor: Tao Zheng
"""

def getPrefix(codes, amounts, prefix, dPerle, weight = 0):
    if len(amounts) == 1:
        codes[prefix] = weight
        return
    
    groups = [[] for i in dPerle] # Eine Liste/Gruppe pro Perlenart
    sums = [0] * len(dPerle)
    
    # Jede Häufigkeit in eine Gruppe zuordnen
    for amount in amounts:
        index = sums.index(min(sums)) # Kleinste Werte priorisieren
        groups[index].append(amount) 
        sums[index] += amount * dPerle[index]
    
    # Für jede Gruppe die Häufigkeiten in weitere Untergruppen zuordnen.
    for i in range(len(dPerle)):
        if groups[i]:
            getPrefix(codes, groups[i], f"{prefix}{i}", dPerle, weight + dPerle[i])

def totalSize(prefixcodes, charmap, dPerle):
    total = 0 # Gesamtgröße
    # Für alle verschiedenen Zeichen durchführen
    for key in prefixcodes.keys():
        # Für jede Perlenart
        for i in range(len(dPerle)):
            # Anzahl der verwendeten Perlen * Gesamtzahl Häufigkeit des Zeichens * Perlengröße
            total += prefixcodes[key].count(f"{i}") * charmap[key] * dPerle[i]
    return total, f"{total/10} cm"

def main(filename):
    # Datei ablesen
    with open(f"Beispiele\\{filename}", encoding="utf-8") as f:
        nPerle = int(f.readline()) # Anzahl verschiedene Perlen
        dPerle = [int(i) for i in f.readline().split(" ")] # Perlendurchmesser
        sentence = f.readline().strip("\n")

    # Anzahl Buchstaben zählen
    charmap = {} # Buchstabe: Häufigkeit
    charset = set() # Hashmap statt Kontrolle über Listen, um die Laufzeit zu verringern
    for letter in sentence:
        if letter in charset:
            charmap[letter] += 1
        else:
            charset.add(letter)
            charmap[letter] = 1
    
    # Symbole und Häufigkeiten in zwei verschiedenen Listen trennen, wobei es die Reihenfolge der Häufigkeiten weiterhin behält.
    # Es wird absteigend abhängig von der Häufigkeit sortiert.
    # Es gilt x[a] >= x[b] für int a < int b
    charlist = list(i for i in charmap.items())
    charlist.sort(key=lambda i: i[1], reverse=True)
    amounts = [i[1] for i in charlist] # Alle Häufigkeiten sortiert (absteigend)
    symbols = [i[0] for i in charlist] # Alle Zeichen sortiert (absteigend)


    codes = {} # Kodierung : Gewicht
    getPrefix(codes, amounts, "", dPerle)

    # Alle Kodierungen nach deren Gewicht sortieren (aufsteigend)
    codesorted = dict(sorted(codes.items(), key=lambda i: i[1]))

    # Für alle Symbole (nach der Häufigkeit absteigend sortiert) eine Kodierung (nach dem Gewicht aufsteigend sortiert) zuweisen 
    NewCode = {} # Symbol : Kodierung
    for i, key in enumerate(codesorted.keys()):
        NewCode[symbols[i]] = key

    # Prefixcode ausdrucken
    amount, length = totalSize(NewCode, charmap, dPerle)
    with open(f"Ergebnis\\ERGEBNIS_default_{filename}", "w", encoding="UTF-8") as f:
        f.write(f"{filename}\nTotalsize: {amount}\nConverted in length: {length}\n")
        for key in charmap.keys():
            f.write(f"{key} {charmap[key]}: {NewCode[key]}\n")
    
    #print(f"{filename}: {amount} -> {length}")
    print(f"{amount} -> {length}")

def timetest(filename):
    from time import time
    start = time()
    main(filename)
    end = time() - start
    print(f"Required time: {end}")

if __name__ == "__main__":
    main("schmuck0.txt")
    main("schmuck00.txt")
    main("schmuck1.txt")
    main("schmuck01.txt")
    main("schmuck2.txt")
    main("schmuck3.txt")
    main("schmuck4.txt")
    main("schmuck5.txt")
    main("schmuck6.txt")
    main("schmuck7.txt")
    main("schmuck8.txt")
    main("schmuck9.txt")
    #timetest("schmuck0.txt")
    #timetest("schmuck00.txt")
    #timetest("schmuck1.txt")
    #timetest("schmuck01.txt")
    #timetest("schmuck2.txt")
    #timetest("schmuck3.txt")
    #timetest("schmuck4.txt")
    #timetest("schmuck5.txt")
    #timetest("schmuck6.txt")
    #timetest("schmuck7.txt")
    #timetest("schmuck8.txt")
    #timetest("schmuck9.txt")