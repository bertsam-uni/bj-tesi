import numpy as np

class BotDetector:
    """
    Rileva software automatizzati (bot) basandosi su
    anomalie nei tempi di risposta e assenza di varianza decisionale.
    Segnali: T_avg < 1s e T_var < 0.05 indicano comportamento meccanico.
    """
    def __init__(self):
        self.decision_times = []

    def record_action(self, decision_time):
        self.decision_times.append(decision_time)

    def get_score(self):
        if len(self.decision_times) < 10:
            return {"t_avg": None, "t_var": None}
        return {
            "t_avg": round(float(np.mean(self.decision_times)), 4),
            "t_var": round(float(np.var(self.decision_times)), 4)
        }

    def is_bot(self, avg_threshold=1.0, var_threshold=0.05):
        score = self.get_score()
        if score["t_avg"] is None:
            return False
        return (score["t_avg"] < avg_threshold and
                score["t_var"] < var_threshold)


if __name__ == "__main__":
    import random
    print("=" * 60)
    print("BOT DETECTION - TEST")
    print("=" * 60)

    bot = BotDetector()
    for _ in range(500):
        bot.record_action(random.gauss(0.1, 0.01))

    human = BotDetector()
    for _ in range(500):
        human.record_action(random.gauss(4.5, 1.2))

    print(f"\n{'Profilo':<10} | {'T_avg':>7} | {'T_var':>7} | {'Bot':>6}")
    print("-" * 40)
    for label, profiler in [("BOT", bot), ("UMANO", human)]:
        s = profiler.get_score()
        flag = profiler.is_bot()
        print(f"{label:<10} | {s['t_avg']:>7.4f} | {s['t_var']:>7.4f} | {str(flag):>6}")
    print()
    print("Soglie: T_avg < 1.0 s  e  T_var < 0.05")
    print("Profili sintetici: bot ~ N(0.1, 0.01), umano ~ N(4.5, 1.2)")