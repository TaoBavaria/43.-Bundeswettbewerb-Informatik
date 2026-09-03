/*
Bundeswettbewerb Informatik 2024 Runde 1 Aufgabe 1
Autor: Tao Zheng
*/

Console.WriteLine("Tao's Hopsitexteditor (Drück [TAB] um zu speichern)");

Stack<int> pointerMoments = new Stack<int>();
Stack<int> targetMoments = new Stack<int>();
Stack<int> skipMoments = new Stack<int>();
string text = "";

int pos = 0;
ConsoleKeyInfo key;
int keyValue;

int nextPos = 0;
ConsoleColor nextPColor = ConsoleColor.Red;

int targetPos = 1;
ConsoleColor targetPColor = ConsoleColor.Blue;

(int, int) GetLocation(int Position)
{
    // lineare Position zur Koordinate umwandeln
    int LetterPos = Position % ((Console.WindowHeight - 2) * Console.WindowWidth);
    int y = LetterPos / Console.WindowWidth + 1;
    int x = LetterPos % Console.WindowWidth;
    return (x, y);
}
int GetValue(byte B)
{
    // Eingabe mithilfe der Tabelle von Junioraufgabe 2 in Werte umwandeln
    switch (B)
    {
        // ABC Großbuchstabe
        case >= 65 and <= 90:
            return (int)B - 64;
        // abc Kleinbuchstabe
        case >= 97 and <= 122:
            return (int)B - 96;
        // ä
        case 228:
        case 196:
            return 27;
        // ö
        case 246:
        case 214:
            return 28;
        // ü
        case 252:
        case 220:
            return 29;
        // ß
        case 223:
            return 30;
        // Backspace
        case 8:
            return -1;
        // Enter
        case 13:
            return -2;
        // Tab
        case 9:
            return -3;
        // ignorieren
        default:
            return 0;
    }
}
byte ReverseValue(int value)
{
    /* Werte mithilfe der Tabelle von Junioaufgabe 2 in bytes umwandeln.
    * Die zurückgegebene Bytes stehen für den bestimmten char (Nach UTF-8)
    */
    switch (value)
    {
        // A - Z
        case < 27:
            return (byte)(value + 64);
        // Ä
        case 27:
            return 228;
        // Ö
        case 28:
            return 246;
        // Ü
        case 29:
            return 252;
        // ß
        case 30:
            return 223;
        // failsafe
        default:
            Console.WriteLine("ReverseValue received " + value);
            return 0;
    }
}
void warning()
{
    // platziert einen Hinweis unter der nächsten SprungPosition und markiert die nächste TargetPoint
    int x, y;
    Console.BackgroundColor = targetPColor;
    (x, y) = GetLocation(targetPos);
    Console.SetCursorPosition(x, y);
    Console.Write(" ");

    (x, y) = GetLocation(nextPos);
    Console.SetCursorPosition(x, y + 1);
    Console.BackgroundColor = ConsoleColor.Red;
    Console.Write((char)ReverseValue(targetPos - nextPos));
    (x, y) = GetLocation(pos);
    Console.SetCursorPosition(x, y);
}
void ShiftValues(ConsoleKeyInfo key, int amount)
{
    // Bewegt alle Werte um Anzahl "amount"
    // mit dem Ziel, dass bei Zeichen die ignoriert werden weiterhin die Stellen richtig angezeigt werden.

    // nächste SprungPosition entfernen
    char text = ' ';
    if ((pos - amount) == nextPos) text = key.KeyChar;
    int x, y;
    (x, y) = GetLocation(nextPos);
    Console.SetCursorPosition(x, y);
    Console.BackgroundColor = ConsoleColor.Black;
    Console.Write(text);

    // Hinweis entfernen
    Console.SetCursorPosition(x, y + 1);
    Console.Write(" ");

    // targetPoint entfernen
    (x, y) = GetLocation(targetPos);
    Console.SetCursorPosition(x, y);
    Console.Write(" ");

    // neue SprungPosition markieren
    (x, y) = GetLocation(nextPos + amount);
    Console.SetCursorPosition(x, y);
    Console.BackgroundColor = nextPColor;
    Console.Write(" ");
    Console.BackgroundColor = ConsoleColor.Black;

    // SprungPosition und targetPoint bewegen.
    nextPos += amount;
    targetPos += amount;

    // TargetPoint und Hinweis neu markieren und anzeigen.
    warning();
}
void Pause(string text)
{
    // Pausiert das Programm bei wichtigen Hinweisen.
    Console.SetCursorPosition(0, 0);
    Console.Write(text + " Drück [TAB] um fortzufahren.");
    ConsoleKeyInfo input;
    do
    {
        input = Console.ReadKey(true);
    } while (input.KeyChar != 9);
    // Text entfernen
    Console.BackgroundColor = ConsoleColor.Black;
    Console.SetCursorPosition(0, 0);
    Console.Write(new string(' ', 31 + text.Length));
    return;
}
void deleteLine()
{
    // Bei fehlender Platz Zeile komplett löschen.
    // Die eingegebenen Zeichen sind weiterhin gespeichert,
    // werden jedoch nicht mehr angezeigt.
    int x, y;
    (x, y) = GetLocation(pos + 2 * Console.WindowWidth);
    Console.SetCursorPosition(0, y);
    Console.BackgroundColor = ConsoleColor.Black;
    Console.Write(new string(' ', Console.WindowWidth));
}

// flexible Koordinaten
int x, y;

// Erste Sprungposition markieren
(x, y) = GetLocation(nextPos);
Console.SetCursorPosition(x, y);
Console.BackgroundColor = nextPColor;
Console.Write(" ");

// Zweite Sprungposition markieren
warning();

while (true)
{
    // Auslösen wenn die zweite Seite erreicht wurde und die Konsole Platz braucht.
    if (pos / (Console.WindowWidth * (Console.WindowHeight - 5)) >= 1 && pos % Console.WindowWidth == 0)
    {
        deleteLine();
    }
    // Zeiger auf die richtige Stelle zurücksetzen.
    (x, y) = GetLocation(pos);
    Console.SetCursorPosition(x, y);
    if (pos == nextPos) Console.BackgroundColor = nextPColor;
    else Console.BackgroundColor = ConsoleColor.Black;
    key = Console.ReadKey();
    keyValue = GetValue((byte)key.KeyChar);
    if (keyValue == -3)
    // Bei TAB -> Speichern
    {
        File.WriteAllText("TaoZHopsitextoutput.txt", text);
        Pause("Datei wurde als TaoZHopsitextoutput.txt gespeichert.");
        Console.SetCursorPosition(x, y);
        continue;
    }
    else if (keyValue == -2)
    // Enter -> ignorieren.
    {
        continue;
    }
    else if (keyValue == -1)
    // Backspace -> Zeichen entfernen
    {
        if (pos == 0) continue;
        text = text.Remove(text.Length - 1);
        if (pos % Console.WindowWidth == 0)
        {
            (x, y) = GetLocation(pos - 1);
            Console.SetCursorPosition(x, y);
        }
        if (pos == nextPos)
        {
            Console.BackgroundColor = ConsoleColor.Black;
        }
        Console.Write(" ");
        pos -= 1;
        // Überprüfen, ob die letzten Zeichen vorher einer der SprungPosition waren
        if (targetMoments.TryPeek(out int targetMoment) && pos == targetMoment)
        {
            (x, y) = GetLocation(targetPos);
            Console.SetCursorPosition(x, y);
            Console.Write(" ");
            (x, y) = GetLocation(nextPos);
            Console.SetCursorPosition(x, y + 1);
            Console.Write(" ");
            ConsoleColor tempColor = targetPColor;
            targetPos = nextPos;
            targetPColor = nextPColor;
            nextPColor = tempColor;
            nextPos = targetMoments.Pop();
            warning();

            (x, y) = GetLocation(pos);
            Console.SetCursorPosition(x, y);
            Console.BackgroundColor = nextPColor;
            Console.Write(" ");
        }
        // Überprüfen, ob es einer der SprungPositionen war 
        else if (pointerMoments.TryPeek(out int pointerMoment) && pos == pointerMoment)
        {
            (x, y) = GetLocation(nextPos);
            Console.SetCursorPosition(x, y);
            Console.Write(" ");
            Console.SetCursorPosition(x, y + 1);
            Console.Write(" ");
            nextPos = pointerMoments.Pop();

            (x, y) = GetLocation(pos);
            Console.BackgroundColor = nextPColor;
            Console.SetCursorPosition(x, y);
            Console.Write(" ");
            warning();
        }
        // Überprüfen, ob der vorherige Zeichen einer der ignorierten Zeichen war.
        else if (skipMoments.TryPeek(out int skipMoment) && skipMoment == (pos + 1))
        {
            skipMoments.Pop();
            ShiftValues(key, -1);
        }
        continue;
    }
    else if (keyValue == 0)
    // ignorierbare Zeichen -> alle Zeichen müssen um eine Position verschoben werden.
    {
        text += key.KeyChar;
        pos += 1;
        skipMoments.Push(pos);
        ShiftValues(key, 1);
        continue;
    }
    else if (pos == nextPos)
    // Spezialfall: der nächste Zeichen ist einer der SprungPosition
    {
        // Überprüfen, ob der Wert zu einem Hopsitext mit gleicher Ausgang führt.
        if (keyValue == (targetPos - nextPos))
        {
            // Zeichen entfernen und den Nutzer darauf hinweisen.
            Console.SetCursorPosition(x, y);
            Console.Write(" ");
            Pause("Achtung, [" + key.KeyChar + "] ist nicht erlaubt. (Position " + (pos + 1) + ")");
            continue;
        }
        text += key.KeyChar;
        Console.BackgroundColor = ConsoleColor.Black;
        Console.SetCursorPosition(x, y + 1);
        Console.Write(" ");
        if ((nextPos + keyValue) > targetPos)
        {
            // Fall: der vorherige Sprungposition kommt nach der zweiten Sprungposition -> Rollenwechsel
            targetMoments.Push(pos);
            int tempPos = nextPos;
            ConsoleColor tempColor = nextPColor;
            nextPos = targetPos;
            nextPColor = targetPColor;
            targetPos = (tempPos + keyValue);
            targetPColor = tempColor;
        }
        else
        {
            // Fall: der vorherige Sprungposition bleibt vor der zweiten Sprungposition -> kein Rollenwechsel
            pointerMoments.Push(pos);
            nextPos += keyValue;
            (x, y) = GetLocation(nextPos);
            Console.SetCursorPosition(x, y);
            Console.BackgroundColor = nextPColor;
            Console.Write(" ");
        }
        pos += 1;
        warning();
        continue;
    }
    else
    // Sonst Zeichen setzen.
    {
        text += key.KeyChar;
    }
    pos += 1;
}