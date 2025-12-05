
from otree.api import *
import math
c = cu
doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2
    ENDOWMENT = [cu(1), cu(10), cu(1)]
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    total_contribution_1 = models.CurrencyField()
    total_contribution_2 = models.CurrencyField()
    total_contribution_3 = models.CurrencyField()

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p3 = group.get_player_by_id(3)
    p1_payoff = [p1.contribution, p2.contribution]
    p2_payoff = [p1.contribution, p2.contribution, p3.contribution]
    p3_payoff = [p2.contribution, p3.contribution]

    contributions_1 = 0
    for p in p1_payoff:
        contributions_1 += p
    group.total_contribution_1 = contributions_1
    p1.payoff = (
            (C.ENDOWMENT[0] - p1_payoff[0]) + (1/2) * (group.total_contribution_1)
    )


    contributions_2 = 0
    for p in p2_payoff:
        contributions_2 += p
    group.total_contribution_2 = contributions_2
    p2.payoff = (
            (C.ENDOWMENT[1] - p2_payoff[1]) + (1/3) * (group.total_contribution_2)
    )


    contributions_3 = 0
    for p in p3_payoff:
        contributions_3 += p
    group.total_contribution_3 = contributions_3
    p3.payoff = (
            (C.ENDOWMENT[2] - p3_payoff[1]) + (1/2) * (group.total_contribution_3)
    )




class Player(BasePlayer):
    contribution = models.CurrencyField(label='How much will you contribute?', min=0)
    major = models.StringField(label='What is your major?')
    year = models.StringField(
        label='What year are you in?',
        choices = [
            ('freshman'),
            ('sophomore'),
            ('junior'),
            ('senior'),
        ],
        widget=widgets.RadioSelect
    )
    Econ = models.IntegerField(label='How many econ classes have you taken? (Please enter a number)')
    Math = models.IntegerField(label='How many math classes have you taken? (Please enter a number)')


def contribution_max(player):
    if player.id_in_group == 1:
        return C.ENDOWMENT[0]
    elif player.id_in_group == 2:
        return C.ENDOWMENT[1]
    else:
        return C.ENDOWMENT[2]


class Instruction(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    form_model = 'player'

    def vars_for_template(self):
        group = self.group
        player1 = group.get_player_by_id(1)
        player2 = group.get_player_by_id(2)
        player3 = group.get_player_by_id(3)
        return {
            'player1_contribution': player1.contribution,
            'player1_payoff': player1.payoff,
            'player2_contribution': player2.contribution,
            'player2_payoff': player2.payoff,
            'player3_contribution': player3.contribution,
            'player3_payoff': player3.payoff,
        }


class Survey(Page):
    form_model = 'player'
    form_fields = ['major', 'year', 'Econ', 'Math']

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


page_sequence = [Instruction, Contribute, ResultsWaitPage, Results, Survey]