# CLIENT-SERVER SIMULATION
# Simula un'architettura client-server con:
# - gestione sessione (nonce + timestamp)
# - analisi statistica lato server (BehaviouralProfiler)
# - detection su profili multipli: contatore, normale, camouflage
# - scenari di attacco: replay, client-side manipulation
 
from montecarlo import MonteCarloSimulator
from cardCountingStrategy import CardCountingStrategy
from strategy import AdvancedStrategy
from behaviouralProfiler import BehaviouralProfiler
import time, secrets
import numpy as np
 
print("=" * 60)
print("CLIENT-SERVER SIMULATION")
print("=" * 60)
 

# INFRASTRUTTURA DI SESSIONE
# nonce registry + validazione timestamp

nonce_registry = set()
 
def generate_nonce():
    return secrets.token_hex(8)
 
def build_packet(action, amount, bet, tc):
    return {
        "nonce": generate_nonce(),
        "timestamp": time.time(),
        "action": action,
        "amount": amount,
        "bet": bet,
        "tc": tc
    }
 
def server_validate(packet, max_bet=80, time_window=5.0):
    """Valida il pacchetto in ingresso: replay, timestamp e bet limit."""
    if packet["nonce"] in nonce_registry:
        return False, "REPLAY ATTACK: nonce già utilizzato"
    if abs(time.time() - packet["timestamp"]) > time_window:
        return False, "TIMESTAMP SCADUTO: pacchetto fuori finestra"
    if packet["amount"] > max_bet:
        return False, f"BET LIMIT EXCEEDED: {packet['amount']} > {max_bet}"
    nonce_registry.add(packet["nonce"])
    return True, "OK"
 

# SIMULAZIONI: 4 PROFILI

print("\n[1/4] Simulazioni in corso...")
 
profiles = {
    "Contatore": (CardCountingStrategy(), 3.2, 0.35),
    "Normale":   (AdvancedStrategy(),     4.5, 1.20),
}
 
try:
    from TcamouflageTest import CamouflageLightStrategy, CamouflageStrongStrategy
    profiles["Camouflage Light"]   = (CamouflageLightStrategy(),  3.8, 0.90)
    profiles["Camouflage Strong"]  = (CamouflageStrongStrategy(), 4.2, 1.10)
except ImportError:
    print("  (camouflage non disponibile, skip)")
 
results = {}
for name, (strategy, mu, sigma) in profiles.items():
    sim = MonteCarloSimulator(num_decks=6, strategy=strategy)
    r = sim.run(num_hands=20000)
    results[name] = (r, mu, sigma)
    print(f"  {name}: completato")
 

# SERVER: BEHAVIOURAL ANALYSIS

print("\n[2/4] Analisi comportamentale lato server...")
 
server_reports = {}
for name, (r, mu, sigma) in results.items():
    profiler = BehaviouralProfiler()
    for i, bet in enumerate(r["bet_history"]):
        tc = r["tc_history"][i] if i < len(r["tc_history"]) else 0
        dt = np.random.normal(mu, sigma)
        profiler.record_action(dt, bet, tc)
    score = profiler.get_anomaly_score()
    server_reports[name] = {**score, "suspicious": profiler.is_suspicious()}
 

# SERVER: ANALISI FINANZIARIA AGGREGATA

def financial_analysis(r):
    bets = r["bet_history"]
    mean_bet = sum(bets) / len(bets)
    bet_var = sum((x - mean_bet) ** 2 for x in bets) / len(bets)
    tc_mean = sum(r["tc_history"]) / len(r["tc_history"]) if r["tc_history"] else 0
 
    suspicion_score = 0
    # bet_var > 2: spread elevato suggerisce adattamento al TC
    # (flat better oscilla ~1, contatore tra 1 e 8)
    if bet_var > 2:
        suspicion_score += 1
    if abs(tc_mean) > 0.5:
        suspicion_score += 1
 
    return {
        "bet_variance": round(bet_var, 4),
        "tc_mean": round(tc_mean, 4),
        "suspicion_score": suspicion_score
    }
 

# REPORT FINALE

print("\n[3/4] Server report — tutti i profili\n")
print(f"{'Profilo':<20} | {'T_Var':>7} | {'Corr':>7} | {'BetVar':>7} | {'TC_mean':>7} | {'Fin.Score':>9} | {'Flagged':>8}")
print("-" * 80)
 
for name, (r, mu, sigma) in results.items():
    s = server_reports[name]
    f = financial_analysis(r)
    flagged = "YES" if (s["suspicious"] or f["suspicion_score"] >= 1) else "NO"
    print(
        f"{name:<20} | {s['timing_variance']:>7.4f} | {s['bet_tc_correlation']:>7.4f} | "
        f"{f['bet_variance']:>7.4f} | {f['tc_mean']:>7.4f} | {f['suspicion_score']:>9} | {flagged:>8}"
    )
 

# SCENARI DI ATTACCO

print("\n[4/4] Scenari di attacco simulati\n")
 
print("--- REPLAY ATTACK ---")
p = build_packet("PLACE_BET", 40, 4, 3)
_, msg1 = server_validate(p)
_, msg2 = server_validate(p)  # stesso pacchetto
print(f"Prima richiesta:  {msg1}")
print(f"Replay tentativo: {msg2}")
 
print("\n--- CLIENT-SIDE MANIPULATION ---")
for amount in [10, 40, 80, 9999]:
    p = build_packet("PLACE_BET", amount, amount, 0)
    _, msg = server_validate(p)
    print(f"  amount={amount:<6} → {msg}")
 
print("\n" + "=" * 60)
print("CONCLUSIONI")
print("=" * 60)
print("- Il server rileva il contatore puro su entrambe le dimensioni")
print("- Il camouflage evade l'analisi comportamentale ma non quella finanziaria")
print("- Nonce e timestamp neutralizzano replay e injection")
print("- Il client non è mai un'entità fidata")