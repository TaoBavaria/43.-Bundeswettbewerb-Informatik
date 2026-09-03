"""
Bundeswettbewerb Informatik 2024 Runde 2 Aufgabe 1 - B
Autor: Tao Zheng
"""

class Knote:
    def __init__(self, letter, amount, childrens=None):
        # Knoten erstellen
        # letter: Buchstabe oder Nichts
        # amount: Häufigkeit der Buchstaben
        # childrens: Untere Knoten
        self.letter = letter
        self.amount = amount
        if childrens is None:
            self.childrens = []
        else:
            self.childrens = childrens
    
    def __lt__(self, other):
        return self.amount < other.amount
    
    def totalSize(self, weight):
        # Gesamtgröße zurückgeben
        if not self.letter is None:
            return self.amount * weight
        sum = 0
        for i in range(len(self.childrens)):
            sum += self.childrens[i].totalSize(weight + 1)
        return sum

    def strOut(self, code=""):
        # Alle Huffman-Codes zurückgeben
        text = ""
        if not self.letter is None:
            text = f"{self.letter} ({self.amount}): {code}\n"
        for i in range(len(self.childrens)):
            text += self.childrens[i].strOut(code + str(i))
        return text

    def printOut(self):
        # Alle Huffman-Codes ausdrucken
        print(self.strOut())

def main(filename):
    # Datei Lesen
    with open(f"Beispiele\\{filename}", encoding="utf-8") as f:
        nPerle = int(f.readline())
        dPerle = [int(i) for i in f.readline().split(" ")]
        sentence = f.readline().strip("\n")

    # Anzahl Buchstaben zählen
    charmap = {}
    charset = set()
    for letter in sentence:
        if letter in charset:
            charmap[letter] += 1
        else:
            charmap[letter] = 1
            charset.add(letter)

    # voraussichtliche Überschuss berechnen
    Joker = (len(charmap)-2)%(nPerle-1)+2
    #if Joker == nPerle:
    #    Joker = 0

    # Knoten erstellen
    Knoten = [Knote(i, charmap[i]) for i in charmap.keys()]
    Knoten.sort(reverse=True)

    while len(Knoten) > 1:
        # Huffman Codierung anwenden
        childrens = [Knoten.pop() for i in range(Joker if Joker > 0 else nPerle)]
        Joker = 0
        amount = 0
        for child in childrens:
            amount += child.amount
        KnotenNeu = Knote(letter=None, amount=amount, childrens=childrens)
        Knoten.append(KnotenNeu)
        Knoten.sort(reverse=True)

    # Speichern
    totalSize = Knoten[0].totalSize(0)
    with open(f"Ergebnis\\ERGEBNIS_huffman_limited_"+filename, "w", encoding="utf-8") as f:
        f.write(f"{filename}\nTotalsize: {totalSize}\nConverted in length: {totalSize/10}cm\n")
        f.write(Knoten[0].strOut())
    print(f"{filename}: {totalSize} -> {totalSize/10}cm")

def timetest(filename):
    from time import time
    start = time()
    main(filename)
    end = time() - start
    print(f"Required time: {end}")

if __name__ == '__main__':
    main("schmuck0.txt")
    main("schmuck00.txt")
    #main("schmuck1.txt")
    main("schmuck01.txt")
    #main("schmuck2.txt")
    #main("schmuck3.txt")
    #main("schmuck4.txt")
    #main("schmuck5.txt")
    #main("schmuck6.txt")
    #main("schmuck7.txt")
    #main("schmuck8.txt")
    #main("schmuck9.txt")
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