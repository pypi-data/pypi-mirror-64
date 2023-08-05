"""Hangman, by Al Sweigart al@inventwithpython.com

A word-guessing game.
Tags: large, game, word, puzzle game"""
__version__ = 0

# A version of this game is featured in the book, "Invent Your Own
# Computer Games with Python. https://nostarch.com/inventwithpython

import random, sys

# Set up the constants:
HANGMAN_PICS = [r"""
 +--+
 |  |
    |
    |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
    |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
 |  |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|  |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|\ |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|\ |
/   |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|\ |
/ \ |
    |
====="""]
CATEGORY = 'Animals'
WORDS = 'ANT BABOON BADGER BAT BEAR BEAVER CAMEL CAT CLAM COBRA COUGAR COYOTE CROW DEER DOG DONKEY DUCK EAGLE FERRET FOX FROG GOAT GOOSE HAWK LION LIZARD LLAMA MOLE MONKEY MOOSE MOUSE MULE NEWT OTTER OWL PANDA PARROT PIGEON PYTHON RABBIT RAM RAT RAVEN RHINO SALMON SEAL SHARK SHEEP SKUNK SLOTH SNAKE SPIDER STORK SWAN TIGER TOAD TROUT TURKEY TURTLE WEASEL WHALE WOLF WOMBAT ZEBRA'.split()


def main():
    print('''HANGMAN
By Al Sweigart al@inventwithpython.com
''')

    # Setup variables for a new game:
    missedLetters = []
    correctLetters = []
    secretWord = random.choice(WORDS)

    while True: # Main game loop.
        drawHangman(missedLetters, correctLetters, secretWord)

        # Let the player enter their letter guess:
        guess = getPlayerGuess(missedLetters + correctLetters)

        if guess in secretWord:
            # The player has guessed correctly:
            correctLetters.append(guess)

            # Check if the player has won:
            foundAllLetters = True
            for i in range(len(secretWord)):
                if secretWord[i] not in correctLetters:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('Yes! The secret word is "' + secretWord + '"! You have won!')
                break
        else:
            # The player has guessed incorrectly:
            missedLetters.append(guess)

            # Check if player has guessed too many times and lost
            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                drawHangman(missedLetters, correctLetters, secretWord)
                print('You have run out of guesses!')
                print('The word was "{}"'.format(secretWord))
                break
        # At this point, go back to the start of the main game loop.

def drawHangman(missedLetters, correctLetters, secretWord):
    """Draw the current state of the hangman, along with the missed and
    correctly-guessed letters of the secret word."""
    print(HANGMAN_PICS[len(missedLetters)])
    print('The category is:', CATEGORY)
    print()

    # Show the previously guessed letters:
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    # Replace blanks with correctly guessed letters:
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    # Show the secret word with spaces in between each letter:
    for letter in blanks:
        print(letter, end=' ')

    print()


def getPlayerGuess(alreadyGuessed):
    """Returns the letter the player entered. This function makes sure the
    player entered a single letter they haven't guessed before."""
    while True: # Keep asking until the player enters a valid letter.
        print('Guess a letter.')
        guess = input()
        guess = guess.upper()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            print('Please enter a LETTER.')
        else:
            return guess


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit() # When Ctrl-C is pressed, end the program.
