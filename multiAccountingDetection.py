import numpy as np

class MultiAccountingDetector:
    """
    Rileva lo stesso utente su account diversi confrontando
    il vettore comportamentale [T_avg, T_var, B_avg] tra sessioni.
    Il vettore è normalizzato per evitare che componenti su scale
    diverse dominino la distanza euclidea.
    Distanza euclidea bassa = profili compatibili = sospetto.
    """
    def __init__(self):
        self.sessions = {}

    def record_session(self, account_id, decision_times, bet_history):
        self.sessions[account_id] = {
            "t_avg": float(np.mean(decision_times)),
            "t_var": float(np.var(decision_times)),
            "b_avg": float(np.mean(bet_history))
        }

    def _vector(self, account_id):
        s = self.sessions[account_id]
        return np.array([s["t_avg"], s["t_var"], s["b_avg"]])

    def _normalized_vector(self, account_id):
        # normalizzazione per scala: T_avg in [0,10], T_var in [0,5], B_avg in [0,100]
        v = self._vector(account_id)
        scale = np.array([10.0, 5.0, 100.0])
        return v / scale

    def compare(self, id_a, id_b):
        if id_a not in self.sessions or id_b not in self.sessions:
            return None
        return round(float(np.linalg.norm(
            self._normalized_vector(id_a) - self._normalized_vector(id_b))), 4)

    def is_suspicious(self, id_a, id_b, threshold=0.15):
        dist = self.compare(id_a, id_b)
        if dist is None:
            return False
        return dist < threshold

if __name__ == "__main__":
    import random
    print("=" * 60)
    print("MULTI-ACCOUNTING DETECTION - TEST")
    print("=" * 60)

    detector = MultiAccountingDetector()

    for acc in ["account_A", "account_A2"]:
        dt = [random.gauss(3.2, 0.35) for _ in range(500)]
        bh = [random.choice([10, 20, 40, 80]) for _ in range(500)]
        detector.record_session(acc, dt, bh)

    dt = [random.gauss(5.0, 1.5) for _ in range(500)]
    bh = [10] * 500
    detector.record_session("account_B", dt, bh)

    pairs = [
        ("account_A", "account_A2", "stesso utente"),
        ("account_A", "account_B",  "utenti diversi")
    ]

    print(f"\n{'Coppia':<22} | {'Distanza':>9} | {'Sospetto':>9}")
    print("-" * 47)
    for id1, id2, label in pairs:
        dist = detector.compare(id1, id2)
        flag = detector.is_suspicious(id1, id2)
        print(f"{label:<22} | {dist:>9.4f} | {str(flag):>9}")
    print()
    print("Soglia: distanza euclidea normalizzata < 0.15  →  stesso utente segnalato")
    print("Vettore comportamentale normalizzato: [T_avg/10, T_var/5, B_avg/100]")