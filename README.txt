BJ TESI — README
================================================================================
Autore:           Bertoglio Samuele
Anno accademico:  2025/2026
Matricola:        31410A
================================================================================


DESCRIZIONE
-----------
Simulatore di blackjack in Python per l'analisi probabilistica del conteggio
delle carte (sistema Hi-Lo) tramite metodo Monte Carlo.

Il progetto si articola in tre aree principali:

  1. Simulazione statistica    — convergenza, house edge, ROI
  2. Strategia e card counting — basic strategy ottimale, Hi-Lo, spread 1-2-4-12
  3. Sicurezza informatica     — PRNG vs CSPRNG, seed prediction attack,
                                 behavioural detection, architettura client-server
                                 (replay attack, client-side manipulation),
                                 rilevamento bot, collusion e multi-accounting


STRUTTURA DEL PROGETTO
----------------------

  images/                  Grafici prodotti dalle simulazioni e immagini per la tesi
  tests/                   File di testing

  -- Moduli core --

  card.py                  Classe Card: rank, suit, value, __repr__, __eq__, __hash__
  rng.py                   PRNG (Mersenne Twister) e CSPRNG (Fisher-Yates con secrets)
  deck.py                  Classe Deck: inizializzazione, shuffle, draw, cards_remaining
  hand.py                  Classe Hand: get_value, is_bust, is_blackjack, has_ace
  strategy.py              AdvancedStrategy: basic strategy ottimale (split, double, soft/hard)
  cardCountingStrategy.py  CardCountingStrategy: Hi-Lo, true count, bet spread 1-2-4-12,
                             deviazioni strategiche (16v10, 15v10, 12v2, 12v3)
  game.py                  Logica di gioco: deal, player_turn, dealer_turn, determine_outcome
  montecarlo.py            MonteCarloSimulator: engine principale, penetrazione 85%,
                             raccolta tc_history e bet_history

  -- Script di simulazione e analisi --

  Trun_simulations.py      Confronto AdvancedStrategy vs CardCountingStrategy su 5M mani,
                             validazione con letteratura (Thorp, Griffin, Wong)
  Tconvergenza.py          Verifica convergenza errore standard (legge 1/√n), plot log-log
  behaviouralProfiler.py   BehaviouralProfiler: timing variance, correlazione puntata/TC
                             (Pearson r), rilevamento anomalie con is_suspicious
  TcamouflageTest.py       CamouflageLightStrategy e CamouflageStrongStrategy:
                             simulazione evasione detection e grafico correlazione
  clientServerSim.py       Architettura client-server: nonce, timestamp, replay attack,
                             client-side manipulation, analisi finanziaria aggregata
  seedPredictionAttack.py            Seed prediction attack: determinismo PRNG, impatto economico,
                             mitigazione con CSPRNG

  -- Moduli di detection delle minacce --

  botDetection.py          BotDetector: rileva software automatizzati tramite analisi dei
                             tempi di decisione. Segnali: T_avg < 1 s e T_var < 0.05
                             indicano comportamento meccanico non umano. Un bot applica la
                             strategia in modo infallibile e costante; il giocatore umano
                             presenta tempi più lenti e irregolari per definizione.
                             Soglie predefinite calibrate su profili sintetici (bot: gauss
                             0.1 s σ=0.01; umano: gauss 4.5 s σ=1.2).

  collusionDetection.py    CollusionDetector: rileva chip dumping calcolando la correlazione
                             di Pearson tra le puntate di due giocatori allo stesso tavolo.
                             Una correlazione fortemente negativa (soglia: r < -0.7) indica
                             che un giocatore perde deliberatamente per trasferire valore
                             all'altro. Il profilo collusivo è incompatibile con il gioco
                             indipendente, dove la correlazione attesa è prossima a zero.

  multiAccountingDetection.py
                           MultiAccountingDetector: rileva lo stesso utente su account
                             diversi confrontando il vettore comportamentale normalizzato
                             [T_avg/10, T_var/5, B_avg/100] tra sessioni. La distanza
                             euclidea tra i due vettori misura la somiglianza dei profili:
                             distanza < 0.15 segnala profili statisticamente compatibili
                             con lo stesso individuo. Contrasta i tentativi di aggirare un
                             ban aprendo nuovi account con identità diverse ma comportamento
                             invariato.

  -- Test --

  Ttest_basico.py          Test unitari CardCountingStrategy: sistema Hi-Lo (RC su mazzo
                             completo), true count, bet sizing, deviazioni strategiche,
                             integrazione end-to-end (1M mani)


ESECUZIONE
----------

  Simulazioni principali (5M mani, ~2-3 minuti):
      python Trun_simulations.py

  Verifica convergenza Monte Carlo:
      python Tconvergenza.py

  Behavioural detection e camouflage:
      python TcamouflageTest.py

  Architettura client-server e scenari di attacco:
      python clientServerSim.py

  Seed prediction attack (PRNG vs CSPRNG):
      python seedPredictionAttack.py

  Rilevamento bot:
      python botDetection.py

  Rilevamento collusion (chip dumping):
      python collusionDetection.py

  Rilevamento multi-accounting:
      python multiAccountingDetection.py

  Test unitari:
      python Ttest_basico.py


DIPENDENZE
----------
  pip install numpy scipy matplotlib


NOTE
----
  - RNG predefinito: PRNG (Mersenne Twister) — veloce, adatto alle simulazioni
  - Per ambienti che richiedono sicurezza crittografica: usare CSPRNG (non riproducibile)
  - Penetrazione mazzo: reshuffle al 15% di carte rimanenti (85% di penetrazione, 6 mazzi)
  - Spread bet: 1-2-4-12 unità
  - I moduli botDetection, collusionDetection e multiAccountingDetection producono
    output autonomo se eseguiti direttamente (__main__); sono importabili come classi
    nei moduli di simulazione per estendere la pipeline di detection