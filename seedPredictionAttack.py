# SEED PREDICTION ATTACK
# Dimostrazione empirica del determinismo del PRNG (Mersenne Twister).
# L'attaccante osserva una sessione con seed noto e replica
# esattamente la sequenza di carte nella sessione successiva.

from montecarlo import MonteCarloSimulator
from cardCountingStrategy import CardCountingStrategy
from deck import Deck
from rng import PRNG, CSPRNG
import random

print("=" * 60)
print("SEED PREDICTION ATTACK — DIMOSTRAZIONE")
print("=" * 60)

SEED = 42


# FASE 1: ATTACCANTE OSSERVA LA PRIMA SESSIONE
# conosce il seed (es. derivato da timestamp prevedibile)

print("\n[FASE 1] Sessione vittima — seed noto all'attaccante")
random.seed(SEED)
deck_vittima = Deck(num_decks=6, rng=PRNG)
sequenza_vittima = [str(deck_vittima.draw()) for _ in range(20)]
print("Prime 20 carte distribuite:")
print(sequenza_vittima)


# FASE 2: ATTACCANTE REPLICA LA SEQUENZA
# resetta lo stesso seed e ottiene le stesse carte in anticipo

print("\n[FASE 2] Attaccante replica la sequenza con seed identico")
random.seed(SEED)
deck_attaccante = Deck(num_decks=6, rng=PRNG)
sequenza_attaccante = [str(deck_attaccante.draw()) for _ in range(20)]
print("Sequenza prevista dall'attaccante:")
print(sequenza_attaccante)


# VERIFICA

identiche = sequenza_vittima == sequenza_attaccante
print(f"\nSequenze identiche: {identiche}")
print(f"Carte indovinate: {sum(a == b for a, b in zip(sequenza_vittima, sequenza_attaccante))}/20")


# FASE 3: IMPATTO ECONOMICO
# con la prescienza delle carte il contatore non deve stimare il TC:
# lo conosce con certezza assoluta — due sessioni identiche lo dimostrano

print("\n[FASE 3] Impatto economico — due sessioni con seed identico")

random.seed(SEED)
sim1 = MonteCarloSimulator(num_decks=6, strategy=CardCountingStrategy(), rng=PRNG)
r1 = sim1.run(num_hands=10000)

random.seed(SEED)
sim2 = MonteCarloSimulator(num_decks=6, strategy=CardCountingStrategy(), rng=PRNG)
r2 = sim2.run(num_hands=10000)

print(f"\n{'Metrica':<25} | {'Sessione 1':>12} | {'Sessione 2':>12} | {'Identiche':>10}")
print("-" * 65)
print(f"{'Win rate':<25} | {r1['win_rate']:>12.6f} | {r2['win_rate']:>12.6f} | {str(r1['win_rate'] == r2['win_rate']):>10}")
print(f"{'House edge':<25} | {r1['house_edge']:>12.6f} | {r2['house_edge']:>12.6f} | {str(r1['house_edge'] == r2['house_edge']):>10}")
print(f"{'Total payoff':<25} | {r1['total_payoff']:>12.0f} | {r2['total_payoff']:>12.0f} | {str(r1['total_payoff'] == r2['total_payoff']):>10}")
print(f"{'Total bet':<25} | {r1['total_bet']:>12.0f} | {r2['total_bet']:>12.0f} | {str(r1['total_bet'] == r2['total_bet']):>10}")
print(f"\nDeterminismo totale: {r1['win_rate'] == r2['win_rate'] and r1['house_edge'] == r2['house_edge']}")


# MITIGAZIONE: CSPRNG

print("\n" + "=" * 60)
print("MITIGAZIONE: CSPRNG")
print("=" * 60)
print("\nCon CSPRNG lo stesso 'seed' non produce la stessa sequenza.")
print("Lo stato interno attinge a /dev/urandom: non riproducibile.")

deck_csp1 = Deck(num_decks=1, rng=CSPRNG)
deck_csp2 = Deck(num_decks=1, rng=CSPRNG)
seq1 = [str(deck_csp1.draw()) for _ in range(5)]
seq2 = [str(deck_csp2.draw()) for _ in range(5)]

print(f"\nCSPRNG sessione 1: {seq1}")
print(f"CSPRNG sessione 2: {seq2}")
print(f"Sequenze identiche: {seq1 == seq2}")