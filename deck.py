from card import Card
from rng import PRNG, CSPRNG

class Deck:
    def __init__(self, num_decks=1, rng=PRNG):  # num_decks: 1 per test, 6 per simulazione realistica
        self.num_decks = num_decks
        self.rng = rng
        self.cards = self._initialize_deck()
        self.shuffle()

    def _initialize_deck(self):
        deck = []
        for _ in range(self.num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    deck.append(Card(suit, rank))
        return deck

    def shuffle(self):
        self.rng.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise ValueError("Deck exhausted")
        return self.cards.pop()

    def cards_remaining(self):
        return len(self.cards)
    
"""test singola classe, prima di AGGIUNTA 'counting'
mazzo = Deck()
print(len(mazzo.cards))  # 52

carta1 = mazzo.draw()
print(carta1)            # Es: "K of Spades"
print(len(mazzo.cards))  # 51 (una carta in meno)

carta2 = mazzo.draw()
print(len(mazzo.cards))  # 50
"""
