class FiniteStateAutomaton:
    def __init__(self):
        self.current_state = 'q0'

    def transition(self, char):
        if self.current_state == 'q0' and char == 'a':
            self.current_state = 'q1'
        elif self.current_state == 'q1' and char == 'b':
            self.current_state = 'q2'
        else:
            self.current_state = 'q0' 

    def is_accepted(self):
        return self.current_state == 'q2'

def match_pattern(input_string):
    automaton = FiniteStateAutomaton()
    for char in input_string:
        automaton.transition(char)
    return automaton.is_accepted()
print(match_pattern("testab"))  
print(match_pattern("ab"))     
print(match_pattern("abc"))     
