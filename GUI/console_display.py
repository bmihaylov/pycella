from pycella.automaton.automaton import CA

def display(ca):
    i = 0
    for cell in ca:
        print(' ' if cell == 0 else '*', end='')
        i += 1
        if i == ca.width:
            i = 0
            print()
