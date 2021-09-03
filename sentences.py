from datetime import datetime

# Reddit markdown is used in this string
comment_reply = f"\n\n\n\n*This comment was left automatically (by a bot)." \
                f" If I don't get this right, don't get mad at me, I'm still learning!*\n\n" \
                f"[^(opt out)](https://www.reddit.com/r/wikipedia_answer_bot/comments/ozztfy/post_for_opting_out/)" \
                f" ^(|) [^(report/suggest)](https://www.reddit.com/r/wikipedia_answer_bot)" \
                f" ^(|) [^(GitHub)](https://github.com/TheBugYouCantFix/wiki-reddit-bot)"


def few_meanings_reply(text):
    return f'This word/phrase({text.strip()}) has a few different meanings.'


def festivity_reply():
    now = datetime.now()
    if datetime.date(now) == datetime(now.year, 12, 25).date():
        return "\n\nHappy Xmas to you! <3"
    elif datetime.date(now) == datetime(now.year, 12, 31).date():
        return "\n\nHappy New Year's Eve, Redditor!"
    elif datetime.date(now) == datetime(now.year, 1, 1).date():
        return "\n\nHappy New Year, Redditor!"

    return ""
