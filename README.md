# isfl-forum-scraper
ISFL forum scraper to identify missing TPE opportunities for a given list of users.

Hopefully the code body is self-explanatory, but here is a brief rundown anyway. Open in your favorite Python IDE--it will become abundantly clear if you open this file that I am an amateur programmer, so any funny business you do with the command line instead is up to you. I'm sure it's rife with bugs, so please tell me about them.

As inputs, MaxEarningClub.py takes three possible values (but usually two)--

* Threads - This should be the thread ID ('tid') of any thread that you want to scrape. It's the number after 'tid=' in any thread URL. If left blank, the script will still attempt to query the Weekly Training thread for the specified user/team.
* Users - A list of one or more users. The values should match the forum names exactly.
* Teams - A list of exactly one team. Required abbreviations are listed in the .py file. If a team is specified, all users associated with the team will be queried and returned.

Either Users or Teams is required, but probably not both. You can technically do both at once, but I wouldn't expect good results from the Weekly Training scraping if you start crossing the streams.

After the inputs are specified, run the script. In the event that you don't encounter an error, you should see a list of users and various thread names and URLs as outputs. These are threads that the user has not posted in (or, in the case of Weekly Training, has not posted in since Monday of the current week). Buy ice cream for users who return an empty set--that means they posted in every thread you specified.

If you've made it this far, you're probably Slate or mojo. Ping me on Discord at Maglubiyet#0479 if you have any issues or just want to talk. Good luck!
