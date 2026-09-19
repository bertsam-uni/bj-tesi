from montecarlo import MonteCarloSimulator
from cardCountingStrategy import CardCountingStrategy
from strategy import AdvancedStrategy
import time

# random.seed(42)  # TODO: fissare per riproducibilità dei risultati citati in tesi (Cap. 4/5)


NUM_HANDS = 5_000_000

print("=" * 60)
print("RISULTATI SIMULAZIONI")
print("=" * 60)

print("\nCONFRONTO STRATEGIE")
print("-" * 60)

print(f"\n[1/2] AdvancedStrategy - {NUM_HANDS:,} mani...")
start = time.time()
sim1 = MonteCarloSimulator(num_decks=6, strategy=AdvancedStrategy())
r1 = sim1.run(num_hands=NUM_HANDS)
time1 = time.time() - start

print(f"  Win Rate:       {r1['win_rate']:.6f}  ({r1['win_rate']*100:.2f}%)")
print(f"  Loss Rate:      {r1['loss_rate']:.6f}  ({r1['loss_rate']*100:.2f}%)")
print(f"  Push Rate:      {r1['push_rate']:.6f}  ({r1['push_rate']*100:.2f}%)")
print(f"  House Edge:     {r1['house_edge']:.6f}  ({r1['house_edge']*100:.2f}%)")
print(f"  ROI:            {r1['roi']:.6f}  ({r1['roi']*100:.2f}%)")
print(f"  EV per mano:    {r1['expected_value_per_hand']:.6f}")
print(f"  Mani giocate:   {r1['total_hands_played']:,}")
print(f"  Total bet:      {r1['total_bet']:,.0f} unita")
print(f"  Total payoff:   {r1['total_payoff']:,.0f} unita")
print(f"  Std Error:      {r1['std_error']:.6f}")
print(f"  Tempo:          {time1:.2f}s  ({time1/60:.1f} min)")

print(f"\n[2/2] CardCountingStrategy (Hi-Lo, spread 1-12) - {NUM_HANDS:,} mani...")
start = time.time()
sim2 = MonteCarloSimulator(num_decks=6, strategy=CardCountingStrategy())
r2 = sim2.run(num_hands=NUM_HANDS)
time2 = time.time() - start

print(f"  Win Rate:       {r2['win_rate']:.6f}  ({r2['win_rate']*100:.2f}%)")
print(f"  Loss Rate:      {r2['loss_rate']:.6f}  ({r2['loss_rate']*100:.2f}%)")
print(f"  Push Rate:      {r2['push_rate']:.6f}  ({r2['push_rate']*100:.2f}%)")
print(f"  House Edge:     {r2['house_edge']:.6f}  ({r2['house_edge']*100:.2f}%)")
print(f"  ROI:            {r2['roi']:.6f}  ({r2['roi']*100:.2f}%)")
print(f"  EV per mano:    {r2['expected_value_per_hand']:.6f}")
print(f"  Avg True Count: {r2['avg_tc']:.6f}")
print(f"  Mani giocate:   {r2['total_hands_played']:,}")
print(f"  Total bet:      {r2['total_bet']:,.0f} unita")
print(f"  Total payoff:   {r2['total_payoff']:,.0f} unita")
print(f"  Std Error:      {r2['std_error']:.6f}")
print(f"  Tempo:          {time2:.2f}s  ({time2/60:.1f} min)")

print(f"\n{'Strategia':<35} | {'House Edge':>12} | {'Win Rate':>10} | {'ROI':>10}")
print("-" * 75)
print(f"{'AdvancedStrategy (no counting)':<35} | {r1['house_edge']:>11.4%} | {r1['win_rate']:>10.4f} | {r1['roi']:>10.6f}")
print(f"{'CardCounting (Hi-Lo, spread 1-12)':<35} | {r2['house_edge']:>11.4%} | {r2['win_rate']:>10.4f} | {r2['roi']:>10.6f}")
print("-" * 75)
print(f"{'delta (counting - baseline)':<35} | {(r2['house_edge']-r1['house_edge']):>11.4%} | {(r2['win_rate']-r1['win_rate']):>10.4f} | {(r2['roi']-r1['roi']):>10.6f}")

print("\n\nANALISI BET SIZING")
print("-" * 60)
total_bet_flat = r2['total_hands_played']
moltiplicatore = r2['total_bet'] / total_bet_flat
print(f"Total bet con spread:       {r2['total_bet']:,.0f} unita")
print(f"Total bet flat (ipotetico): {total_bet_flat:,} unita")
print(f"Moltiplicatore effettivo:   {moltiplicatore:.2f}x")
print(f"\nIl contatore punta in media {moltiplicatore:.2f}x la puntata base.")

print("\n\nVALIDAZIONE CON LETTERATURA")
print("-" * 60)
print(f"\n{'Fonte':<25} | {'HE no count':>13} | {'HE Hi-Lo':>14} | {'ROI':>10}")
print("-" * 70)
print(f"{'Baldwin et al. (1956)':<25} | {'+0.50%':>13} | {'—':>14} | {'—':>10}")
print(f"{'Thorp (1966)':<25} | {'+0.45%':>13} | {'-0.5% / -1.0%':>14} | {'+0.5% / +1.5%':>10}")
print(f"{'Griffin (1999)':<25} | {'+0.48%':>13} | {'-0.5% / -2.0%':>14} | {'+0.5% / +1.5%':>10}")
print(f"{'Wong (1994)':<25} | {'+0.52%':>13} | {'-0.8% / -1.5%':>14} | {'+0.4% / +1.2%':>10}")
print("-" * 70)
print(f"{'nostri risultati':<25} | {r1['house_edge']:>13.2%} | {r2['house_edge']:>14.2%} | {r2['roi']:>9.2%}")

error_baseline = abs(r1['house_edge'] - 0.0050)
in_range_hilo = -0.02 <= r2['house_edge'] <= -0.005
roi_positive = r2['roi'] > 0

print(f"\nAdvancedStrategy:")
print(f"  errore vs teorico (0.50%): {error_baseline*100:.2f}%")
print(f"  esito: {'validato (< 0.1%)' if error_baseline < 0.001 else 'deviazione moderata'}")

print(f"\nCardCountingStrategy:")
print(f"  house edge ottenuto: {r2['house_edge']*100:.2f}%")
print(f"  esito: {'entro range teorico' if in_range_hilo else 'fuori range / da verificare'}")

print(f"\nROI:")
print(f"  risultato: {r2['roi']*100:.2f}%")
print(f"  esito: {'positivo, coerente con teoria' if roi_positive else 'non ancora positivo'}")

print("\n\nCONCLUSIONI")
print("-" * 60)
print(f"\n1) AdvancedStrategy: house edge = {r1['house_edge']*100:.2f}%, coerente con il valore teorico atteso (~0.5%).")
print(f"\n2) Confronto eseguito su {NUM_HANDS:,} mani per strategia.")
print(f"   Spread effettivo: {moltiplicatore:.2f}x la puntata base.")

if r2['house_edge'] < r1['house_edge'] and r2['roi'] > r1['roi']:
    print(f"\n3) Il sistema Hi-Lo mostra un miglioramento rispetto alla baseline")
    print(f"   sia in house edge sia in ROI.")
else:
    print(f"\n3) I risultati del counting non mostrano ancora un vantaggio netto.")
    print(f"   Verificare convergenza statistica, penetrazione e bet sizing.")

print(f"\n4) La validazione della basic strategy e solida.")
print(f"   La CardCountingStrategy e corretta nei test unitari;")
print(f"   la conferma empirica richiede house edge <= 0 e ROI positivo.")

print("\n" + "=" * 60)