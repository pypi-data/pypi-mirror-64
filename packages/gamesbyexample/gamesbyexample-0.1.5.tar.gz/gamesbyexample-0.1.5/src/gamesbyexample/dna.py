"""DNA, by Al Sweigart al@inventwithpython.com

A simple animation of a DNA double-helix. Press Ctrl-C to stop.
Inspired by matoken https://asciinema.org/a/155441
Tags: short, artistic, scrolling, science"""
__version__ = 0

import random, sys, time

# Set up the constants:
# These are the individual rows of the DNA animation:
ROWS = [
    '         ##',  # Index 0 has no {}.
    '        #{}-{}#',
    '       #{}---{}#',
    '      #{}-----{}#',
    '     #{}------{}#',
    '    #{}------{}#',
    '    #{}-----{}#',
    '     #{}---{}#',
    '     #{}-{}#',
    '      ##',  # Index 9 has no {}.
    '     #{}-{}#',
    '     #{}---{}#',
    '    #{}-----{}#',
    '    #{}------{}#',
    '     #{}------{}#',
    '      #{}-----{}#',
    '       #{}---{}#',
    '        #{}-{}#']


def main():
    """Run the DNA animation."""
    print('Press Ctrl-C to quit...')
    time.sleep(2)
    rowIndex = 0

    while True:  # Main program loop.
        # Increment rowIndex to draw next row:
        rowIndex += 1
        if rowIndex == len(ROWS):
            rowIndex = 0

        # Row indexs 0 and 9 don't have nucleotides:
        if rowIndex == 0 or rowIndex == 9:
            print(ROWS[rowIndex])
            continue

        # Select random nucleotide pairs:
        randomSelection = random.randint(1, 4)
        if randomSelection == 1:
            leftNucleotide, rightNucleotide = 'A', 'T'
        elif randomSelection == 2:
            leftNucleotide, rightNucleotide = 'T', 'A'
        elif randomSelection == 3:
            leftNucleotide, rightNucleotide = 'C', 'G'
        elif randomSelection == 4:
            leftNucleotide, rightNucleotide = 'G', 'C'

        # Print the row.
        print(ROWS[rowIndex].format(leftNucleotide, rightNucleotide))
        time.sleep(0.15)  # Add a slight pause.
        # At this point, go back to the start of the main program loop.


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # When Ctrl-C is pressed, end the program.
