class AdvancedStrategy:
    def decide(self, player_hand, dealer_card):
        dealer_value = dealer_card.value()
        if isinstance(dealer_value, tuple):
            dealer_value = 11
        player_value = player_hand.get_value()

        # split
        if len(player_hand.cards) == 2 and \
           player_hand.cards[0].rank == player_hand.cards[1].rank:
            rank = player_hand.cards[0].rank
            if rank == "A":
                return "split"
            if rank == "8":
                return "split"
            if rank == "9" and dealer_value not in [7, 10, 11]:
                return "split"
            if rank == "7" and 2 <= dealer_value <= 7:
                return "split"
            if rank == "6" and 2 <= dealer_value <= 6:
                return "split"
            if rank in ["2", "3"] and 2 <= dealer_value <= 7:
                return "split"

        # double
        if len(player_hand.cards) == 2:
            if player_value == 11:
                return "double"
            if player_value == 10 and dealer_value <= 9:
                return "double"
            if player_value == 9 and dealer_value in [3, 4, 5, 6]:
                return "double"

        if player_hand.is_soft():
            return self._decide_soft(player_value, dealer_value, len(player_hand.cards))
        return self._decide_hard(player_value, dealer_value)


    def _decide_hard(self, player_value, dealer_value):
        if player_value >= 17:
            return "stand"
        if 13 <= player_value <= 16:
            return "stand" if 2 <= dealer_value <= 6 else "hit"
        if player_value == 12:
            return "stand" if 4 <= dealer_value <= 6 else "hit"
        return "hit"

    def _decide_soft(self, player_value, dealer_value, num_cards):
        if player_value >= 19:
            return "stand"
        if player_value == 18:
            if dealer_value in [2, 3, 4, 5, 6] and num_cards == 2:
                return "double"
            if dealer_value in [7, 8]:
                return "stand"
            return "hit"
        # soft 13-17
        if num_cards == 2:
            if player_value == 17 and 3 <= dealer_value <= 6:
                return "double"
            if player_value in [15, 16] and 4 <= dealer_value <= 6:
                return "double"
            if player_value in [13, 14] and 5 <= dealer_value <= 6:
                return "double"
        return "hit"