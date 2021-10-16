import prawcore
import sentences as s
import text_funcs as tf
import excluding_words as ew
from mediawikiapi import MediaWikiAPI, MediaWikiAPIException as Exc, PageError
from praw import Reddit, exceptions
from tenacity import retry, wait_chain, wait_fixed

# These all are fake except for the username
reddit = Reddit(client_id="id", client_secret="secret",
                password="password",
                user_agent="agent",
                username="wikipedia_answer_bot")

subreddit = reddit.subreddit('all')

never_reply = {"wikipedia_answer_bot", "AutoModerator"}
opted_out_users = set()
OPT_OUT_MESSAGE = "wab opt out"  # wab stands for wikipedia answer bot
OPT_IN_MESSAGE = "wab opt in"

DELETE_MESSAGE = "wab delete"
MIN_SCORE_TO_DELETE = -3


def opt_out_and_opt_in(comment):
    text = comment.body.lower().strip()
    username = comment.author.name

    if text == OPT_OUT_MESSAGE:
        print('there')
        if username in opted_out_users:
            comment.reply(f"You are already opted out, {username}")
        else:
            opted_out_users.add(username)
            comment.reply(
                f"You've been successfully opted out, {username}\n\n Write `wab opt in` if you want to opt in")
            print(f'{username} opted out')

    elif text == OPT_IN_MESSAGE:
        if username not in opted_out_users:
            comment.reply(f"You are already opted in, {username}")
        else:
            opted_out_users.remove(username)
            comment.reply(f"You've been successfully opted in, {username}")
            print(f'{username} opted in')

            
def delete_comment(comment):
    if comment.body.strip().lower() == DELETE_MESSAGE:
        print('trying to delete...')

        try:
            parent_comment = comment.parent()
            score = parent_comment.score

            print(f"score: {score}")

            if score <= MIN_SCORE_TO_DELETE and \
                    parent_comment.author.name == bot_username:

                parent_comment.delete()
                print('deleted successfully')
            else:
                print("can't delete")

        except Exception as e:
            print(f"couldn't delete: {e}")
          

def make_page_and_reply(text, comment, auto_s=False):
    # Trying to find the appropriate wikipedia page
    try:
        pg = mwa.page(text, auto_suggest=auto_s)
    except (PageError, Exc, KeyError) as e:
        print(f'Wikipedia Exception: {e}')

        if not auto_s:
            auto_s = True
            make_page_and_reply(text, comment, auto_s=auto_s)

    # If the page is found
    else:

        # Checking if the page matches the search
        pg.title = tf.remove_chars(pg.title)

        if all([i in pg.title.lower().split() for i in text.split()]):
            try:
                reply = mwa.summary(text, sentences=2, auto_suggest=auto_s)

                # Showing all the page content if the word can have a few different meanings
                if any(i in reply for i in ew.link_only):
                    reply = s.few_meanings_reply(text)

                # Replying to a comment
                comment.reply(f"**{reply}**\n\nMore details here: "
                              f"<{pg.url}> {s.comment_reply}{s.festivity_reply()}")

                print(f"Reply Success: {pg.title}")

            except (prawcore.exceptions.Forbidden, exceptions.RedditAPIException,
                    prawcore.exceptions.ServerError, prawcore.ServerError, KeyError) as e:
                print(f'Praw Exception: {e}')


def send(text, comment):
    length = len(text.split())
    print(f'testing title: {text}')

    # Meme replies
    memes = tf.get_meme(text.strip())

    if memes:
        comment.reply(f"{memes}\n\n{s.comment_reply}{s.festivity_reply()}")

    # No replies to short and long searches
    elif length <= 3 and len(text) >= 3:
        make_page_and_reply(text, comment)


def check_and_send(comment):
    # Checking if this is a question
    if '?' in comment.body and '/s' not in comment.body:

        # Splitting one comment to 1 or more questions
        comment_lower = comment.body.lower().split('?')[:-1]

        # Iterating through all the questions in the comment
        for i in comment_lower:

            i += ' '  # space added so checking exclusions can be more precise

            if not tf.check_question(i, ew.excluding_words1) or not tf.check_question(i, ew.quotes):
                break

            if '.' in i:
                i = i[i.rfind('.') + 1:]

            # Checking pattern 1: What does X mean?
            if 'what does ' in i and ' mean' in i:
                print('pattern1')

                # Slicing the sentence so only the question remains
                i = i[i.index('what does '):]

                # Removing everything except for the word to search for
                i = tf.remove_all(i, ew.to_replace1)
                send(i, comment)

            # Resetting valid_question's value to check the second pattern
            else:
                verb = ('who\'s ' in i or 'who is ' in i) and 'ing ' in i
                valid_pattern = tf.pattern2(i)

                # Checking pattern 2: What/who is/are X?
                # P.S. <'who' in i and 'ing' not in i> is needed to avoid replying to verbs. E.G: "Who is playing?"
                if valid_pattern and not verb:
                    print('pattern2', i)

                    i = i.replace(valid_pattern, '')
                    i = ' ' + i

                    valid_question = tf.check_question(i, ew.excluding_words2)

                    if valid_question:
                        # Removing everything except for the word to search for
                        i = tf.remove_all(i, ew.to_replace2)

                        send(i.strip(), comment)

    else:
        opt_out_and_opt_in(comment)
        delete_comment(comment)


def read_comment(comment):
    # Checking if the comment is valid
    if hasattr(comment, 'body') and hasattr(comment.author, 'name') \
            and (comment.author.name not in opted_out_users or OPT_IN_MESSAGE in comment.body.lower().strip()) \
            and comment.author.name not in never_reply:
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
    mwa = MediaWikiAPI()  # Creating a wikipedia API variable
    main()
