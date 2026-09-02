from card import Card

class Hand:
    def __init__(self):
        self.cards = []
        self.split_aces = False
        self.from_split = False

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        total = 0
        aces = 0
        for card in self.cards:
            value = card.value()
            if isinstance(value, tuple):  # asso
                total += 11
                aces += 1
            else:
                total += value
        while total > 21 and aces > 0:  # aggiusta il valore degli assi se si sballa
            total -= 10
            aces -= 1
        return total

    def is_bust(self):
        return self.get_value() > 21

    def is_blackjack(self):  # blackjack naturale: due carte con totale 21
        return len(self.cards) == 2 and self.get_value() == 21

    def has_ace(self):
        return any(card.rank == 'A' for card in self.cards)
    
"""test singolo
Esempio 1: Mano semplice senza Assi
mano = Hand()
mano.add_card(Card('Hearts', '10'))
mano.add_card(Card('Spades', 'K'))

print(mano.get_value())  # 20 (10 + 10)
print(mano.is_bust())    # False
print(mano.is_blackjack())  # False (non c'è Asso)

Esempio 2: Blackjack naturale
mano = Hand()
mano.add_card(Card('Hearts', 'A'))   # Asso
mano.add_card(Card('Spades', 'K'))   # 10

print(mano.get_value())  # 21 (11 + 10)
print(mano.is_blackjack())  # True 

Esempio 3: Asso che si aggiusta (soft hand)
pythonmano = Hand()
mano.add_card(Card('Hearts', 'A'))   # 11 (inizialmente)
mano.add_card(Card('Spades', '6'))   # +6 = 17

print(mano.get_value())  # 17 (11 + 6, soft 17)

# Pesca un'altra carta
mano.add_card(Card('Diamonds', '9'))  # +9 = 26 (bust?)

# NO! L'Asso si aggiusta:
# 11 + 6 + 9 = 26 > 21 → Asso diventa 1
# 1 + 6 + 9 = 16 

print(mano.get_value())  # 16 (non 26!)
print(mano.is_bust())    # False 

Esempio 4: Due Assi
pythonmano = Hand()
mano.add_card(Card('Hearts', 'A'))   # 11
mano.add_card(Card('Spades', 'A'))   # +11 = 22 > 21

# Primo Asso si aggiusta: 11 → 1
# Totale: 1 + 11 = 12

print(mano.get_value())  # 12 (non 22)

mano.add_card(Card('Clubs', '9'))    # +9 = 21

print(mano.get_value())  # 21 

Esempio 5: Bust vero (non salvabile)
pythonmano = Hand()
mano.add_card(Card('Hearts', 'K'))   # 10
mano.add_card(Card('Spades', 'Q'))   # +10 = 20
mano.add_card(Card('Clubs', '5'))    # +5 = 25

print(mano.get_value())  # 25
print(mano.is_bust())    # True (nessun Asso da aggiustare)
"""
