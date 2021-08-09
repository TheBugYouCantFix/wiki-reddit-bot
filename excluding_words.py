# Questions with the words that are used in the daily questions like:
# "What's the reason/matter?", "What's up?", "What's the reason/point?" and others
# should be ignored because the bot can't answer the right

# Excluding words for the first pattern
excluding_words1 = {'‘', ' it ', 'i\'m', ' dat', 'those', 'these', 'this ', 'that', 'you ', ' her ', 'here ',
                    'the', 'they ', ' we ', ' he ', ' she ', ' his ', 'my ', 'their', 'thing', ' not ',
                    'your ', 'our', 'called', 'name', 'him ', 'normal ', 'special', 'ya ', 'then'}

# Fuck NLTK, all my homies use self-made adjectives set
adjectives = {' good ', ' better ', ' worse ', ' bad ', ' new ', ' smart',
              'fair', 'wanted', 'true', 'false', 'first', 'different', 'obvious ',
              ' close', 'alive', ' easy ', ' easier ', ' broken ', ' gross'}

# Excluding words for the second pattern
excluding_words2 = {
    'point', ' be', 'in ', 'so ', ' up', ' with', 'would ',  ' every', ' over ',
    'going', 'more ', 'too ',  ' coach', 'score', 'to ', 'next', ' tomorrow', 'yesterday',
    'body ', 'reason', ' in ', ' on ', 'out ', 'inside ', 'enough',
    'happen', 'da  ', 'meaning',  'and ', ' outside ', ' who ', ' what '}.union(adjectives)

quotes = ('"', "“")

to_replace1 = ('what does ', 'mean', 'even ')
to_replace2 = (" an ", " a ")

link_only = ("may refer to", "can refer to", "may stand for", "refers to", "refer to", "can mean")
