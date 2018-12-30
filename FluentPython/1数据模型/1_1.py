
import collections
import random

# 定义一个namedtuple名称为card
Card = collections.namedtuple('card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = "spades diamonds Clubs hearts".split()

    def __init__(self):
        # _开头意味着其为保护成员变量
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


if __name__ == '__main__':
    duck = FrenchDeck()
    print(duck.ranks)
    print(duck.suits)
    print(duck.__repr__)
    print(duck[1])
    print(random.choice(duck))
