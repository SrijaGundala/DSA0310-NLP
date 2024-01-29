class MorphologicalFSM:
    def pluralize_noun(self, noun):
        if noun.endswith('y'):
            return noun[:-1] + 'ies'
        elif noun[-1] in ['s', 'x', 'z'] or noun[-2:] in ['sh', 'ch']:
            return noun + 'es'
        else:
            return noun + 's'
morph_fsm = MorphologicalFSM()
print(morph_fsm.pluralize_noun("cat"))    
print(morph_fsm.pluralize_noun("baby"))   
print(morph_fsm.pluralize_noun("box"))    
