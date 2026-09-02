from montecarlo import MonteCarloSimulator
from cardCountingStrategy import CardCountingStrategy
from strategy import AdvancedStrategy
from scipy.stats import pearsonr
import numpy as np
import random
import matplotlib.pyplot as plt
from behaviouralProfiler import BehaviouralProfiler


# CAMOUFLAGE STRATEGIES (solo estensione necessaria)


class CamouflageLightStrategy(CardCountingStrategy):
    def get_bet_size(self, base_bet=1):
        real = super().get_bet_size(base_bet)
        r = random.random()

        if r < 0.25:
            return base_bet
        if r < 0.45:
            return max(base_bet, real / 2)
        return real


class CamouflageStrongStrategy(CardCountingStrategy):
    def get_bet_size(self, base_bet=1):
        real = super().get_bet_size(base_bet)
        r = random.random()

        if r < 0.50:
            return base_bet
        if r < 0.80:
            return min(real, base_bet * 2)
        return min(real, base_bet * 4)


# SIMULAZIONI

if __name__ == "__main__":

    print("Esecuzione simulazioni Monte Carlo... attendere.\n")

    sim_counter = MonteCarloSimulator(num_decks=6, strategy=CardCountingStrategy())
    r_counter = sim_counter.run(num_hands=500000)

    sim_normal = MonteCarloSimulator(num_decks=6, strategy=AdvancedStrategy())
    r_normal = sim_normal.run(num_hands=500000)

    sim_light = MonteCarloSimulator(num_decks=6, strategy=CamouflageLightStrategy())
    r_light = sim_light.run(num_hands=500000)

    sim_strong = MonteCarloSimulator(num_decks=6, strategy=CamouflageStrongStrategy())
    r_strong = sim_strong.run(num_hands=500000)



    # PROFILING (riuso classe)


    def build_profiler(results, mu, sigma):
        profiler = BehaviouralProfiler()

        tc_hist = results["tc_history"]
        bet_hist = results["bet_history"]

        for i in range(len(bet_hist)):
            decision_time = np.random.normal(mu, sigma)
            tc = tc_hist[i] if i < len(tc_hist) else 0
            profiler.record_action(decision_time, bet_hist[i], tc)

        return profiler


    counter_profiler = build_profiler(r_counter, 3.2, 0.35)
    normal_profiler = build_profiler(r_normal, 4.5, 1.2)
    light_profiler = build_profiler(r_light, 3.8, 0.9)
    strong_profiler = build_profiler(r_strong, 4.2, 1.1)


    c_score = counter_profiler.get_anomaly_score()
    n_score = normal_profiler.get_anomaly_score()
    l_score = light_profiler.get_anomaly_score()
    s_score = strong_profiler.get_anomaly_score()



    # OUTPUT

    print("\n=== RISULTATI ===\n")

    print("COUNTER | T:", c_score["timing_variance"],
        "| Corr:", c_score["bet_tc_correlation"],
        "| Susp:", counter_profiler.is_suspicious())

    print("NORMAL  | T:", n_score["timing_variance"],
        "| Corr:", n_score["bet_tc_correlation"],
        "| Susp:", normal_profiler.is_suspicious())

    print("LIGHT   | T:", l_score["timing_variance"],
        "| Corr:", l_score["bet_tc_correlation"],
        "| Susp:", light_profiler.is_suspicious())

    print("STRONG  | T:", s_score["timing_variance"],
        "| Corr:", s_score["bet_tc_correlation"],
        "| Susp:", strong_profiler.is_suspicious())


    # GRAFICO CORRELAZIONE


    labels = ["Counter", "Light", "Strong"]

    corrs = [
        c_score["bet_tc_correlation"],
        l_score["bet_tc_correlation"],
        s_score["bet_tc_correlation"]
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, corrs)
    plt.title("Riduzione detection con camouflage")
    plt.ylabel("Pearson correlation")
    plt.show()