<div>

[![Status](https://img.shields.io/badge/status-active-success.svg)]() [![GitHub Issues](https://img.shields.io/github/issues/lk2322/Project_YANDEX)](https://github.com/lk2322/Project_YANDEX/issues) ![Lines of code](https://img.shields.io/tokei/lines/github/TheBugYouCantFix/wiki-reddit-bot)

</div>


# wiki-reddit-bot
**Public repo of  u/wikipedia_answer_bot**
<br />


## Tools 

**Language:** *Python*

**Libraries:** 
- [praw](https://praw.readthedocs.io/en/latest/) (Reddit [API](https://en.wikipedia.org/wiki/API "API"))
- [mediawikiapi](https://pypi.org/project/mediawikiapi/") (Wikipedia [API](https://en.wikipedia.org/wiki/API "API"))
- [tenacity](https://github.com/jd/tenacity "tenacity")
<br />

## How it works
##### 1. It looks through all the new comments on [Reddit](https://www.reddit.com/ "Reddit") in real time using praw.

##### 2. Checks whether a comment contains a question written with one of the following patterns:
- What is / What's / What are X?
- Who is/ Who's / Who are X?
- What does X mean?

X is a word / phrase which meanig the comment's author wants to know

**Note**: *If you want the bot to reply to your question, there is no need to write its name, use some specific charcter, etc. You should only ask a question the way it matches these patterns above*
*P.S. I know that the fact you don't have to summon it is bad. But it is also good xD :)*

##### 3. Looks for an approptiate article in Wikipedia
##### 4. Replies with a definition found in the article (if the article itself was found)

#### **Here is an example of the bot's reply:**
![](https://i.imgur.com/cXPkFhD.jpeg)

**Note:** *There may be not any artcles matching some exact word or the Wikipedia API is not able to find them for some reason. If this happens, you will just not get a reply.*

*Also, some words may have a few meanings.  In this case, the bot will respond to your comment with a link leading to other links, each of those will contain every separate definiton of an ambiguos word.*
![](https://i.imgur.com/arL1r7a.jpeg)
<br />


## Possible irrelevant answers
You may get an answer which is completely inappropriate to the conversation. This is because the bot can not understand a whole point of the specific comment or even dialog, unfortunately ):
<br />


## Additional features
1. It writes a felicitation in the end of the comment if it is one of the following holidays today:
    - Christamas (Catholic)
    - New Year's Eve
    - New Year
    - Halloween

2. There is a one joke I don't want to reveal, hehe (you can actually find it in the code)


## Hosting info:
**Hosted on:** *Heroku*

**Running since:** *October, 2020* (I was using another private repo while hosting it)

**Stopped running on:** *March 24, 2021* (free hosting time has ended T_T)

P.S. [@federicotorrielli](https://github.com/federicotorrielli) has been hosting it for a few months and took part in the bot's development
<br />


## Links
Bot: https://www.reddit.com/user/wikipedia_answer_bot

Bot's subreddit: https://www.reddit.com/r/wikipedia_answer_bot
<br />


## Conclusion
Thank you for visiting this repo! Hopefully you liked it :)

Always feel free to contribute. Let's make this open source world better ;)


