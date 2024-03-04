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
