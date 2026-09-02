from scipy.stats import pearsonr
import numpy as np
 
 
class BehaviouralProfiler:
    def __init__(self):
        self.decision_times = []
        self.bet_history = []
        self.tc_history = []
 
    def record_action(self, decision_time, bet_size, true_count):
        self.decision_times.append(decision_time)
        self.bet_history.append(bet_size)
        self.tc_history.append(true_count)
 
    def get_anomaly_score(self):
        timing_variance = np.var(self.decision_times)
        bet_variance = np.var(self.bet_history)
 
        if len(self.tc_history) > 10 and np.std(self.bet_history) > 0 and np.std(self.tc_history) > 0:
            corr, _ = pearsonr(self.bet_history, self.tc_history)
        else:
            corr = 0.0
 
        return {
            "timing_variance": round(timing_variance, 4),
            "bet_variance": round(bet_variance, 4),
            "bet_tc_correlation": round(corr, 4)
        }
 
    def is_suspicious(self, variance_threshold=0.45, correlation_threshold=0.75):
        score = self.get_anomaly_score()
        return (
            score["timing_variance"] < variance_threshold or
            score["bet_tc_correlation"] > correlation_threshold
        )
 
 
if __name__ == "__main__":
    from montecarlo import MonteCarloSimulator
    from cardCountingStrategy import CardCountingStrategy
    from strategy import AdvancedStrategy
    import matplotlib
    matplotlib.use("Agg")  # salva su file, non apre finestra
    import matplotlib.pyplot as plt
    import random

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })

    from TcamouflageTest import CamouflageLightStrategy, CamouflageStrongStrategy

    # -- simulazioni 
    print("Simulazioni in corso...")
    N = 500000

    r_counter = MonteCarloSimulator(num_decks=6, strategy=CardCountingStrategy()).run(N)
    r_normal  = MonteCarloSimulator(num_decks=6, strategy=AdvancedStrategy()).run(N)
    r_light   = MonteCarloSimulator(num_decks=6, strategy=CamouflageLightStrategy()).run(N)
    r_strong  = MonteCarloSimulator(num_decks=6, strategy=CamouflageStrongStrategy()).run(N)

    # -- profiling 
    def build_profiler(results, mu, sigma):
        p = BehaviouralProfiler()
        tc_hist  = results["tc_history"]
        bet_hist = results["bet_history"]
        for i, bet in enumerate(bet_hist):
            tc = tc_hist[i] if i < len(tc_hist) else 0
            p.record_action(np.random.normal(mu, sigma), bet, tc)
        return p

    cp = build_profiler(r_counter, 3.2, 0.35)
    np_ = build_profiler(r_normal,  4.5, 1.2)
    lp = build_profiler(r_light,   3.8, 0.9)
    sp = build_profiler(r_strong,  4.2, 1.1)

    cs = cp.get_anomaly_score()
    ns = np_.get_anomaly_score()
    ls = lp.get_anomaly_score()
    ss = sp.get_anomaly_score()

    print(f"CONTATORE | T_Var: {cs['timing_variance']} | Corr: {cs['bet_tc_correlation']} | Susp: {cp.is_suspicious()}")
    print(f"NORMALE   | T_Var: {ns['timing_variance']} | Corr: {ns['bet_tc_correlation']} | Susp: {np_.is_suspicious()}")
    print(f"LIGHT     | T_Var: {ls['timing_variance']} | Corr: {ls['bet_tc_correlation']} | Susp: {lp.is_suspicious()}")
    print(f"STRONG    | T_Var: {ss['timing_variance']} | Corr: {ss['bet_tc_correlation']} | Susp: {sp.is_suspicious()}")

    # -- FIGURA 1: pearson.png 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    fig.subplots_adjust(wspace=0.35)

    bins = np.linspace(0, 9, 35)
    ax1.hist(np_.decision_times,  bins=bins, alpha=0.55, color="#2166ac",
             density=True, label="Giocatore normale", edgecolor="white")
    ax1.hist(cp.decision_times, bins=bins, alpha=0.75, color="#d6604d",
             density=True, label="Contatore", edgecolor="white")
    ax1.set_title("Distribuzione tempi di decisione")
    ax1.set_xlabel("Secondi")
    ax1.set_ylabel("Densità")
    ax1.legend(frameon=False)
    ax1.text(0.97, 0.95,
             f"Var normale = {ns['timing_variance']:.2f}\nVar contatore = {cs['timing_variance']:.2f}",
             transform=ax1.transAxes, ha="right", va="top", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#999", alpha=0.8))

    tc_arr  = np.array(r_counter["tc_history"])
    bet_arr = np.array(r_counter["bet_history"])
    ax2.scatter(tc_arr, bet_arr, s=8, alpha=0.25, color="#d6604d",
                label="Contatore", rasterized=True)
    m, b = np.polyfit(tc_arr, bet_arr, 1)
    xs = np.linspace(tc_arr.min(), tc_arr.max(), 100)
    ax2.plot(xs, m*xs + b, color="#d6604d", linewidth=1.6, linestyle="--",
             label=f"Tendenza (r = {cs['bet_tc_correlation']})")
    ax2.set_title("Correlazione puntata / True Count")
    ax2.set_xlabel("True Count")
    ax2.set_ylabel("Dimensione puntata (unità)")
    ax2.legend(frameon=False, fontsize=9)

    fig.savefig("images/pearson.png", dpi=300, bbox_inches="tight")
    print("Salvato: images/pearson.png")

    # -- FIGURA 2: camou.png 
    fig2, ax = plt.subplots(figsize=(7, 4.2))

    labels = ["Contatore\npuro", "Camouflage\nlight", "Camouflage\nstrong", "Normale"]
    corrs  = [cs["bet_tc_correlation"], ls["bet_tc_correlation"],
              ss["bet_tc_correlation"], ns["bet_tc_correlation"]]
    colors = ["#d6604d", "#f4a582", "#92c5de", "#2166ac"]

    bars = ax.bar(labels, corrs, color=colors, width=0.5, edgecolor="white")
    ax.axhline(0.75, color="black", linewidth=1.2, linestyle="--")
    ax.text(3.45, 0.76, "Soglia rilevamento (0.75)",
            ha="right", va="bottom", fontsize=9)
    for bar, val in zip(bars, corrs):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.015,
                f"{val:.4f}", ha="center", fontsize=9)
    ax.set_ylabel("Correlazione puntata / True Count (Pearson r)")
    ax.set_title("Degradazione della correlazione al crescere del camouflage")
    ax.set_ylim(-0.05, 1.05)

    fig2.savefig("images/camou.png", dpi=300, bbox_inches="tight")
    print("Salvato: images/camou.png")