import random   # numeri pseudo-casuali
import secrets  # numeri crittograficamente sicuri

class PRNG:
    """Mersenne Twister — veloce, deterministico, prevedibile se si conosce il seed."""
    @staticmethod
    def shuffle(cards):
        random.shuffle(cards)

class CSPRNG:
    """Crittograficamente sicuro — Fisher-Yates con secrets.randbelow."""
    @staticmethod
    def shuffle(cards):
        n = len(cards)
        for i in range(n - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            cards[i], cards[j] = cards[j], cards[i]



"""test singolo
# Crea un mazzo di test
mazzo = ['A♥', 'K♠', 'Q♦', 'J♣', '10♥']

print("Mazzo originale:", mazzo)

# Copia per testare PRNG
mazzo_prng = mazzo.copy()
PRNG.shuffle(mazzo_prng)
print("Dopo PRNG:", mazzo_prng)

# Copia per testare CSPRNG
mazzo_csprng = mazzo.copy()
CSPRNG.shuffle(mazzo_csprng)
print("Dopo CSPRNG:", mazzo_csprng)

# Output esempio:
# Mazzo originale: ['A♥', 'K♠', 'Q♦', 'J♣', '10♥']
# Dopo PRNG: ['Q♦', '10♥', 'A♥', 'J♣', 'K♠']
# Dopo CSPRNG: ['K♠', 'A♥', 'J♣', '10♥', 'Q♦']
"""