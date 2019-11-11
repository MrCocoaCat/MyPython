# -*- coding: utf-8 -*-

a = [{'id': 1, 'a': 2},
     {'id': 3, 'a': 2},
     {'id': 2, 'a': 2},
     ]

b = sorted(a, key=lambda x: x['id'])
print(b)


# class Student():
#
#     @property
#     def birth(self):
#         return self._birth
#
#     @birth.setter
#     def birth(self, value):
#         self._birth = value
#
#     @property
#     def age(self):
#         return 2014 - self._birth

class Student():

    __score = 100


    @property
    def score(self):
        return Student.__score

    # @score.setter
    # def score(self, value):
    #     if not isinstance(value, int):
    #         raise ValueError('score must be an integer!')
    #     if value < 0 or value > 100:
    #         raise ValueError('score must between 0 ~ 100!')
    #     Student.__score = value


s = Student()
a = Student
print(s.score)
a.__score = 60
print(s.score)

print(a.__name__)




