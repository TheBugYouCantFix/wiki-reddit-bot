import prawcore
import sentences
from mediawikiapi import MediaWikiAPI, MediaWikiAPIException as Exc, PageError
from praw import Reddit, exceptions
from tenacity import retry, wait_chain, wait_fixed

# These all are fake except for the username
reddit = Reddit(client_id="id", client_secret="secret",
                password="password",
                user_agent="agent",
                username="wikipedia_answer_bot")

subreddit = reddit.subreddit('all')

opted_out_users = set()


def remove_all(word: str, to_replace: tuple) -> str:
    """Replaces every word(words are passed in to_replace tuple)
    of the question(passed word var) except for the word that
    will be searched in wikipedia to give users its meaning"""

    for i in to_replace:
        word = word.replace(i, '')

    return word.strip()


def remove_chars(word):
    """Used to replace all the characters of the word.
    In this program we replace it in the wiki page title,
    so it can reply to some words .
    Example:
        word: austin
        page title: austin, texas

    If the ',' is kep in the page title, bot will not reply
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


def send(text, comment):
    length = len(text.split())

    # Joe mama joke
    if text == "joe":
        comment.reply(f"Joe Mama :D\n\n{sentences.comment_reply}{sentences.festivity_reply()}")
        print("Reply Success --> I just dropped a joe bomb on 'em")

    # No replies to short and long searches
    elif length <= 3 and len(text) >= 3:

        # Trying to find the appropriate wikipedia page
        try:
            pg = mediawikiapi.page(text)
        except (PageError, Exc, KeyError) as e:
            print(f'Wikipedia Exception: {e}')

        # If the page is found
        else:

            # Checking if the page matches the search
            pg.title = remove_chars(pg.title)
            if all([i in pg.title.lower().split() for i in text.split()]):
                try:
                    reply = mediawikiapi.summary(text, sentences=2)

                    # Showing all the page content if the word can have a few different
                    # meanings or the article is too small
                    if "may refer to" in reply:
                        reply = f'This word/phrase({text}) has a few different meanings.' \
                                ' You can see all of them by clicking the link below.'

                    # Replying to a comment
                    comment.reply(f"{reply}\n\nMore details here: "
                                  f"{pg.url} {sentences.comment_reply}{sentences.festivity_reply()}")

                    print(f"Reply Success: {pg.title}")

                except (prawcore.exceptions.Forbidden, exceptions.RedditAPIException,
                        prawcore.exceptions.ServerError, prawcore.ServerError, KeyError) as e:
                    print(f'Praw Exception: {e}')


def opt_out(comment):
    if comment.body.lower() == "opt out":
        opted_out_users.add(comment.author.name)

    # TODO: get the submission id and make condition checking whether the comment was written under the exact post


def check_and_send(comment):
    # Checking if this is a question
    if '?' in comment.body and comment.author.name not in opted_out_users:

        # Splitting one comment to 1 or more questions
        comment_lower = comment.body.lower().split('?')[:-1]

        # Questions with the words that are used in the daily questions like:
        # "What's the reason/matter?", "What's up?", "What's the reason/point?" and others
        # should be ignored because the bot can't answer the right

        # Excluding words for the first pattern
        excluding_words1 = ('‘', ' it', ' your ', 'i\'m', '"', ' dat', 'those', 'these', 'this', 'that',
                            ' the ', "“", ' they', ' we', ' he', ' she', 'his', ' my', ' their',
                            ' you', ' our', ' called', ' name', ' him', 'normal ', ' special', ' ya ')

        # Excluding words for the for the second pattern
        excluding_words2 = excluding_words1 + (
            ' point', ' wrong', ' be', ' next', ' in', ' so', ' up', ' with', 'would ', 'alive', ' local', ' every',
            'differen', ' good', ' bad', 'going', 'more ', ' too ', 'first', ' coach', 'the', 'score', ' to ', ' next',
            ' not ', 'body ', 'er ', ' reason', ' new', ' old', ' in ', ' on ', ' out ', ' inside ', ' inside',
            'close ', ' fair ', ' happen')

        # Iterating through all the questions in the comment
        for i in comment_lower:
            i += ' '  # space added so checking exclusions can be more precise

            replied = False  # tracks if the bot answered the question
            valid_question = check_question(i, excluding_words1)

            # Exceptions like New York(and other geographical names like this) and normal distribution
            valid_question = True if ('new' in i and i[-1] != 'w') or ('normal ' in i and i[-1] != 'l') \
                else valid_question

            # Checking pattern 1: What does X mean?
            if 'what does ' in i and ' mean' in i and valid_question:

                to_replace1 = ('what does ', ' mean', ' stand for', ' even')

                # Removing everything except for the word to search for
                i = remove_all(i, to_replace1)
                send(i, comment)
                replied = True

            # Resetting valid_question's value to check the second pattern
            else:
                valid_question = check_question(i, excluding_words2)

                # Checking pattern 2: What/who is/are X?
                # P.S. <'who' in i and 'ing' not in i> is needed to avoid replying to verbs. E.G: "Who is playing?"
                if ('what is ' in i or ('who is ' in i or "who's " in i and 'ing' not in i) or
                        'what\'s ' in i) and valid_question and not replied:

                    to_replace2 = ('who\'s', "what\'s", "whats", "what", "who", " is ", " are ", "who's",
                                   "what's", " an ", " a ")

                    # Removing everything except for the word to search for
                    i = remove_all(i, to_replace2)
                    send(i, comment)


def read_comment(comment):
    # Checking if the comment is valid
    if hasattr(comment, 'body') and hasattr(comment.author, 'name') and comment.author.name != "wikipedia_answer_bot":
        check_and_send(comment)


# Reconnecting to the server if there's 503 error(Service Unavailable)
@retry(wait=wait_chain(*[wait_fixed(3) for i in range(3)] +
                        [wait_fixed(7) for j in range(2)] +
                        [wait_fixed(9)]))
def main():
    # Scanning all the new comments and checking them with the functions above
    for comment in subreddit.stream.comments(skip_existing=True):
        read_comment(comment)


if __name__ == '__main__':
    mediawikiapi = MediaWikiAPI()  # Creating a wikipedia API variable
    main()
