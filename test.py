import sentences as s
import text_funcs as tf
import excluding_words as ew
from mediawikiapi import MediaWikiAPI, PageError, MediaWikiAPIException as Exc


def make_page_and_reply(text, auto_s=False):

    # Trying to find the appropriate wikipedia page
    try:
        pg = mwa.page(text, auto_suggest=auto_s)
        print(text)
        print(pg.url)
    except (PageError, Exc, KeyError) as e:
        print(f'Wikipedia Exception: {e}')

        if not auto_s:
            auto_s = True
            make_page_and_reply(text, auto_s=auto_s)

    # If the page is found
    else:

        print(f'testing the title {pg.title.lower()}')
        # Checking if the page matches the search
        pg.title = tf.remove_chars(pg.title)

        print('title is valid')

        if all([i in pg.title.lower().split() for i in text.split()]):
            reply = mwa.summary(text, sentences=2, auto_suggest=auto_s)

            # Showing all the page content if the word can have a few different meanings
            if any(i in reply for i in ew.link_only):
                reply = s.few_meanings_reply(text)

            # Replying to a comment
            print(f"{reply}\n\nMore details here: "
                  f"<{pg.url}> ")


def send(text):
    print(f'Testing: {text}')
    length = len(text.split())

    # Meme replies
    memes = tf.get_meme(text.strip())
    if memes:
        print(memes)

    # No replies to short and long searches and abbreviations
    elif length <= 3 and len(text) >= 3:
        print('passed')
        make_page_and_reply(text)


def check_and_send(comment):
    # Checking if this is a question
    print(tf.check_question(comment, ew.quotes))
    if '?' in comment.lower() and '/s' not in comment.lower():

        # Splitting one comment to 1 or more questions
        comment_lower = comment.lower().split('?')[:-1]

        # Iterating through all the questions in the comment
        for i in comment_lower:
            i += ' '  # space added so checking exclusions can be more precise

            if not tf.check_question(i, ew.excluding_words1) or not tf.check_question(comment, ew.quotes):
                print('s')
                break

            if '.' in i:
                i = i[i.rfind('.') + 1:]

            valid_question = tf.check_question(i, ew.excluding_words1)
            print(i)

            # Checking pattern 1: What does X mean?
            if 'what does ' in i and ' mean' in i and valid_question:

                # Slicing the sentence so only the question remains
                i = i[i.index('what does '):]

                # Removing everything except for the word to search for
                i = tf.remove_all(i, ew.to_replace1)
                send(i)

            # Resetting valid_question's value to check the second pattern
            else:
                verb = ('who\'s ' in i or 'who is ' in i) and 'ing ' in i
                valid_pattern = tf.pattern2(i)

                # Checking pattern 2: What/who is/are X?
                if valid_pattern and not verb:

                    i = i.replace(valid_pattern, '')
                    i = ' ' + i

                    valid_question = tf.check_question(i, ew.excluding_words2)

                    if valid_question:
                        print('about to reply ...')
                        # Removing everything except for the word to search for
                        i = tf.remove_all(i, ew.to_replace2)

                        send(i)


def read_comment(comment):
    check_and_send(comment)


def main():
    comment = None

    while comment != '.':
        comment = input()
        read_comment(comment)
        print('search ended')


if __name__ == '__main__':
    mwa = MediaWikiAPI()  # Creating a wikipedia API variable
    main()
