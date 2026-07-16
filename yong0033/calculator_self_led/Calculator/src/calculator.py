'''Author: Charlotte Pierce
For FIT2107.
'''


class Calculator():
    '''A calculator class.'''

    def __init__(self):
        '''Initialise answer to 0.'''
        self._answer = 0

    def get_answer(self):
        '''Get the current answer stored by the calculator.'''
        return self._answer

    def reset(self):
        '''Reset the internal answer to 0.'''
        self._answer = 0
        return self

    def add(self, num):
        '''Add `num` to the currently stored answer.'''
        self._answer += num
        return self

    def subtract(self, num):
        '''Subtract `num` from the currently stored answer.'''
        self._answer -= num
        return self

    def multiply(self, num):
        '''Multiply `num` with the currently stored answer.'''
        self._answer *= num

    def power(self, num):
        '''Raise the currently stored answer to the power of `num`.'''
        self._answer = self._answer ** num
        return self
