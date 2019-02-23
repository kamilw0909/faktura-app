def konwertuj(lista):
    jednosci = ["zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć",
     "siedem", "osiem", "dziewięć"]
    dziesiatki = ["", "dziesięć", "dwadzieścia", "trzydzieści", "czterdzieści",
     "pięćdziesiąt", "sześćdziesiąt", "siedemdziesiąt", "osiemdziesiąt",
     "dziewięćdziesiąt"]
    setki = ["", "sto", "dwieście", "trzysta", "czterysta", "pięćset",
     "sześćset", "siedemset", "osiemset", "dziewięćset"]
    nascie = ["dziesięć", "jedenaście", "dwanaście", "trzynaście",
     "czternaście", "piętnaście", "szesnaście", "siedemnaście",
     "osiemnaście", "dziewiętnaście"]
    a, b, c = map(int, lista)
    if a == 0 and b == 0 and c == 0:
        return ""
    wynik = ""
    if a != 0:
        wynik += setki[a] + " "
    if b != 0:
        if b == 1:
            return wynik + nascie[c] + " "
        else:
            wynik += dziesiatki[b] + " "
    if c != 0:
        wynik += jednosci[c] + " "
    return wynik
 
 
def dopisek(lista, licznik):
    wielkie = ["", "tysiąc", "milion", "miliard", "bilion", "biliard",
    "trylion", "tryliard", "kwadrylion", "kwadryliard", "kwintylion",
    "kwintyliard", "sekstylion", "sekstyliard", "septylion", "septyliard",
    "oktylion", "oktyliard", "nonilion", "noniliard", "decylion", "decyliard",
    "undecylion", "undecyliard", "duodecylion", "duodecyliard", "trycylion",
    "trycyliard", "kwadragilion", "kwadragiliard", "oktogilion", "oktogiliard",
    "centylion", "centyliard"]
    if licznik == 0:
        return ""
    a = 0
    b = 0
    c = 0
    if len(lista) == 1:
        c = int(lista[0])
    if len(lista) == 2:
        b = int(lista[0])
        c = int(lista[1])
    if len(lista) == 3:
        a = int(lista[0])
        b = int(lista[1])
        c = int(lista[2])
    if a == 0 and b == 0 and c == 1:
        if licznik == 1:
            return "tysiąc "
        else:
            return wielkie[licznik] + " "
    if b == 1:
        if licznik == 1:
            return "tysięcy "
        else:
            return wielkie[licznik] + "ów "
    else:
        if c == 2 or c == 3 or c == 4:
            if licznik == 1:
                return "tysiące "
            else:
                return wielkie[licznik] + "y "
        else:
            if licznik == 1:
                return "tysięcy "
            else:
                return wielkie[licznik] + "ów "
 
 
def main(liczba):
    #liczba = int(str(liczba).split('.')[0])
    if liczba == 0:
        print("zero")
        return
    liczba = str(liczba)
    reszta = len(liczba) % 3
    wynik = ""
    dlugosc = int((len(liczba) - 1) / 3)
    if reszta == 1:
        wynik += konwertuj('0' + '0' + liczba[0])
        wynik += dopisek('0' + '0' + liczba[0], dlugosc)
        dlugosc -= 1
        liczba = liczba[1:]
    if reszta == 2:
        wynik += konwertuj('0' + liczba[0] + liczba[1])
        wynik += dopisek('0' + liczba[0] + liczba[1], dlugosc)
        dlugosc -= 1
        liczba = liczba[2:]
    for i in range(0, len(liczba), 3):
        wynik += konwertuj(liczba[i] + liczba[i + 1] + liczba[i + 2])
        if liczba[i] != '0' or liczba[i + 1] != '0' or liczba[i + 2] != '0':
            wynik += dopisek(liczba[i] + liczba[i + 1] + liczba[i + 2], dlugosc)
        dlugosc -= 1
    return(wynik)

if __name__ == "__main__":
    kwota = input('Podaj liczbę: ')
    print(main(kwota))