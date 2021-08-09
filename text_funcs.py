# import nltk
#NLTK has some doesn't really work in heroku for some reason


# A file that contains text functions which help working with reddit comments
# and improve the search and answers quality


def remove_all(word: str, to_replace: tuple) -> str:
    """Replaces every word(words are passed in to_replace tuple)
    of the question(passed word var) except for the word that
    will be searched in wikipedia to give users its meaning"""

    for i in to_replace:
        word = word.replace(i, '')

    return word


def remove_chars(word):
    """Used to replace all the characters of the word.
    In this program we replace it in the wiki page title,
    so it can reply to some words .
    Example:
        word: austin
        page title: austin, texas

    If the ',' is kept in the page title, bot will not reply
        """

    chars = ('.', ',', ':', '!', '?')  # that's it for now

    for char in chars:
        word = word.replace(char, '')

    return word


def check_question(question: str, excluding_words: tuple) -> bool:
    """Returns true to confirm that the question is valid
    and lets continue the search if there are no excluding
    words in it.Otherwise returns false and stops
    the search since it doesn't make sense anymore"""

    # Checking if the question has excluding words
    for word in excluding_words:
        if word in question:
            return False

    return True


# def is_adjective(word: str) -> bool:
#     """
#     Checking whether the word is adjective to avoid replying to comments like:
#     # What's better?/ Who's beautiful? etc.
#     :param word: str
#     :return: bool
#     """
#
#     word = word.capitalize().strip()
#     token = nltk.word_tokenize(word)
#     part_of_speech = nltk.pos_tag(token)
#
#     # JJ - adjective, JJR - comparative form of adjective
#     if (word, 'JJ') in part_of_speech or (word, 'JJR') in part_of_speech:
#         return True
#
#     return False


check_words = ["what is ", "what's ", "who is ", "who's ", "who are ", "what are "]


def pattern2(text):
    for i in check_words:
        if i in text:
            return i

    return None


memes = {
    "joe": "Joe Mama :D",
    "candice": "Candice dick fit in your mouth?",
    "ligma": "Ligma balls :D",
    "steve jobs": "Ligma balls :D",
    "love": "baby don't hurt me",
    "yuri": "Yuri Tarded",
    "suckma": "suckma dick :D",
    "sugma": "sugma dick :D",
    "deez": "deez nuts :D"
}


def get_meme(text):
    return memes.get(text)
