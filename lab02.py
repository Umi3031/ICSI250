import random
import string

def load_words(filename="words.txt"):
    """file-aas ugiin jaagsaltiig ashaalna"""
    try:
        with open("C:\\Users\\user\\Downloads\\hangman\\words.txt", "r", encoding="utf-8") as file: #file-iin  bairshil 
            words=[line.strip() for line in file if line.strip()]
        print(f"Loading word list from file...\n{len(words)} words loaded.")
        return words
    except FileNotFoundError:
        print("Error: words.txt file oldsongui! Zamiig shalgana uu.")
        return []

def choose_word(wordlist):
    """Jagsaaltaas sanamsargui neg ug songono uu"""
    return random.choice(wordlist) if wordlist else None # random.choice() ashiglaj sanamsargui ug songono

def match_with_gaps(my_word, other_word):
    """my_word-iin dooguur zuraas bolon other_word-iig khartsuulaj tokhirokh esekhiig shalgalna"""
    my_word=my_word.strip()
    other_word=other_word.strip()
    idx=0
    new_word=""
    for i in my_word:
        if i==' ':
            continue
        new_word+=i
   # print(new_word)
   # print(other_word)
    if len(new_word)==len(other_word):
        for i in new_word:
            if i=='_':
                idx+=1
                continue
            if i!=other_word[idx]:
                return False
            idx+=1
        return True
    else:
        return False

def show_possible_matches(my_word, word_list):
    """my_word-iin tokhirokh ugsiig word_list-ees khaij olj kharuulna"""
    matches=[word for word in word_list if match_with_gaps(my_word, word)] #word_list dotor my wordtoi tarakh bolomjit ugsiig shuuj baruulna
    
    if matches:
        print("Possible word matches are:")
        print(" ".join(matches))
    else:
        print("No matches found")

def get_guessed_word(secret_word, letters_guessed): #secret_Wword dotor ali usgiig taasan baigaag haruulna
    """Taamaglasan uguudiig kharuulakh"""
    ret=''
    for i in secret_word:
        guessed=0
        for j in letters_guessed:
            if i==j:
                guessed=1
                break
        if guessed==1:
            ret+=i
        else:
            ret+='_ '
    return ret

def is_vowel(guess, secret_word):
    #Y is considered to be a vowel if… The word has no other vowel: gym, my.
    vowels = ['a', 'e', 'i', 'o', 'u']
    y_occ=0
    if guess in vowels: 
        return True
    for i in secret_word:
        if i=='y':
            y_occ+=1
    if y_occ!=0:
        return True
    else:
        return False

def is_word_guessed(secret_word, letters_guessed):
    """tokhirokh uguud taagdsan esekhiig shalgana"""
    l=len(secret_word)
    cnt=0
    for i in letters_guessed:
        for j in secret_word:
            if i==j:
                cnt+=1 
    if cnt==l: 
        return True
    else:
        return False

def valid_input(warnings, letters_guessed):
    """Toglogchiin zuw oruulsan useg esbel tuslamj abakh shalgalt"""
    guess = input("Please guess a letter: ").lower()
    
    if len(guess) != 1 or not guess.isalpha():
        if warnings > 0:
            warnings -= 1
            print(f"Invalid letter. You have {warnings} warnings left.")
            return None
        else:
            print("No warnings left. You lose a guess.")
            return None
    
    if guess in letters_guessed:
        print(f"You've already guessed {guess}. Try again.")
        return None
    
    return guess

def hangman_with_hints():
    """Hangman togloomiin tuslamjtai khubilbar"""
    word_list=load_words()
    secret_word=choose_word(word_list)
    letters_guessed=set()
    attempts=6
    warnings=3

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-----Umi-----")

    while attempts>0:
        print(f"You have {attempts} guesses left.")
        print(f"You have {warnings} warnings left.")
        print(f"Available letters: {string.ascii_lowercase}")
        print(f"Word to guess: {get_guessed_word(secret_word, letters_guessed)}")

        guess=valid_input(warnings, letters_guessed)

        if guess is None:
            attempts-=1
            continue

        if guess=='*':  # tuslamj husekh
            show_possible_matches(get_guessed_word(secret_word, letters_guessed), word_list)
            continue

        letters_guessed.add(guess)

        if guess in secret_word:
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        else:
            if is_vowel(guess, secret_word):
                attempts -= 2
                print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                attempts -= 1
                print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")

        print("------Umi----")

        if is_word_guessed(secret_word, letters_guessed):
            print(f"Congratulations, you won!")
            score=attempts*len(secret_word)
            print(f"Your total score for this game is: {score}")
            break

    if attempts==0 and not is_word_guessed(secret_word, letters_guessed):
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
        print("Game Over")

def hangman():
    """Hangman toglomiin engiin khubilbar, hamgiin ekhend hiij guisetgsen hangman
    shalgakhdaa heregtei geed bodood ustgsangui"""
    words=load_words("C:\\Users\\user\\Downloads\\hangman\\words.txt")
    if not words:
        return
    secret_word=choose_word(words)
    guessed_letters=set()
    attempts=int(input("Kheden udaa taakh bolomjtoi be: "))

    print("Nuuts ug n", "_ " * len(secret_word))

    while attempts > 0:
        guess = input("Useg oruulna uu: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Neg useg oruulna uu!")
            continue

        if guess in guessed_letters:
            print("Ene usgiig ali hediin oruulsan baina")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Nice!", end=" ")
        else:
            attempts -= 1
            print(f"Buruu! Ulsen bolomj: {attempts}")

        displayed_word = " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])
        print(displayed_word)

        if "_" not in displayed_word:
            print("Nice! Ta gal yum bna: ", secret_word)
            return

    print("Ta bukh bolomjoo ashiglalaa. Nuuts ug: ", secret_word)

if __name__ == "__main__":
    # Hangman toglomiin  tuslamjtai khubilbar
    hangman_with_hints()
    
    # engiin Hangman togloomiin khubilbar
    # hangman()
