
from fastapi import APIRouter, Query
from datetime import datetime
from sqlalchemy import or_
import random



router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
    tags=["Api"]
)


@router.get("/", status_code=200)
async def root():
    return {"message": "Welcome to API"}

@router.get("/getMeme", status_code=200)
def getMeme():
    memes =  [
        {
        "title": "Made a meal out of it",
        "url": "https://i.redd.it/84uhwvgmmrsb1.gif",
        "preview":
            "https://preview.redd.it/84uhwvgmmrsb1.gif?width=640&crop=smart&format=png8&s=c12d2e21057a6e7f9868762943c093ea17eba207"
        },
        {
        "title": "How does it work though",
        "url": "https://www.reddit.com/r/memes/comments/16dm9kw/how_does_it_work_though/",
        "preview": 
            "https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Fiqmxp9o1k3nb1.jpg"
        },
        {
        "title": "Check Engine Light",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-27-6328530526689__700.jpg"
        },
        {
        "title": "Sad meme",
        "url": "",
        "preview": "https://www.nature.com/articles/s41599-022-01381-4/figures/1"
        },
        {
        "title": "Something Sweet",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-7-63282ec36969e__700.jpg"
        },
        {
        "title": "In the mirror",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-15-63283925da269__700.jpg"
        },
        {
        "title": "Please no",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-71-6329c64cc5683__700.jpg"
        },
        {
        "title": "Facetime",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-1-632827c66b20c__700.jpg"
        },
        {
        "title": "Clowns",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-3-63282981225d3__700.jpg"
        },
        {
        "title": "wholesome",
        "url": "https://hehimhismedia.com/20-never-seen-mental-health-memes-a-review-of-mental-health-and-memes/",
        "preview": "https://hehimhismedia.com/wp-content/uploads/2022/01/memes-to-cope.jpg"
        },
        {
        "title": "its all together",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://i.imgflip.com/70fk01.jpg"
        },
        {
        "title": "Days off",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-72-6329c6ae9beb9__700.jpg"
        },
        {
        "title": "Drunk",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-74-6329c7917f219__700.jpg"
        },
        {
        "title": "Friendship",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-74-6329c7917f219__700.jpg"
        },
        {
        "title": "Lecture",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-23-63281fd2f1184__700.jpg"
        },
        {
        "title": "Dont run away from your problems",
        "url": "https://the-breakdown.co.uk/mental-health-memes-youll-relate-to/",
        "preview": "https://the-breakdown.co.uk/wp-content/uploads/2020/12/D5lcE5hWkAUeRFS-768x675.jpeg"
        },
        {
        "title": "youre doing great",
        "url": "https://the-breakdown.co.uk/mental-health-memes-youll-relate-to/",
        "preview": "https://the-breakdown.co.uk/wp-content/uploads/2020/12/Cute-and-Positive-Affirmations-Super-Cute-Kawaii.gif"
        },
        {
        "title": "reality bites",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://i.imgflip.com/53gfqu.jpg"
        },
        {
        "title": "Still Up",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-5-63282b231d997__700.jpg"
        },
        {
        "title": "Ignoring call",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-28-63281fda93e4c__700.jpg"
        },
        {
        "title": "Not Enough Sleep",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-34-63281fe6a43d5__700.jpg"
        },
        {
        "title": "Alarm",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-4-63282a68bb4b2__700.jpg"
        },
        {
        "title": "Me at 3AM",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-25-63285008e84cd__700.jpg"
        },
        {
        "title": "Treat yo self",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-11-632858291987c__700.jpg"
        },
        {
        "title": "45 Seconds",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-weneedfun-best-45-seconds-of-my-life-min.jpg"
        },
        {
        "title": "Haha. I'm ok",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-haha-im-okay-min.png"
        },
        {
        "title": "Wake up",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-2-6328287127973__700.jpg"
        },
        {
        "title": "Laugh",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-18-632849496a255__700.jpg"
        },
        {
        "title": "Need Sleep",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-28-6328537ce55e1__700.jpg"
        },
        {
        "title": "Scary Boss",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-55-6328200ddb301__700.jpg"
        },
        {
        "title": "Ugly",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-9-6328318479d81__700.jpg"
        },
        {
        "title": "Food Coma",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-12-63281fbd38b0e__700.jpg"
        },
        {
        "title": "Not sure if its tuesday or....",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-not-sure-if-its-tuesday-or-min.png"
        },
        {
        "title": "at least im professional",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-at-least-im-professional-min.png"
        },
        {
        "title": "Remember ?",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-remember.png"
        },
        {
        "title": "Pushing Through",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-107-63282094200bf__700.jpg"
        },
        {
        "title": "Drinking Water",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-10-63283203a0be7__700.jpg"
        },
        {
        "title": "In it together",
        "url": "https://www.boredpanda.com/relatable-funny-memes/?utm_source=google&utm_medium=organic&utm_campaign=organic",
        "preview": "https://www.boredpanda.com/blog/wp-content/uploads/2022/09/relatable-funny-memes-26-632851bc6c00f__700.jpg"
        },
        {
        "title": "please drop the call already",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-theawesomedaily-please-drop-the-call-already-min.jpg"
        },
        {
        "title": "My guardian angel be like",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-imgflip-my-guardian-angel-be-like-min.jpg"
        },
        {
        "title": "I'm fine. Totally fine!",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-sayingimages-im-fine-totally-fine-min.jpg"
        },
        {
        "title": "Oh what a long list",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-oh-what-a-long-list-min.png"
        },
        {
        "title": "Come on, fight me",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-come-on-fight-me-min.png"
        },
        {
        "title": "Me, thinking about life",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-me-thinking-about-life-min.png"
        },
        {
        "title": "Hello there, soulmate",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-yourtango-hello-there-soulmate-min.png"
        },
        {
        "title": "Lets just probably enjoy it",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-solifequotes-lets-just-probably-enjoy-it-min.png"
        },
        {
        "title": "Priorities!",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-onlytwitterpics-priorities-min.jpg"
        },
        {
        "title": "I was kidding.",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-lovethispic-i-was-kidding-min.jpg"
        },
        {
        "title": "My life isn't important",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-instoremag-my-life-is-not-important-maam-min-768x470.jpg"
        },
        {
        "title": "Someone feed my mind, please",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://www.happierhuman.com/wp-content/uploads/2022/01/memes-about-life-curiouskeeda-someone-feed-my-mind-please-min-768x768.jpg"
        },
        {
        "title": "Life vs. you",
        "url": "https://www.happierhuman.com/memes-life/",
        "preview": "https://imgflip.com/gif/7wkl4t"
        }
        ]
    random_meme = random.choice(memes)
    return(random_meme)








