"""
variance_check.py
Esegue N run indipendenti di AdvancedStrategy vs CardCountingStrategy
per verificare la stabilita del segno dell'house edge e del ROI
riportati nel Capitolo 4. Ogni run usa istanze fresche delle strategie.
"""

from montecarlo import MonteCarloSimulator
from cardCountingStrategy import CardCountingStrategy
from strategy import AdvancedStrategy
import statistics
import time

NUM_RUNS = 10
HANDS_PER_RUN = 1_000_000   # ridotto rispetto a 5M per contenere i tempi;
                             # aumentare se serve maggiore precisione per run

results_adv = {'house_edge': [], 'roi': [], 'win_rate': []}
results_cc  = {'house_edge': [], 'roi': [], 'win_rate': [], 'avg_tc': []}

print("=" * 70)
print(f"VERIFICA VARIANZA TRA RUN - {NUM_RUNS} run x {HANDS_PER_RUN:,} mani")
print("=" * 70)

for i in range(1, NUM_RUNS + 1):
    t0 = time.time()

    sim_adv = MonteCarloSimulator(num_decks=6, strategy=AdvancedStrategy())
    r_adv = sim_adv.run(num_hands=HANDS_PER_RUN)

    sim_cc = MonteCarloSimulator(num_decks=6, strategy=CardCountingStrategy())
    r_cc = sim_cc.run(num_hands=HANDS_PER_RUN)

    results_adv['house_edge'].append(r_adv['house_edge'])
    results_adv['roi'].append(r_adv['roi'])
    results_adv['win_rate'].append(r_adv['win_rate'])

    results_cc['house_edge'].append(r_cc['house_edge'])
    results_cc['roi'].append(r_cc['roi'])
    results_cc['win_rate'].append(r_cc['win_rate'])
    results_cc['avg_tc'].append(r_cc['avg_tc'])

    dt = time.time() - t0
    print(f"\nRun {i}/{NUM_RUNS}  ({dt:.1f}s)")
    print(f"  AdvancedStrategy   : HE = {r_adv['house_edge']*100:+.4f}%  | ROI = {r_adv['roi']*100:+.4f}%")
    print(f"  CardCounting       : HE = {r_cc['house_edge']*100:+.4f}%  | ROI = {r_cc['roi']*100:+.4f}%  | avg TC = {r_cc['avg_tc']:+.4f}")

def summarize(name, data, key, as_pct=True):
    vals = data[key]
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
    mult = 100 if as_pct else 1
    print(f"  {name:<20} media = {mean*mult:+.4f}  |  std = {stdev*mult:.4f}  |  min = {min(vals)*mult:+.4f}  |  max = {max(vals)*mult:+.4f}")

print("\n" + "=" * 70)
print("RIEPILOGO AGGREGATO")
print("=" * 70)

print("\nAdvancedStrategy:")
summarize("House Edge (%)", results_adv, 'house_edge')
summarize("ROI (%)", results_adv, 'roi')

print("\nCardCountingStrategy:")
summarize("House Edge (%)", results_cc, 'house_edge')
summarize("ROI (%)", results_cc, 'roi')
summarize("Avg True Count", results_cc, 'avg_tc', as_pct=False)

# Quante run su NUM_RUNS mostrano il vantaggio "atteso" (HE negativo, ROI positivo)?
n_he_negative = sum(1 for x in results_cc['house_edge'] if x < 0)
n_roi_positive = sum(1 for x in results_cc['roi'] if x > 0)
n_cc_beats_adv = sum(1 for a, c in zip(results_adv['house_edge'], results_cc['house_edge']) if c < a)

print(f"\nRun con House Edge CardCounting < 0 (vantaggio giocatore): {n_he_negative}/{NUM_RUNS}")
print(f"Run con ROI CardCounting > 0 (profitto netto):              {n_roi_positive}/{NUM_RUNS}")
print(f"Run in cui CardCounting batte AdvancedStrategy (HE minore): {n_cc_beats_adv}/{NUM_RUNS}")

print("\n" + "=" * 70)