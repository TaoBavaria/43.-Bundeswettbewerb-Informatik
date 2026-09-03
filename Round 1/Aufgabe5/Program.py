"""
Bundeswettbewerb Informatik 2024 Runde 1 Aufgabe 5
Autor: Tao Zheng
"""

Dateipfad = "A5_DasAegyptischeGrabmal\grabmal5.txt"
# Dateipfad einer der Beispieldateien.

CustomRecursionLimit = 0
# Bei mehr als ~1000 Abschnitten kann Python einen RecursionError auslösen. Um das zu umgehen,
# muss das RecursionLimit erhöht werden. (Der Standardwert wird für CustomRecursionLimit = 0 verwendet.)

#-------------------------------------------------------

from sys import setrecursionlimit
if CustomRecursionLimit != 0:
    setrecursionlimit(CustomRecursionLimit)

def Gehen(abschnitten, gesamt_abschnitte, position=0, ankunft_zeit=0, zurueck=False) -> str:
    #print(f"Gehen(position={position}, ankunft_zeit={ankunft_zeit}{f', zurueck={zurueck}' if zurueck else ''})")
    """
    Berechnet den Weg durch eine Serie von Abschnitten mit unterschiedlicher Dauer.

    Argumente:
    - abschnitten (list): Liste der Dauer der Abschnitte.
    - gesamt_abschnitte (int): Gesamtanzahl der Abschnitte.
    - position (int): Der aktuelle Abschnitt
    - ankunft_zeit (int): Die Zeit beim Betreten des Abschnittes
    - zurueck (bool): Kontext, ob man eine sofortige nach vorne laufen vermeiden sollte.

    Rückgabewerte:
    - str: Beschreibung der Schritte zum Ziel oder leere Menge bei falschem Wege.
    """
    
    # Basisfall: Wenn alle Abschnitte durchlaufen wurden.
    if position == gesamt_abschnitte:
        return f"{position}.\nDu bist angekommen. (Gesamtdauer: {ankunft_zeit} Minuten)"
    
    # Prüfen ob der aktuelle Abschnitt offen ist.
    if not zurueck and (ankunft_zeit // abschnitten[position]) % 2:
        schritte = Gehen(abschnitten, gesamt_abschnitte, position + 1, ankunft_zeit )
        if schritte != "":
            return schritte
    
    # Starte bei der aktuellen Zeit.
    aktuelle_zeit = ankunft_zeit

    naechste_abschnitt_dauer = abschnitten[position]

    # Überprüfen, ob man sich in einem Abschnitt befindet.
    aktuelle_abschnitt_dauer = 0
    if position != 0:
        aktuelle_abschnitt_dauer = abschnitten[position - 1]

    # Überprüfen, ob es eine vorherigen Abschnitt existiert.
    vorherige_abschnitt_moment = None
    vorherige_abschnitt_dauer = 0
    if position > 1:
        vorherige_abschnitt_dauer = abschnitten[position - 2]

    while True:
        # Berechne die Zeit bis der nächste Abschnitt wieder geöffnet wird
        zeit_bis_naechster_abschnitt = naechste_abschnitt_dauer*2 - ((aktuelle_zeit - naechste_abschnitt_dauer) % (naechste_abschnitt_dauer*2))

        # Prüfen, ob der aktuelle Abschnitt schließt, bevor der nächste geöffnet wird
        if aktuelle_abschnitt_dauer > 0:
            verbleibende_zeit_aktueller_abschnitt = aktuelle_abschnitt_dauer - (aktuelle_zeit  % aktuelle_abschnitt_dauer)

            if vorherige_abschnitt_dauer > 0:
                zeit_bis_vorherige_abschnitt = vorherige_abschnitt_dauer*2 - ((aktuelle_zeit - vorherige_abschnitt_dauer) % (vorherige_abschnitt_dauer*2))
                nicht_gleiche_abschnitt = (zeit_bis_vorherige_abschnitt + aktuelle_zeit - ankunft_zeit) > vorherige_abschnitt_dauer
                if verbleibende_zeit_aktueller_abschnitt > zeit_bis_vorherige_abschnitt and (zurueck or nicht_gleiche_abschnitt):
                    vorherige_abschnitt_moment = zeit_bis_vorherige_abschnitt + aktuelle_zeit
            
            if verbleibende_zeit_aktueller_abschnitt <= zeit_bis_naechster_abschnitt:
                if not vorherige_abschnitt_moment is None:
                    schritte = Gehen(abschnitten, gesamt_abschnitte, position - 1, vorherige_abschnitt_moment, True)
                    if schritte != "":
                        wartezeit = vorherige_abschnitt_moment - ankunft_zeit
                        return f"{position}.\nWarte {wartezeit} Minuten. Geh zurueck zu Abschnitt: " + schritte
                return "" # Der Weg funktioniert zeitlich nicht. Geh zurück!
                
        aktuelle_zeit += zeit_bis_naechster_abschnitt

        # Geh zum nächsten Abschnitt
        schritte = Gehen(abschnitten, gesamt_abschnitte, position + 1, aktuelle_zeit)
        if schritte != "":
            wartezeit = aktuelle_zeit - ankunft_zeit
            if position == 0:
                return f"Warte {wartezeit} Minuten. Geh zu Abschnitt: " + schritte
            return f"{position}.\nWarte {wartezeit} Minuten. Geh zu Abschnitt: " + schritte


if __name__ == '__main__':
    with open(Dateipfad) as f:
        n = int(f.readline())
        abschnitten = [int(i) for i in f.read().split("\n")]

    from time import time
    Start = time()
    print(Gehen(abschnitten, n))
    End = time()
    print(f"Dauer: {End - Start}")