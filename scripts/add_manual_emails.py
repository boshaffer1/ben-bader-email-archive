#!/usr/bin/env python3
"""
Add manually provided emails to the collection
"""

import json
from datetime import datetime

# Parse the emails from the text provided
manual_emails = [
    {
        "date": "11/22/2022",
        "subject": "Shalom",
        "body": """Yo first_name,

You really think I'm that dumb?

Come on.

I bet you're like "WTF did I just subscribe to?"

This kid has an email list and he doesn't even know how to personalize emails???

For the record Adam I do know how to personalize these things I just wanted to grab your attention.

So listen my friend.

I don't know when, why, or how you subscribed to this...

... and I don't know how often I'll be emailing you.

Every now and then I'll drink too much caffeine and spam your inbox at 1am, but most of the time you'll forget I even exist.

This is the part where I tell you to look out for my next email titled "my story" (intentionally in all lowercase so it's more *trendy*).

But fortunately for you, I won't be assaulting your inbox with a boring welcome series over the next 3 days.

You're welcome.

I will be sending you direct mail though.

You will receive a letter in the mail tomorrow titled "IRS: YOU'RE BEING AUDITED"

So if you don't mind just open that, write down your bank info and SSN on a handy dandy napkin and mail it back to me.

Thanks.

Sent from my Xbox 360.

Ben"""
    },
    {
        "date": "2/20/2023",
        "subject": "i got you breakfast Adam",
        "body": """It's 10:11 am, and I just sat down inside my favorite coffee spot in Miami.

The sweet lady who takes my order every day seemed kind of sad, so I bought her an iced latte.

I wasn't planning on writing an email to you right now, but it's a good excuse to postpone my long list of to-dos for the day.

There's a couple to my left, and this woman literally spent 4 minutes taking pictures of her acai bowl before she started eating it.

I know it was 4 minutes because I've been staring at my screen for the same amount of time, trying to decide where to take this email.

Yesterday I posted an Instagram pic, and someone commented, "need to obtain this lifestyle."

It's interesting how that works. Remember when you were chasing what you have right now?

But now it just feels so normal… there was no mystical point of arrival.

Before I turn this into some corny "be grateful" type email, the couple next to me got like 4 different entrees, and shorty just got up to order more.

Breakfast is a scam. Anyone that claims to be hungry before noon literally just has no self-control. They're just bored and would rather get up and waddle to the local woofery rather than do anything productive with their lives.

If you're reading this while taking a bite of your warm little pancake breakfast at 11 am, spit it out. And unsubscribe. You're not welcome here.

You can have coffee before noon. That's it.

Seriously fasting will help your focus so much. We've all been psyop'd by big breakfast into believing that breakfast is the most important meal of the day, and it's simply not true.

I think fat people should have to pay extra taxes too.

Oh my god, this bitch to the left is taking more pictures of their FIFTH entree.

Sorry, I'm gonna kill someone.

Imagine one day I'm running some really big public company, and someone just screenshots the last few lines of this email.

[CEO says, "fat people should pay extra taxes."] What a headline.

Ok, I've gotta get to work. I know this was schizo as fuck, so hopefully, I at least made you giggle on this beautiful Monday morning.

Have a great day (unless you ate breakfast),

Ben"""
    },
    {
        "date": "2/24/2023",
        "subject": "the most important questions of your life",
        "body": """Good morning Adam,

Have you ever wondered why there's a space between good and morning but no space in goodnight?

Me too.

Just another piece of mind-controlling government propaganda we've all been sold (lol).

If I see one more person using "the matrix is attacking" angle to sell some bullshit course, I think I'm gonna implode.

"The economy is collapsing! Your job doesn't care about you! The government is trying to kill you…

Aaaand if you want to protect yourself from these things, you need to build a social circle! Pick up my program, How to stop being a bubble-blowing clown-loving burger-flipping idiot loser, today."

Moving on…

I've been thinking about how all stages of our lives eventually become mostly-happy memories.

Even the darker stages.

When I look back on times when I was super stressed out or down bad, it's with nothing but gratitude.

The word gratitude has become so corny, but I can't think of a synonym, so you're gonna have to bear with me.

The things that once brought me turbulence all seem so minuscule now.

I encourage you to audit your life as well.

Most people just sleepwalk through this whole thing.

Pause to analyze the things that you're stressing about and understand that all things are temporary. Good or bad.

You'll probably look back at this period in your life with amusement for the person you once were and appreciation for who you've become.

I'm doing this right now.

A few moments ago, I had to google whether it was "bare with me" or "bear with me."

Apparently, it was the latter.

Now I know… silly old me.

Speaking of silliness…

A handful of my friends around my same age have gotten married, and some even popped out a kid or two.

In no way am I hating on them, but this is just an absolute mindfuck to me.

Like how are you possibly mature enough to know you want to spend the rest of your life with a 20ish-year-old girl?

What if she gets a wrinkle? Or clogs your toilet? Or even worse… you discover she likes pineapple on her pizza???

Maybe I'm missing something, but these are all dealbreakers for me.

And I don't think I'm anywhere close enough to figuring out this life thing the way I'd want to in order to feel ready to share a bed with someone for the rest of time.

I could be immature. Idk man.

If you're still here, hit reply and lmk what you think. How does one decide they're ready to get married and have kids?

And if girls don't poop, why do they spend so much time in the bathroom?

The world may never know.

See ya,

Ben"""
    },
    # Continue with remaining emails...
]

def parse_date_to_timestamp(date_str):
    """Convert date string to milliseconds timestamp"""
    try:
        # Try MM/DD/YYYY format
        if '/' in date_str:
            dt = datetime.strptime(date_str, "%m/%d/%Y")
        else:
            dt = datetime.strptime(date_str, "%m/%d/%Y")
        return str(int(dt.timestamp() * 1000))
    except:
        return "0"

def main():
    # Load existing emails
    with open('../data/raw_emails.json', 'r') as f:
        existing_emails = json.load(f)

    print(f"Found {len(existing_emails)} existing emails")

    # Convert manual emails to proper format
    new_emails = []
    for email in manual_emails:
        new_email = {
            "id": f"manual_{email['date'].replace('/', '_')}",
            "subject": email["subject"],
            "from": "Ben Bader <benbader0@gmail.com>",
            "date": email["date"],
            "timestamp": parse_date_to_timestamp(email["date"]),
            "body": email["body"],
            "snippet": email["body"][:200]
        }
        new_emails.append(new_email)

    # Combine and sort by timestamp
    all_emails = existing_emails + new_emails
    all_emails.sort(key=lambda x: int(x.get('timestamp', '0')))

    # Save back
    with open('../data/raw_emails.json', 'w') as f:
        json.dump(all_emails, f, indent=2, ensure_ascii=False)

    print(f"✓ Added {len(new_emails)} new emails")
    print(f"✓ Total emails now: {len(all_emails)}")

if __name__ == '__main__':
    main()
