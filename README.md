# Bot-Quora-Questions_Request
Simple bot that get all questions of a Quora User, then make some request to that questions


# DESCRIPTION

This script is a scraper that connects to a user's Quora page and collects all the questions that the user has made.

To do this, it uses the selenium library to control a web browser (in this case, Chrome) and navigate to the user's question page on Quora. It then uses a for loop to scroll down the page several times, loading more questions as it scrolls.

Once all the questions have been loaded, the script uses the BeautifulSoup library to parse the HTML code of the page and extract the questions. It then writes the questions to a text file called ask.txt.

The script also has a function called iniciar_sesion() that is used to log in to Quora and a function called cred_return() that reads the login credentials from a file called credentials.json and returns them as a dictionary.

It also has a function called add_question() that adds a new question to the ask.txt file and a function called get_question() that reads the first line of the ask.txt file and removes it from the file. Additionally, it has a function called return_questions() that uses all these functions to collect the user's questions and write them to the ask.txt file.

# EXAMPLE

