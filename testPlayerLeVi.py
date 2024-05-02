from pypokerengine.players import BasePokerPlayer
import random as rand
import pprint

class TestPlayer(BasePokerPlayer):
  deck = []
  for suit in ['H', 'D', 'S', 'C']:
    for number in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
      card = suit + number
      deck.append(card)

  def declare_action(self, valid_actions, hole_card, round_state):
    # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
    pp = pprint.PrettyPrinter(indent=2)
    # print("------------ROUND_STATE(RANDOM)--------")
    # pp.pprint(round_state)
    # print("------------HOLE_CARD----------")
    # pp.pprint(hole_card)
    # print("------------VALID_ACTIONS----------")
    # pp.pprint(valid_actions)
    # print("-------------------------------")
    table = round_state['community_card']
    hand = hole_card
    # pp.pprint(hand)
    # pp.pprint(valid_actions)
    if(len(table) == 0):
        action = valid_actions[1]["action"]
        return action
        # call_action_info = self.handle_starting_hand(hand, valid_actions)
        # return call_action_info["action"]
    else:
      round_win_rate = self.win_rate(hand, table)
      if round_win_rate > 0.75:
        for i in valid_actions:
          if i["action"] == "raise":
              action = i["action"]
              return action
        action = valid_actions[1]["action"]
        return action
      elif round_win_rate > 0.4: 
        action = valid_actions[1]["action"]
        return action
      else:
        action = valid_actions[0]["action"]
        return action

    # r = rand.random()
    # if r <= 0.5:
    #   call_action_info = valid_actions[1]
    # elif r<= 0.9 and len(valid_actions ) == 3:
    #   call_action_info = valid_actions[2]
    # else:
    #   call_action_info = valid_actions[0]
    # action = call_action_info["action"]
    # return action  # action returned here is sent to the poker engine

  def handle_starting_hand(self, hand, valid_actions):
    card1 = hand[0]
    card2 = hand[1]
    # if card1[1] == card2[1] and ord(card1[1]) >= 54:
    if card1[1] == card2[1]:
        if len(valid_actions) == 3:
            return valid_actions[2]
        else:
            return valid_actions[1]
    elif card1[1] == 'A' or card1[1] == 'K' or card2[1] == 'A' or card2[1] == 'K':
        if len(valid_actions) == 3:
            return valid_actions[2]
        else:
            return valid_actions[1]
    elif card1[0] == card2[0] and ((card1[1] == 'Q' and card2[1] == 'J') or (card1[1] == 'J' and card2[1] == 'Q') or (card1[1] == 'Q' and card2[1] == 'T') or (card1[1] == 'T' and card2[1] == 'Q') or (card1[1] == 'Q' and card2[1] == '9') or (card1[1] == '9' and card2[1] == 'Q') or (card1[1] == 'J' and card2[1] == 'T') or (card1[1] == 'T' and card2[1] == 'J') or (card1[1] == 'J' and card2[1] == '9') or (card1[1] == '9' and card2[1] == 'J') or (card1[1] == 'T' and card2[1] == '9') or (card1[1] == '9' and card2[1] == 'T')):
        if len(valid_actions) == 3:
            return valid_actions[2]
        else:
            return valid_actions[1]
    return valid_actions[0]

  def handle_flop_street(self, hand, valid_actions):
    pass

  def win_rate(self, hand, table):
    my_cards = []
    opponent_cards = []
    score = 0
    overallCases = 0
    for card in hand:
        my_cards.append(card)
    for card in table:
        my_cards.append(card)
        opponent_cards.append(card)
    my_best = self.best_hand_level(my_cards)
    for card1Idx in range(0, 52):
      for card2Idx in range(card1Idx + 1, 52):
        card1 = self.deck[card1Idx]
        card2 = self.deck[card2Idx]
        if card1 not in hand and card1 not in table and card2 not in hand and card2 not in table:
          opponent_cards.append(card1)
          opponent_cards.append(card2)
          opponent_best = self.best_hand_level(opponent_cards)
          if my_best > opponent_best:
            score += 1
          elif my_best == opponent_best:
            score += 0.5
          overallCases += 1
          opponent_cards = opponent_cards[:-2]
    return score/overallCases
    

  def best_hand_level(self, hand):
    hand_size = len(hand)
    max_level = 0
    hand_five = []
    for i1 in range(0, hand_size):
      hand_five.append(hand[i1])
      for i2 in range(i1 + 1, hand_size):
        hand_five.append(hand[i2])
        for i3 in range(i2 + 1, hand_size):
          hand_five.append(hand[i3])
          for i4 in range(i3 + 1, hand_size):
            hand_five.append(hand[i4])
            for i5 in range(i4 + 1, hand_size):
              hand_five.append(hand[i5])
              hand_score = self.calculate_hand(hand_five)
              max_level = max(max_level, hand_score)
              hand_five = hand_five[:-1]
            hand_five = hand_five[:-1]
          hand_five = hand_five[:-1]
        hand_five = hand_five[:-1]
      hand_five = hand_five[:-1]
    return max_level

  def calculate_hand(self, hand):
    reformatted_hand = []
    for card in hand:
      reformatted_card = card[0]
      if ord(card[1]) > 57:
        if card[1] == 'T':
          reformatted_card = ':' + reformatted_card
        elif card[1] == 'J':
          reformatted_card = ';' + reformatted_card
        elif card[1] == 'Q':
          reformatted_card = '<' + reformatted_card
        elif card[1] == 'K':
          reformatted_card = '=' + reformatted_card
        elif card[1] == 'A':
          reformatted_card = '>' + reformatted_card
      else: 
        reformatted_card = card[1] + reformatted_card
      reformatted_hand.append(reformatted_card)
    reformatted_hand.sort()
    # print(reformatted_hand)
    if ord(reformatted_hand[1][0]) - ord(reformatted_hand[0][0]) == 1 and ord(reformatted_hand[2][0]) - ord(reformatted_hand[1][0]) == 1 and ord(reformatted_hand[3][0]) - ord(reformatted_hand[2][0]) == 1 and ord(reformatted_hand[4][0]) - ord(reformatted_hand[3][0]) == 1:
      if reformatted_hand[0][1] == reformatted_hand[1][1] and reformatted_hand[1][1] == reformatted_hand[2][1] and reformatted_hand[2][1] == reformatted_hand[3][1] and reformatted_hand[3][1] == reformatted_hand[4][1]:
        if reformatted_hand[0][0] == ':':
          return 9
        else:
          return 8
      else:
        return 4
    dupe_score = self.check_dupes(reformatted_hand)
    if dupe_score > 0:
      return dupe_score
    if reformatted_hand[0][1] == reformatted_hand[1][1] and reformatted_hand[1][1] == reformatted_hand[2][1] and reformatted_hand[2][1] == reformatted_hand[3][1] and reformatted_hand[3][1] == reformatted_hand[4][1]:
      return 5
    return 0
      

  def check_dupes(self, hand):
    count_dict = {}
    check3 = False
    check2_1 = False
    check2_2 = False
    for card in hand:
      if card[0] in count_dict:
        count_dict[card[0]] += 1
      else:
        count_dict[card[0]] = 1
    for count in count_dict.values():
      if count >= 4:
        return 7
      if count == 3:
        check3 = True
      if count == 2:
        if check2_1 == False:
          check2_1 = True
        else:
          check2_2 = True
    if check3 == True:
      if check2_1 == True:
        return 6
      return 3
    if check2_1 == True:
      if check2_2 == True:
        return 2
      return 1
    return 0

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass

def setup_ai():
  return TestPlayer()
