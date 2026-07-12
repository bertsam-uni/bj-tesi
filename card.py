from __future__ import annotations

class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit: str, rank: str):
        if suit not in self.SUITS:
            raise ValueError("Invalid suit")
        if rank not in self.RANKS:
            raise ValueError("Invalid rank")
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return (1, 11)
        return int(self.rank)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))
    

"""test singola classe
    
    asso_cuori = Card('Hearts', 'A')
    dieci_picche = Card('Spades', '10')
    re_quadri = Card('Diamonds', 'K')

    # Stampa le carte
    print(asso_cuori)    # A of Hearts
    print(dieci_picche)  # 10 of Spades
    print(re_quadri)     # K of Diamonds

    # Ottieni i valori
    print(asso_cuori.value())   # (1, 11)
    print(dieci_picche.value()) # 10
    print(re_quadri.value())    # 10

    # Prova carta non valida
    try:
        carta_falsa = Card('Banana', 'Z')
    except ValueError as e:
        print(f"Errore: {e}")  # Errore: Invalid suit
"""

#COUNTING
