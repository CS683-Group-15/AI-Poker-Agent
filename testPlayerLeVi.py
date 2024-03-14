from pypokerengine.players import BasePokerPlayer
import random as rand
import pprint

class TestPlayer(BasePokerPlayer):

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
    for card in table:
        hand.append(card)
    # pp.pprint(hand)
    # pp.pprint(valid_actions)
    if(len(hand) == 2):
        call_action_info = self.handle_starting_hand(hand, valid_actions)
        return call_action_info["action"]
    if(len(hand) == 5):
        self.calculate_hand(hand)
        # call_action_info = self.handle_flop_street(hand, valid_actions)
        # return call_action_info["action"]

    r = rand.random()
    if r <= 0.5:
      call_action_info = valid_actions[1]
    elif r<= 0.9 and len(valid_actions ) == 3:
      call_action_info = valid_actions[2]
    else:
      call_action_info = valid_actions[0]
    action = call_action_info["action"]
    return action  # action returned here is sent to the poker engine

  def handle_starting_hand(self, hand, valid_actions):
    card1 = hand[0]
    card2 = hand[1]
    if card1[1] == card2[1] and ord(card1[1]) >= 54:
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
    print(reformatted_hand)
    if ord(reformatted_hand[1][0]) - ord(reformatted_hand[0][0]) == 1 and ord(reformatted_hand[2][0]) - ord(reformatted_hand[1][0]) and ord(reformatted_hand[3][0]) - ord(reformatted_hand[2][0]) and ord(reformatted_hand[4][0]) - ord(reformatted_hand[3][0]):
      if reformatted_hand[0][1] == reformatted_hand[1][1] and reformatted_hand[1][1] == reformatted_hand[2][1] and reformatted_hand[2][1] == reformatted_hand[3][1] and reformatted_hand[3][1] == reformatted_hand[4][1]:
        if reformatted_hand[0][0] == ':':
          return 9
        else:
          return 8
      else:
        return 4
    dupe_score = check_dupes(reformatted_hand)
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
