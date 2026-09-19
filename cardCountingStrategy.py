from strategy import AdvancedStrategy

class CardCountingStrategy(AdvancedStrategy):
    def __init__(self, num_decks=6):
        super().__init__()
        self.running_count = 0  #conteggio corrente Hi-Lo
        self.cards_seen = 0
        self.num_decks = num_decks
        self.total_cards = 52 * num_decks
    
    def update_count(self, card):
        value = card.value()
        
        if isinstance(value, tuple):  # Asso
            self.running_count -= 1
        elif value >= 10:  # 10, J, Q, K
            self.running_count -= 1
        elif 2 <= value <= 6:  # Carte basse
            self.running_count += 1
        
        self.cards_seen += 1
    
    def get_true_count(self):                 #RUNNING COUNT/MAZZI RIMANENTI
        cards_remaining = self.total_cards - self.cards_seen
        decks_remaining = max(0.5, cards_remaining / 52)
        return round(self.running_count / decks_remaining, 1)
    
    def get_bet_size(self, base_bet=1):
        tc = self.get_true_count()
        
        if tc <= 0:
            return base_bet          # TC <= 0  → 1x (minima)
        elif tc <= 1:
            return base_bet * 2      # 0 < TC <= 1 → 2x
        elif tc <= 3:
            return base_bet * 4      # 1 < TC <= 3 → 4x  (TC = 3 incluso)
        else:
            return base_bet * 12      # TC > 3 (TC >= 4) → 12x (massima)   #PRIMI TEST CON (x8)#
    
    def decide(self, player_hand, dealer_card):
        tc = self.get_true_count()
        player_value = player_hand.get_value()
        dealer_value = dealer_card.value()
        
        if isinstance(dealer_value, tuple):
            dealer_value = 11
            
        is_pair = (len(player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank)
    
        # Le deviazioni si applicano solo a mani non più splittabili
        if not is_pair:
            # Deviazione: 16 vs 10
            if player_value == 16 and dealer_value == 10:
                if tc >= 0:
                    return 'stand'
                else:
                    return 'hit'
            # Deviazione: 15 vs 10
            if player_value == 15 and dealer_value == 10:
                if tc >= 4:
                    return 'stand'
                return super().decide(player_hand, dealer_card)

            # Deviazione: 12 vs 2
            if player_value == 12 and dealer_value == 2:
                if tc >= 3:
                    return 'stand'
            # Deviazione: 12 vs 3
            if player_value == 12 and dealer_value == 3:
                if tc >= 2:
                    return 'stand'
        
        # Delega ad AdvancedStrategy
        return super().decide(player_hand, dealer_card)
    
    def reset_count(self):
        """Reset dopo shuffle"""
        self.running_count = 0
        self.cards_seen = 0