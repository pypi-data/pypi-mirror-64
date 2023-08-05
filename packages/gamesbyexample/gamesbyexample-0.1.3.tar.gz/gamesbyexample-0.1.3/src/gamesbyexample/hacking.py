"""Hacking, by Al Sweigart al@inventwithpython.com

The hacking mini-game from "Fallout 3". Find out which seven-letter
word is the password by using clues each guess gives you.
Tags: large, game, artistic"""

__version__ = 1

import random, sys

# Set up the constants:
# The "filler" characters for the board.
GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/\\'

# Load the WORDS list from a text file that has 7-letter words.
with open('sevenletterwords.txt') as dictionaryFile:
    WORDS = dictionaryFile.readlines()
for i in range(len(WORDS)):
    WORDS[i] = WORDS[i].strip().upper()


def main():
    """Run a single game of Hacking."""
    print('''HACKING MINIGAME
By Al Sweigart al@inventwithpython.com
''')

    gameWords = getWords()
    gameBoard = getBoard(gameWords)
    secretPassword = random.choice(gameWords)

    print('Find the password in the computer\'s memory:')
    print(gameBoard)
    for triesRemaining in range(4, 0, -1):
        playerMove = getPlayerMove(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('A C C E S S   G R A N T E D')
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print('Access Denied ({}/7 correct)'.format(numMatches))
    print('Out of tries. Secret password was {}.'.format(secretPassword))


def getBoard(words):
    """Return a string representing the "computer memory"."""

    # Pick which lines contain words:
    linesWithWords = random.sample(range(16 * 2), len(words))
    # The starting memory address (this is also cosmetic).
    memoryAddress = 16 * random.randint(0, 4000)

    #
    board = []
    nextWord = 0
    for i in range(16):
        leftLine = ''
        rightLine = ''
        for j in range(16):
            leftLine += random.choice(GARBAGE_CHARS)
            rightLine += random.choice(GARBAGE_CHARS)

        if i in linesWithWords:
            insertionIndex = random.randint(0, 9)
            leftLine = leftLine[:insertionIndex] + words[nextWord] + leftLine[insertionIndex + 7:]
            nextWord += 1
        if i + 16 in linesWithWords:
            insertionIndex = random.randint(0, 9)
            rightLine = rightLine[:insertionIndex] + words[nextWord] + rightLine[insertionIndex + 7:]
            nextWord += 1

        board.append('0x' + hex(memoryAddress)[2:].zfill(4) +
                     '  ' + leftLine + '    ' +
                     '0x' + hex(memoryAddress + (16*16))[2:].zfill(4) +
                     '  ' + rightLine)

        memoryAddress += 16

    # Each string in board is joined into one large string to return:
    return '\n'.join(board)


def getPlayerMove(words, tries):
    """Let the player enter a password guess."""
    while True:
        print('Enter password: ({} tries remaining)'.format(tries))
        move = input().upper()
        if move in words:
            return move
        print('That is not one of the possible passwords listed above.')


def numMatchingLetters(word1, word2):
    """Returns the number of matching letters between these two words."""
    matches = 0
    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1
    return matches


def getOneWordExcept(blocklist=None):
    """Returns a random word from WORDS that isn't in blocklist."""
    if blocklist == None:
        blocklist = []

    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def getWords():
    """Return the words that could possibly be the password.

    To make the game fair, we want to only have at most 2 words that
    have 0 letters in common with the secret password."""
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    # Find two words more that have zero matching letters.
    # "< 3" because the secret password is already in words.
    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    # Find two words that have 3 matching letters (but give up at 500
    # tries if not enough can be found).
    for i in range(500):
        if len(words) == 5:
            break

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    # Find seven words that have at least one matching letter (but give
    # up at 500 tries if not enough can be found).
    for i in range(500):
        if len(words) == 12:
            break

        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    # Add any random words needed to get 12 words total.
    words.extend(random.sample(WORDS, 12 - len(words)))

    assert len(words) == 12
    return words


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # When Ctrl-C is pressed, end the program.
