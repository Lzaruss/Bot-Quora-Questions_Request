# Bot-Quora-Questions_Request
Simple bot that get all questions of a Quora User, then make some request to that questions


# DESCRIPTION

This script is a scraper that connects to a user's Quora page and collects all the questions that the user has made.

To do this, it uses the selenium library to control a web browser (in this case, Chrome) and navigate to the user's question page on Quora. It then uses a for loop to scroll down the page several times, loading more questions as it scrolls.

Once all the questions have been loaded, the script uses the BeautifulSoup library to parse the HTML code of the page and extract the questions. It then writes the questions to a text file called ask.txt.

The script also has a function called iniciar_sesion() that is used to log in to Quora and a function called cred_return() that reads the login credentials from a file called credentials.json and returns them as a dictionary.

It also has a function called add_question() that adds a new question to the ask.txt file and a function called get_question() that reads the first line of the ask.txt file and removes it from the file. Additionally, it has a function called return_questions() that uses all these functions to collect the user's questions and write them to the ask.txt file.

One for thing, if the script fail at login you must comment the line 23, that will be press the login button, but if there is a captcha it will give you error. In that case comment the line and add some time so that you can hit the captcha manually.

# EXAMPLE 1

command -> python .\test.py -f req -n 150 

In this case, I recommend use a number longer like 300 or higher, but the time will be more longer
In a case I made for myself, with a scroll number of 2000, the bot gave me 2400 questions.
By default the number will be 50 (if you dont put the arg -n)

https://user-images.githubusercontent.com/104428151/209848955-bebcec89-db29-44aa-9762-60e73273ff5e.mp4

# EXAMPLE 2

command -> python .\test.py -f send -n 50

In this case, is better put a number lower like 50, the max i think is 110 approximately, because Quora requests are limited.
By default the number will be 20 (if you dont put the arg -n)

https://user-images.githubusercontent.com/104428151/209850939-02fbb605-9e55-4d1e-a1c1-3e736e3fa229.mp4
