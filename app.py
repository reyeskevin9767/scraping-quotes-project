
# * Import Modules
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from termcolor import colored
from colorama import init
init()

# * Using BeautifulSoup
BASE_URL = 'http://quotes.toscrape.com'

# * Scrape Quotes from website


def scrape_quotes():
    all_quotes = []
    url = "/page/1"

    # Loop through the each page of the website
    while url:
        res = requests.get(f"{BASE_URL}{url}")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.findAll(class_="quote")

        # For each quote, find the text, author , and link to bio
        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")['href']
            })

        # Check to see if there are any remaining pages
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")['href'] if next_btn else None
        sleep(2)
    return all_quotes


# Guessing the quote
def start_game(quotes):

    # Randomly select a quote from list
    quote = choice(quotes)
    remaining_guesses = 4

    print(colored("Here's a quote: ", color='green'))
    print(colored(quote["text"], color='grey'))
    guess = ''

    # Loop breaks when guess equals author name or remaining guesses reaches zero
    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:

        print(colored(
            f"\nWho said this quote? Guesses remaining: {remaining_guesses}.", color='cyan'))
        guess = input()

        # First Hint
        if guess.lower() == quote['author'].lower():
            print(colored("\nYou Got It Right\n", color="green"))
            break
        remaining_guesses -= 1

        # Second Hint
        if remaining_guesses == 3:

            # Scrape the website with the bio-link include to get more info on author
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(
                colored(f"\nHere's a hint: The author was born on {birth_date} {birth_place}", color='grey'))

        # Third Hint
        elif remaining_guesses == 2:
            print(colored(
                f"\nHere's a hint: The author's first name {quote['author'][0]}", color="grey"))

        # Fourth Hint
        elif remaining_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(colored(
                f"\nHere's a hint: The author's last name {last_initial}", color="grey"))

        # No More Hints Left
        else:
            print(colored(
                f"\nSorry you ran out of guesses. The answer was {quote['author']}\n", color='red'))

    # Ask the player if they want to play again
    again = ''
    while again not in ('y', 'yes', 'n', 'no'):
        print(colored("Would you like to play again (y/n)"))
        again = input()
    if again.lower() in ('yes', 'y'):
        return start_game(quotes)
    else:
        print(colored("\nGame, Shutting Down", color="cyan"))


quotes = scrape_quotes()
start_game(quotes)
