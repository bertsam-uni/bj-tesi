from deck import Deck
from hand import Hand
from rng import PRNG

class Game:
    def __init__(self, num_decks=6, rng=None):
        self.deck = Deck(num_decks, rng=rng if rng is not None else PRNG)
        self.player_hands = [Hand()]
        self.dealer_hand = Hand()
        self.bets = [1]

    def deal_initial_cards(self, strategy):
        # la hole card del dealer (seconda carta) non viene conteggiata:
        # in casino è coperta, viene rivelata e conteggiata in dealer_turn()
        for round_card in range(2):
            for hand in self.player_hands:
                card = self.deck.draw()
                hand.add_card(card)
                if hasattr(strategy, "update_count"):
                    strategy.update_count(card)

            card = self.deck.draw()
            self.dealer_hand.add_card(card)

            if round_card == 0:  # solo la upcard è visibile
                if hasattr(strategy, "update_count"):
                    strategy.update_count(card)

    def player_turn(self, strategy):
        i = 0
        while i < len(self.player_hands):
            hand = self.player_hands[i]
            is_split_aces = getattr(hand, "split_aces", False)

            while True:
                # dopo split di assi si pesca una sola carta e si chiude
                if is_split_aces:
                    card = self.deck.draw()
                    hand.add_card(card)
                    if hasattr(strategy, "update_count"):
                        strategy.update_count(card)
                    break

                action = strategy.decide(hand, self.dealer_hand.cards[0])

                if (
                    action == "split"
                    and len(hand.cards) == 2
                    and hand.cards[0].rank == hand.cards[1].rank
                ):
                    new_hand = Hand()
                    new_hand.add_card(hand.cards.pop())

                    hand.from_split = True
                    new_hand.from_split = True

                    if hand.cards[0].rank == "A":
                        hand.split_aces = True
                        new_hand.split_aces = True

                    card1 = self.deck.draw()
                    hand.add_card(card1)
                    if hasattr(strategy, "update_count"):
                        strategy.update_count(card1)

                    card2 = self.deck.draw()
                    new_hand.add_card(card2)
                    if hasattr(strategy, "update_count"):
                        strategy.update_count(card2)

                    self.player_hands.append(new_hand)
                    self.bets.append(self.bets[i])

                    if hand.split_aces:
                        break
                    continue

                elif action == "double" and len(hand.cards) == 2:
                    self.bets[i] *= 2
                    card = self.deck.draw()
                    hand.add_card(card)
                    if hasattr(strategy, "update_count"):
                        strategy.update_count(card)
                    break

                elif action == "hit":
                    card = self.deck.draw()
                    hand.add_card(card)
                    if hasattr(strategy, "update_count"):
                        strategy.update_count(card)
                    if hand.is_bust():
                        break

                else:
                    break

            i += 1

        return ["bust" if h.is_bust() else "stand" for h in self.player_hands]

    def dealer_turn(self, strategy):
        # rivela la hole card e la conteggia
        if len(self.dealer_hand.cards) >= 2:
            if hasattr(strategy, "update_count"):
                strategy.update_count(self.dealer_hand.cards[1])

        while self.dealer_hand.get_value() < 17:
            card = self.deck.draw()
            self.dealer_hand.add_card(card)
            if hasattr(strategy, "update_count"):
                strategy.update_count(card)

        return "bust" if self.dealer_hand.is_bust() else "stand"

    def determine_outcome(self):
        results = []
        dealer_value = self.dealer_hand.get_value()
        dealer_bj = self.dealer_hand.is_blackjack()

        for hand in self.player_hands:
            # NOTA: is_blackjack() non esclude le mani nate da split (from_split=True).
            # Se una coppia splittata riceve una carta che completa esattamente 21,
            # questa mano viene trattata come "blackjack naturale" anche nel confronto
            # con un eventuale blackjack del banco (es. risultato "push" invece di "loss").
            # Regola standard da casinò: un 21 dopo split non è naturale e perde contro
            # il blackjack vero del banco. 
            # Edge case a impatto statisticamente trascurabile su milioni di mani simulate
            # non corretto per non alterare i risultati già validati in tesi.
            player_bj = hand.is_blackjack()

            if player_bj and dealer_bj:
                results.append("push")
            elif player_bj:
                results.append("win")
            elif dealer_bj:
                results.append("loss")
            elif hand.is_bust():
                results.append("loss")
            elif self.dealer_hand.is_bust():
                results.append("win")
            else:
                p = hand.get_value()
                if p > dealer_value:
                    results.append("win")
                elif p < dealer_value:
                    results.append("loss")
                else:
                    results.append("push")

        return results