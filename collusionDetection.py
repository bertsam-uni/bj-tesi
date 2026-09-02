import numpy as np
from scipy.stats import pearsonr

class CollusionDetector:
    """
    Rileva chip dumping: correlazione tra le puntate di due
    giocatori allo stesso tavolo. Correlazione negativa forte
    indica che uno perde deliberatamente per favorire l'altro.
    """
    def __init__(self):
        self.players = {}  # player_id -> bet_history

    def record_bet(self, player_id, bet):
        if player_id not in self.players:
            self.players[player_id] = []
        self.players[player_id].append(bet)

    def get_correlation(self, id_a, id_b):
        a = self.players.get(id_a, [])
        b = self.players.get(id_b, [])
        n = min(len(a), len(b))
        if n < 10:
            return None
        if np.std(a[:n]) == 0 or np.std(b[:n]) == 0:
            return 0.0
        corr, _ = pearsonr(a[:n], b[:n])
        return round(float(corr), 4)

    def is_suspicious(self, id_a, id_b, threshold=-0.7):
        corr = self.get_correlation(id_a, id_b)
        if corr is None:
            return False
        return corr < threshold


if __name__ == "__main__":
    import random
    print("=" * 60)
    print("COLLUSION DETECTION - TEST")
    print("=" * 60)

    detector = CollusionDetector()
    base = [random.choice([10, 20, 40, 80]) for _ in range(500)]
    for i, bet in enumerate(base):
        detector.record_bet("player_A", bet)
        detector.record_bet("player_B_collude", 90 - bet + random.gauss(0, 5))
        detector.record_bet("player_C_normal", random.choice([10, 20, 40]))

    pairs = [
        ("player_A", "player_B_collude", "collusione"),
        ("player_A", "player_C_normal",  "gioco normale")
    ]

    print(f"\n{'Coppia':<20} | {'Pearson r':>10} | {'Sospetto':>9}")
    print("-" * 45)
    for id1, id2, label in pairs:
        corr = detector.get_correlation(id1, id2)
        flag = detector.is_suspicious(id1, id2)
        print(f"{label:<20} | {corr:>10.4f} | {str(flag):>9}")
    print()
    print("Soglia: r < -0.7  →  chip dumping segnalato")
    print("player_B inverte sistematicamente le puntate di player_A")