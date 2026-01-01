import random

# Define card values and deck
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck = [f'{value} of {suit}' for value in card_values.keys() for suit in suits]

# Shuffle the deck
random.shuffle(deck)

# Initialize player's money
money = 100

def deal_card():
    """Deal a card from the deck."""
    global deck
    if len(deck) < 20:  # Reshuffle if deck is running low
        print("Reshuffling the deck...")
        deck = [f'{value} of {suit}' for value in card_values.keys() for suit in suits]
        random.shuffle(deck)
    return deck.pop()

def calculate_hand_value(hand):
    """Calculate the value of a hand."""
    value = sum(card_values[card.split()[0]] for card in hand)
    # Adjust for Aces if value > 21
    aces = sum(1 for card in hand if card.startswith('A'))
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def play_hand(player_hand, bet):
    """Play a single hand of Blackjack."""
    global deck, money
    print(f"\nYour hand: {', '.join(player_hand)} (Value: {calculate_hand_value(player_hand)})")

    # Check for player Blackjack
    if calculate_hand_value(player_hand) == 21:
        print("Blackjack! You win 1.5x your bet!")
        return bet * 1.5

    # Check for split option
    if len(player_hand) == 2 and card_values[player_hand[0].split()[0]] == card_values[player_hand[1].split()[0]]:
        split_choice = input("Do you want to split? (yes/no) ").strip().lower()
        if split_choice == 'yes':
            if money < bet:
                print("You don't have enough money to split.")
            else:
                # Split the hand into two hands
                money -= bet  # Deduct the additional bet for the split hand
                hand1 = [player_hand[0], deal_card()]
                hand2 = [player_hand[1], deal_card()]
                print(f"\nFirst split hand: {', '.join(hand1)}")
                print(f"Second split hand: {', '.join(hand2)}")
                # Play both split hands recursively
                result1 = play_hand(hand1, bet)
                result2 = play_hand(hand2, bet)
                return result1 + result2

    # Player's turn
    while calculate_hand_value(player_hand) < 21:
        action = input("Do you want to Hit or Stand? ").strip().lower()
        if action == 'hit':
            player_hand.append(deal_card())
            print(f"Your hand: {', '.join(player_hand)} (Value: {calculate_hand_value(player_hand)})")
        elif action == 'stand':
            break
        else:
            print("Invalid input. Please type 'Hit' or 'Stand'.")

    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        print("Bust! You lose your bet.")
        return -bet
    else:
        print(f"You stand with {player_value}.")
        return player_value

def main():
    global money, deck
    print("Welcome to Blackjack! You start with $100.")
    while money > 0:
        print(f"\nYou have ${money}.")
        try:
            num_hands = int(input("How many hands do you want to play (1-3)? ").strip())
            if num_hands < 1 or num_hands > 3:
                print("Please enter a number between 1 and 3.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        bets = []
        player_hands = []
        for i in range(num_hands):
            while True:
                try:
                    bet = int(input(f"How much do you want to bet on hand {i+1}? ").strip())
                    if bet > money:
                        print("You don't have enough money.")
                    else:
                        bets.append(bet)
                        money -= bet  # Deduct the bet from the player's money
                        break
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Deal initial cards for each hand
            player_hand = [deal_card(), deal_card()]
            player_hands.append(player_hand)

        # Dealer's hand
        dealer_hand = [deal_card(), deal_card()]
        print(f"\nDealer's hand: {dealer_hand[0]} and [Hidden Card]")

        # Insurance option
        if dealer_hand[0].split()[0] == 'A':
            insurance_choice = input("Do you want to take insurance? (yes/no) ").strip().lower()
            if insurance_choice == 'yes':
                insurance_bet = min(bet // 2, money)  # Insurance bet is half the original bet
                money -= insurance_bet
                print(f"You placed an insurance bet of ${insurance_bet}.")
                if calculate_hand_value(dealer_hand) == 21:
                    print("Dealer has Blackjack! Insurance pays 2:1.")
                    money += insurance_bet * 3  # Return insurance bet + payout
                else:
                    print("Dealer does not have Blackjack. You lose your insurance bet.")

        # Play each player hand
        results = []
        for i in range(num_hands):
            print(f"\nPlaying hand {i+1}...")
            result = play_hand(player_hands[i], bets[i])
            results.append(result)

        # Dealer's turn
        print(f"\nDealer's hand: {', '.join(dealer_hand)} (Value: {calculate_hand_value(dealer_hand)})")
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card())
            print(f"Dealer hits: {dealer_hand[-1]}")
            print(f"Dealer's hand: {', '.join(dealer_hand)} (Value: {calculate_hand_value(dealer_hand)})")

        dealer_value = calculate_hand_value(dealer_hand)
        if dealer_value > 21:
            print("Dealer busts!")
        else:
            print(f"Dealer stands with {dealer_value}.")

        # Compare each player hand to the dealer's hand
        for i in range(num_hands):
            player_value = results[i]
            if isinstance(player_value, float):  # Player got a Blackjack
                money += player_value  # Add winnings to money
                print(f"Hand {i+1}: Blackjack! You win ${player_value}!")
            elif player_value == -bets[i]:  # Player busted
                print(f"Hand {i+1}: Bust! You lose ${bets[i]}.")
            else:
                if dealer_value > 21 or player_value > dealer_value:
                    money += bets[i] * 2  # Player wins
                    print(f"Hand {i+1}: You win ${bets[i]}!")
                elif player_value < dealer_value:
                    print(f"Hand {i+1}: Dealer wins! You lose ${bets[i]}.")
                else:
                    money += bets[i]  # Push (return the bet)
                    print(f"Hand {i+1}: It's a tie! You get your ${bets[i]} back.")

        if money <= 0:
            print("You're out of money! Game over.")
            break

        play_again = input("Do you want to play again? (yes/no) ").strip().lower()
        if play_again != 'yes':
            print(f"Thanks for playing! You leave with ${money}.")
            break

if __name__ == "__main__":
    main()
