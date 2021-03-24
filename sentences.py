from datetime import datetime

comment_reply = f"\n\n\n\n*This comment was left automatically (by a bot). If something's " \
                f"wrong, please, report it in [my subreddit](https://www.reddit.com/r/wikipedia_answer_bot)." \
                f"*\n\n*Really hope this was " \
                f"useful and relevant :D*" + \
                f"\n\n*If I don't get this right, don't get mad at me, I'm still learning!*"


def festivity_reply():
    now = datetime.now()
    if datetime.date(now) == datetime(now.year, 12, 25).date():
        return "\n\nHappy Xmas to you! <3"
    elif datetime.date(now) == datetime(now.year, 12, 31).date():
        return "\n\nHappy New Year's Eve, Redditor!"
    elif datetime.date(now) == datetime(now.year, 1, 1).date():
        return "\n\nHappy New Year, Redditor!"
    else:
        return ""
