from game import Game
from hand import Hand
from deck import Deck
from strategy import AdvancedStrategy
from rng import PRNG
import math

class MonteCarloSimulator:
    def __init__(self, num_decks=6, strategy=None, rng=None):
        self.num_decks = num_decks
        self.strategy = strategy or AdvancedStrategy()
        self.rng = rng if rng is not None else PRNG

    def run(self, num_hands=100000):
        wins = losses = pushes = 0
        total_payoff = 0
        total_bet = 0
        outcomes = []
        total_hands_played = 0
        tc_history = []
        bet_history = []

        game = Game(self.num_decks, rng=self.rng)

        for _ in range(num_hands):
            # reshuffle a 85% di penetrazione     #PRIMI TEST A 75% #
            if game.deck.cards_remaining() < 0.15 * (52 * self.num_decks):
                game.deck = Deck(self.num_decks, rng=self.rng)
                if hasattr(self.strategy, 'reset_count'):
                    self.strategy.reset_count()

            base_bet = self.strategy.get_bet_size() if hasattr(self.strategy, 'get_bet_size') else 1
            bet_history.append(base_bet) #

            if hasattr(self.strategy, 'get_true_count'):
                tc_history.append(self.strategy.get_true_count())

            game.player_hands = [Hand()]
            game.dealer_hand = Hand()
            game.bets = [base_bet]

            game.deal_initial_cards(self.strategy)
            game.player_turn(self.strategy)
            game.dealer_turn(self.strategy)
            results = game.determine_outcome()

            for idx, result in enumerate(results):
                bet = game.bets[idx]
                hand = game.player_hands[idx]
                total_hands_played += 1
                total_bet += bet

                if result == 'win':
                    wins += 1
                    is_natural_bj = hand.is_blackjack() and not getattr(hand, 'from_split', False)
                    payoff = 1.5 * bet if is_natural_bj else bet
                elif result == 'loss':
                    losses += 1
                    payoff = -bet
                else:
                    pushes += 1
                    payoff = 0

                total_payoff += payoff
                outcomes.append(payoff)

        ev = total_payoff / total_hands_played
        variance = sum((x - ev) ** 2 for x in outcomes) / total_hands_played
        std_error = math.sqrt(variance / total_hands_played)

        return {
            'win_rate': wins / total_hands_played,
            'loss_rate': losses / total_hands_played,
            'push_rate': pushes / total_hands_played,
            'expected_value_per_hand': ev,
            'house_edge': -ev,
            'roi': total_payoff / total_bet if total_bet > 0 else 0,
            'std_error': std_error,
            'total_hands_played': total_hands_played,
            'total_bet': total_bet,
            'total_payoff': total_payoff,
            'tc_history': tc_history,
            'bet_history': bet_history,
            'avg_tc': sum(tc_history) / len(tc_history) if tc_history else 0
        }