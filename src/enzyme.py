aminoacids = frozenset(
    [   
        'cut', # cut strand(s)
        'del', # delete base from strand
        'swi', # switch enzyme to other strand
        'mvr', # move one unit to the right
        'mvl', # move one unit to the left
        'cop', # turn one Copy mode
        'off', # turn off Copy mode
        'ina', # insert A to the right of this unit
        'inc', # insert C to the right of this unit
        'ing', # insert G to the right of this unit
        'int', # insert T to the right of this unit
        'rpy', # search for the nearest pyrimidine to the right
        'rpu', # search for the nearest purine to the right
        'lpy', # search for the nearest pyrimidine to the left
        'lpu', # search for the nearest purine to the left
    ]
)

class NotInSet(ValueError):
    pass

class NotAString(TypeError):
    pass

class Enzyme:
    """It's a machine operating on strands by means of instructions--Amino Acids"""
    def __init__(self, commands):
        try:
            for item in commands:
                if not isinstance(item, str):
                    raise NotAString
                else:
                    if item not in aminoacids:
                        raise NotInSet
        except TypeError:
            raise
        self.commands = commands