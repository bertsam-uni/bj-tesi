from montecarlo import MonteCarloSimulator
from rng import PRNG
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import time
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

# random.seed(42)  #fissare per riproducibilità di tabella e grafico di convergenza SE


test_sizes = [1000, 10000, 100000, 500000, 1000000, 5000000]
results_table = []

for n in test_sizes:
    print(f"\nEsecuzione con n = {n:,} mani...")
    start = time.time()
    sim = MonteCarloSimulator(num_decks=6, rng=PRNG)
    results = sim.run(num_hands=n)
    elapsed = time.time() - start
    results_table.append({
        'n': n,
        'win_rate': results['win_rate'],
        'house_edge': results['house_edge'],
        'std_error': results['std_error'],
        'time': elapsed
    })
    print(f"  House edge: {results['house_edge']:.6f}")
    print(f"  Std error:  {results['std_error']:.6f}")
    print(f"  Tempo:      {elapsed:.2f}s")

print("\n" + "=" * 60)
print("TABELLA RIASSUNTIVA")
print("=" * 60)
print(f"{'n':>12} | {'Win Rate':>10} | {'House Edge':>12} | {'Std Error':>12} | {'Tempo (s)':>10}")
print("-" * 60)
for r in results_table:
    print(f"{r['n']:>12,} | {r['win_rate']:>10.4f} | {r['house_edge']:>12.6f} | {r['std_error']:>12.6f} | {r['time']:>10.2f}")

# verifica empirica SE ~ 1/sqrt(n), dati dinamici dalla simulazione
plot_data = [r for r in results_table if r['n'] <= 1000000]
n_values = [r['n'] for r in plot_data]
std_errors = [r['std_error'] for r in plot_data]

# stima k dalla prima osservazione
k = std_errors[0] * np.sqrt(n_values[0])
theoretical_se = [k / np.sqrt(n) for n in n_values]

plt.figure(figsize=(10, 6))
plt.loglog(n_values, std_errors, 'o-', label='SE empirico', markersize=8)
plt.loglog(n_values, theoretical_se, '--', label=f'SE teorico (k={k:.2f})', linewidth=2)
plt.xlabel('Numero di mani (n)', fontsize=12)
plt.ylabel('Standard Error (SE)', fontsize=12)
plt.title('Convergenza Standard Error: verifica legge 1/√n', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'convergenza_se.png'), dpi=300)
plt.show()
print("Grafico salvato: images/convergenza_se.png")

log_n = np.log(n_values)
log_se = np.log(std_errors)
correlation, _ = pearsonr(log_n, log_se)
r_squared = correlation ** 2
print(f"\nCoefficiente R² (fit log-log): {r_squared:.4f}")
print("(R² ≈ 1 conferma relazione SE ∝ 1/√n)")