"""
Elenco completo dei Magic Methods di Python
Guida di riferimento per metodi speciali (dunder methods)
"""

# =============================================================================
# 1. INIZIALIZZAZIONE E COSTRUZIONE
# =============================================================================

class Esempio1:
    def __new__(cls, *args, **kwargs):
        """Crea una nuova istanza (chiamato prima di __init__)"""
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, valore):
        """Inizializza l'istanza dopo la creazione"""
        self.valore = valore
    
    def __del__(self):
        """Chiamato quando l'oggetto viene distrutto"""
        print(f"Oggetto {self.valore} eliminato")


# =============================================================================
# 2. RAPPRESENTAZIONE COME STRINGA
# =============================================================================

class Esempio2:
    def __init__(self, nome):
        self.nome = nome
    
    def __repr__(self):
        """Rappresentazione 'ufficiale' (per debug)"""
        return f"Esempio2(nome='{self.nome}')"
    
    def __str__(self):
        """Rappresentazione 'user-friendly'"""
        return f"Oggetto: {self.nome}"
    
    def __format__(self, spec):
        """Formattazione personalizzata"""
        if spec == 'upper':
            return self.nome.upper()
        return self.nome
    
    def __bytes__(self):
        """Conversione a bytes"""
        return self.nome.encode('utf-8')


# =============================================================================
# 3. OPERATORI MATEMATICI - Aritmetici
# =============================================================================

class Vettore:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """self + other"""
        return Vettore(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """self - other"""
        return Vettore(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """self * scalar"""
        return Vettore(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """self / scalar"""
        return Vettore(self.x / scalar, self.y / scalar)
    
    def __floordiv__(self, scalar):
        """self // scalar"""
        return Vettore(self.x // scalar, self.y // scalar)
    
    def __mod__(self, other):
        """self % other"""
        return Vettore(self.x % other, self.y % other)
    
    def __pow__(self, power):
        """self ** power"""
        return Vettore(self.x ** power, self.y ** power)
    
    def __divmod__(self, other):
        """divmod(self, other)"""
        return (self // other, self % other)
    
    # Versioni "riflesse" (quando operatore è a destra)
    def __radd__(self, other):
        """other + self"""
        return self.__add__(other)
    
    def __rsub__(self, other):
        """other - self"""
        return Vettore(other - self.x, other - self.y)
    
    # Versioni "in-place" (con assegnamento)
    def __iadd__(self, other):
        """self += other"""
        self.x += other.x
        self.y += other.y
        return self
    
    def __isub__(self, other):
        """self -= other"""
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __repr__(self):
        return f"Vettore({self.x}, {self.y})"


# =============================================================================
# 4. OPERATORI UNARI
# =============================================================================

class Numero:
    def __init__(self, valore):
        self.valore = valore
    
    def __neg__(self):
        """- self"""
        return Numero(-self.valore)
    
    def __pos__(self):
        """+ self"""
        return Numero(+self.valore)
    
    def __abs__(self):
        """abs(self)"""
        return Numero(abs(self.valore))
    
    def __invert__(self):
        """~ self (bitwise NOT)"""
        return Numero(~self.valore)
    
    def __repr__(self):
        return f"Numero({self.valore})"


# =============================================================================
# 5. OPERATORI DI CONFRONTO
# =============================================================================

class Studente:
    def __init__(self, nome, voto):
        self.nome = nome
        self.voto = voto
    
    def __eq__(self, other):
        """self == other"""
        return self.voto == other.voto
    
    def __ne__(self, other):
        """self != other"""
        return self.voto != other.voto
    
    def __lt__(self, other):
        """self < other"""
        return self.voto < other.voto
    
    def __le__(self, other):
        """self <= other"""
        return self.voto <= other.voto
    
    def __gt__(self, other):
        """self > other"""
        return self.voto > other.voto
    
    def __ge__(self, other):
        """self >= other"""
        return self.voto >= other.voto
    
    def __repr__(self):
        return f"Studente('{self.nome}', {self.voto})"


# =============================================================================
# 6. ACCESSO AGLI ATTRIBUTI
# =============================================================================

class AttributiDinamici:
    def __init__(self):
        self._data = {}
    
    def __getattr__(self, name):
        """Chiamato quando attributo non trovato"""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{name}' non trovato")
    
    def __setattr__(self, name, value):
        """obj.attr = value"""
        if name == '_data':
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __delattr__(self, name):
        """del obj.attr"""
        if name in self._data:
            del self._data[name]
    
    def __getattribute__(self, name):
        """Chiamato per OGNI accesso attributo"""
        # Attenzione: può causare ricorsione infinita
        return super().__getattribute__(name)
    
    def __dir__(self):
        """dir(obj)"""
        return list(self._data.keys())


# =============================================================================
# 7. CONTAINER (Liste, Dict, etc.)
# =============================================================================

class MiaLista:
    def __init__(self, items=None):
        self.items = items if items else []
    
    def __len__(self):
        """len(obj)"""
        return len(self.items)
    
    def __getitem__(self, index):
        """obj[index]"""
        return self.items[index]
    
    def __setitem__(self, index, value):
        """obj[index] = value"""
        self.items[index] = value
    
    def __delitem__(self, index):
        """del obj[index]"""
        del self.items[index]
    
    def __contains__(self, item):
        """item in obj"""
        return item in self.items
    
    def __iter__(self):
        """for x in obj"""
        return iter(self.items)
    
    def __reversed__(self):
        """reversed(obj)"""
        return reversed(self.items)
    
    def __repr__(self):
        return f"MiaLista({self.items})"


class Iteratore:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        """Rende l'oggetto iterabile"""
        return self
    
    def __next__(self):
        """next(iter) - restituisce prossimo elemento"""
        if self.current >= self.end:
            raise StopIteration
        val = self.current
        self.current += 1
        return val


# =============================================================================
# 8. CALLABLE (Oggetti chiamabili come funzioni)
# =============================================================================

class Moltiplicatore:
    def __init__(self, fattore):
        self.fattore = fattore
    
    def __call__(self, x):
        """obj(x) - rende l'oggetto chiamabile"""
        return x * self.fattore


# =============================================================================
# 9. CONTEXT MANAGER (with statement)
# =============================================================================

class GestoreFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Inizio blocco with"""
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fine blocco with"""
        if self.file:
            self.file.close()
        # Ritorna False per propagare eccezioni
        return False


# =============================================================================
# 10. OPERATORI BITWISE
# =============================================================================

class BitSet:
    def __init__(self, value):
        self.value = value
    
    def __and__(self, other):
        """self & other"""
        return BitSet(self.value & other.value)
    
    def __or__(self, other):
        """self | other"""
        return BitSet(self.value | other.value)
    
    def __xor__(self, other):
        """self ^ other"""
        return BitSet(self.value ^ other.value)
    
    def __lshift__(self, n):
        """self << n"""
        return BitSet(self.value << n)
    
    def __rshift__(self, n):
        """self >> n"""
        return BitSet(self.value >> n)
    
    def __repr__(self):
        return f"BitSet({self.value})"


# =============================================================================
# 11. CONVERSIONI DI TIPO
# =============================================================================

class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __int__(self):
        """int(obj)"""
        return int(self.celsius)
    
    def __float__(self):
        """float(obj)"""
        return float(self.celsius)
    
    def __complex__(self):
        """complex(obj)"""
        return complex(self.celsius)
    
    def __bool__(self):
        """bool(obj)"""
        return self.celsius > 0
    
    def __hash__(self):
        """hash(obj) - per usare in dict/set"""
        return hash(self.celsius)
    
    def __index__(self):
        """Conversione a indice intero"""
        return int(self.celsius)
    
    def __repr__(self):
        return f"Temperatura({self.celsius}°C)"


# =============================================================================
# 12. DESCRIPTOR PROTOCOL
# =============================================================================

class Descrittore:
    def __init__(self, nome):
        self.nome = nome
    
    def __get__(self, obj, objtype=None):
        """Lettura descriptor"""
        if obj is None:
            return self
        return obj.__dict__.get(self.nome)
    
    def __set__(self, obj, value):
        """Scrittura descriptor"""
        obj.__dict__[self.nome] = value
    
    def __delete__(self, obj):
        """Cancellazione descriptor"""
        del obj.__dict__[self.nome]


# =============================================================================
# 13. COPYING
# =============================================================================

import copy

class Copiabile:
    def __init__(self, data):
        self.data = data
    
    def __copy__(self):
        """copy.copy(obj) - copia superficiale"""
        return Copiabile(self.data)
    
    def __deepcopy__(self, memo):
        """copy.deepcopy(obj) - copia profonda"""
        return Copiabile(copy.deepcopy(self.data, memo))


# =============================================================================
# 14. PICKLE (Serializzazione)
# =============================================================================

class Serializzabile:
    def __init__(self, valore):
        self.valore = valore
    
    def __getstate__(self):
        """Stato da serializzare"""
        return {'valore': self.valore}
    
    def __setstate__(self, state):
        """Ripristino stato"""
        self.valore = state['valore']
    
    def __reduce__(self):
        """Riduzione per pickle"""
        return (self.__class__, (self.valore,))
    
    def __reduce_ex__(self, protocol):
        """Versione estesa"""
        return self.__reduce__()


# =============================================================================
# ESEMPI D'USO PER IL BLACKJACK
# =============================================================================

print("=" * 70)
print("ESEMPI PRATICI PER IL PROGETTO BLACKJACK")
print("=" * 70)

# Esempio 1: Card con __repr__
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

card = Card('Hearts', 'A')
print(f"Card: {card}")  # A of Hearts

# Esempio 2: Deck con __len__ e __getitem__
class Deck:
    def __init__(self):
        self.cards = [Card('Hearts', 'A'), Card('Spades', 'K')]
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]
    
    def __iter__(self):
        return iter(self.cards)

deck = Deck()
print(f"Carte nel mazzo: {len(deck)}")
print(f"Prima carta: {deck[0]}")

# Esempio 3: Hand con __add__ per sommare valori
class Hand:
    def __init__(self):
        self.cards = []
    
    def __len__(self):
        return len(self.cards)
    
    def __repr__(self):
        return f"Hand({', '.join(str(c) for c in self.cards)})"

# Esempio 4: Callable per strategia
class BasicStrategy:
    def __call__(self, player_hand, dealer_card):
        """Rende la strategia chiamabile"""
        # Logica strategia
        return 'hit' if player_hand < 17 else 'stand'

strategy = BasicStrategy()
action = strategy(16, 'K')
print(f"Azione consigliata: {action}")

print("=" * 70)