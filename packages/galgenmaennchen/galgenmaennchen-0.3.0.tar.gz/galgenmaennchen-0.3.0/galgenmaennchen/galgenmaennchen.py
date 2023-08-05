"""
Ein Modul zum Spielen von galgenmaennchen.
Funktionen:

galgenmaennchen.get_word(): Bekomme ein zufälliges Wort von _galgenmaennchen.galgenmaennchen_word_list.
galgenmaennchen.play(word): Spiele eine Runde Galgenmännchen mit einem bestimmten Wort.
galgenmaennchen.galgenmaennchen(): das normale Spiel. Normalerweise die beste Option.
"""

__all__ = [
    "get_word",
    "play",
    "galgenmaennchen"
]


import random, _galgenmaennchen, time, os


def get_word(mode="j", maxsize=100, minsize=3):
    """
    Bekomme ein Wort von _galgenmaennchen.galgenmaennchen_word_list.
    param mode - Der Modus vom zurückgegebenen Wort. Normalwert ist "v" für Wörtern mit Vokalen und ohne spezielle Charakter.
    Andere Möglichkeiten:
    n für Nomen
    l für kleingeschriebene Wörter (z.B. Verben oder Adjektive)
    a für alle Wörter ohne spezielle Charakter (ohne Vokale)
    s für Wörter mit speziellen Charaktern
    j für jedes mögliche Wort (echter Zufall)
    """
    word = random.choice(_galgenmaennchen.galgenmaennchen_word_list)
    if len(word) <= maxsize and len(word) >= minsize:
        if mode=="v":
            if word.isalpha():
                if any(c in word for c in "aeiouyäöü"):
                    return word
                else:
                    return get_word(maxsize=maxsize, minsize=minsize)
            else:
                return get_word(maxsize=maxsize, minsize=minsize)
        elif mode=="n":
            if word.isalpha():
                if any(c in word for c in "aeiouyäöü") and word.title() == word:
                    return word
                else:
                    return get_word(mode="n", maxsize=maxsize, minsize=minsize)
            else:
                return get_word(mode="n", maxsize=maxsize, minsize=minsize)
        elif mode=="a":
            if word.isalpha():
                return word
            else:
                return get_word(mode="a", maxsize=maxsize, minsize=minsize)
        elif mode=="s":
            if not word.isalpha():
                return word
            else:
                return get_word(mode="s", maxsize=maxsize, minsize=minsize)
                
        elif mode=="j":
            return word
    else:
        return get_word(mode=mode, maxsize=maxsize, minsize=minsize)


def play(raw_word):
    """
    param raw_word - Das Wort, mit dem du spielen möchtest
    Spiele ein Spiel galgenmaennchen mit einem bestimmmten Wort.
    Wird intern von galgenmaennchen.galgenmaennchen() verwendet.
    """
    
    
    word = raw_word.upper()
    used_solution = False
    word_completion = ""
    for w in raw_word:
        if w.isalpha():
            word_completion += "_"
        else:
            word_completion+=w
    guessed = False
    guessed_letters = []
    guessed_words = []
    
    
    tries = len(_galgenmaennchen.galgenmaennchen_stages)-1
    print(os.environ["username"].strip().title(),", " "lasst uns galgenmaennchen spielen!", sep="")
    print(_galgenmaennchen.galgenmaennchen_stages[tries])
    print(word_completion)
    print("\n")
    
    while not guessed and tries > 0:
        guess = input("Bitte rate einen Buchstaben oder ein Wort: ").upper().strip()
        print(guess)
        if len(guess) == 1: # and guess.isalpha():
            if guess in guessed_letters:
                print("Du hast schon ", guess, " geraten.")
            elif guess not in word:
                print(guess, "ist nicht im Wort.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Gut gemacht,", guess, "ist im Wort!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif guess == "SOLUTION":
            used_solution = True
            guessed = True
            word_completion = word
            print("sol")
        elif len(guess) == len(word): #  and guess.isalpha():
            if guess in guessed_words:
                print("Du hast schon" + guess + "geraten.")
            elif guess != word:
                print(guess, "ist leider falsch.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
                tries+=2
        elif len(guess) > len(word):
            print("Zu viele Buchstaben.")
        elif len(guess) == 0:
            print("Du hast nichts eingegeben. Gib bitte etwas ein.")
        else:
            print("Ungültige Eingabe.")
        strgl = str(sorted(guessed_letters))
        print("Du hast schon diese Buchstaben geraten: ",strgl[1:len(strgl)-1].replace("'", ""))
        if guessed_words:
            strgw = str(sorted(guessed_words))
            print("Du hast schon diese Wörter geraten: ", strgw[1:len(strgw)-1].replace("'", ""))
        print("Noch", tries, "Versuche")
        print(_galgenmaennchen.galgenmaennchen_stages[tries])
        print(word_completion)
        
        print("\n")
    if guessed and not used_solution:
        print("Du hast es geschafft! Du hast das Wort " +raw_word+" in", len(_galgenmaennchen.galgenmaennchen_stages)-tries, "Versuchen erraten!")
        return tries
    elif guessed and used_solution:
        print("Es macht doch keinen Spaß, zu schummeln.")
        return -100
    else:
        print("Schade, du hast leider keine Versuche mehr." , raw_word , "wäre richtig gewesen. Vielleicht beim nächsten Mal!")
        return False
    
    







def galgenmaennchen(getmode="j", maxlen=100, minlen=3):
    """Spiele galgenmaennchen."""
    score = 0
    if os.path.exists("C://Python38/Lib/assets/scores.txt"):
        with open("C://Python38/Lib/assets/scores.txt") as f:
            global highscore
            try:
                highscore = int(f.read())
            except Exception:
                highscore = 0
                global not_found
                not_found = true
        raw_word = get_word(mode=getmode)
    else:
        with open("C://Python38/Lib/assets/scores.txt", "w") as f:
            f.write("0")
            highscore = 0
        raw_word = get_word(mode=getmode, maxsize=maxlen, minsize=minlen)
        
    word = get_word(mode=getmode).upper().strip()
    
    p = int(play(raw_word))
    if p:
        while input("Nochmal spielen? (Y/N) ").upper() == "Y":
            raw_word = get_word()
            word = get_word(mode=getmode).upper().strip()
            for i in range(10):
                time.sleep(.1)
                print(-i+10)
            
            p = int(play(raw_word))
            score+=p if p else 0
        if score > highscore:
            highscore = score
            with open("C://Python38/Lib/assets/scores.txt", "w") as f:
                f.write(str(score))
                print("Toll, du hast den Highscore gebrochen! Der neue Highscore ist ", score, "!", sep="")
        else:
            print("Schade, den Highscore von", highscore, "hast du mit deinen", score, "leider nicht gebrochen.\nVersuche es doch noch einmal!")
    
g = galgenmaennchen


if __name__ == "__main__":
    g(getmode="j")


    
