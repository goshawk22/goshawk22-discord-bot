import random
import string

# Setup Discord bot library
import discord
from discord.ext import commands

description = """A bot to define and give examples of a word"""
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", description=description, intents=intents)


# Setup random word library
from random_word import RandomWords
r = RandomWords()


# Setup urban dictionary api
import requests
urban_dictionary_api_url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
urban_dictionary_headers = {
    'x-rapidapi-key': "your-token",
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }

get_urban_querystring = lambda x:  {"term":x}

# Setup Word Dictionary API
word_dictionary_api_url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/"

get_word_querystring = lambda x:  {"entry":x}

word_dictionary_headers = {
    'x-rapidapi-host': "twinword-word-graph-dictionary.p.rapidapi.com",
    'x-rapidapi-key': "your_api"
    }


# Setup our own internal dictionary to avoid defining the same word with two different meanings and allow saving to disk
import json

try:
    with open('data/internal_dict.json', 'r') as fp:
        internal_dict = json.load(fp)
except:
    internal_dict = {}
    with open('data/internal_dict.json', 'w') as fp:
        json.dump(internal_dict, fp)

with open("data/rude-words.json", 'r') as fp:
    rude_words_list = json.load(fp)

# Checks to see if the definition of the random word exists in Urban Dictionary
def check_random_word(random_word):
    # Dummy value
    if random_word == None:
        return False
    
    # Check API
    response = requests.request("GET", word_dictionary_api_url, headers=word_dictionary_headers, params=get_word_querystring(random_word))

    # See if API returns valid definition
    if response.json()['result_msg'] == "Success":
        return True
    
    # No valid definitions were found
    return False

def get_random_word(word):
    if word in internal_dict:
        return internal_dict[word]
    
    a_random_word = None
    counter = 0
    while not check_random_word(a_random_word):
        a_random_word = r.get_random_word()
        if counter > 10:
            break

    internal_dict[word] = a_random_word

    with open('data/internal_dict.json', 'w') as fp:
        json.dump(internal_dict, fp)

    return internal_dict[word]

def check_rude_word(word):
    if word.lower() in rude_words_list:
        return True
    
    return False

# Start defining commands

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command()
async def define(ctx, word: str):
    """Gets the random definition a word"""
    lower_word = word.lower()
    if check_rude_word(lower_word):
        querystring = get_word_querystring(get_random_word(lower_word))
        response = requests.request("GET", word_dictionary_api_url, headers=word_dictionary_headers, params=querystring)
        print(get_random_word(lower_word))
        print(response.text)
        try:
            definition = response.json()['meaning']['noun'] + response.json()['meaning']['verb'] + response.json()['meaning']['adverb'] + response.json()['meaning']['adjective']
        
        except IndexError:
            print("Unknown word: ", word)
            result = "Sorry I don't know the definition of " + word
            await ctx.send(result)
            return


    else:
        querystring = get_urban_querystring(lower_word)
        response = requests.request("GET", urban_dictionary_api_url, headers=urban_dictionary_headers, params=querystring)

        try:
            definition = response.json()['list'][0]['definition'].replace("[", "").replace("]", "")

        except IndexError:
            print("Unknown word: ", word)
            result = "Sorry I don't know the definition of " + word
            await ctx.send(result)
            return

    result = word + ": " + definition
    await ctx.send(result)

'''
@bot.command()
async def example(ctx, word: str):
    """Gets examples a word in a sentence"""


    if check_rude_word(word):
        querystring = get_querystring(get_random_word(word))
        random_word = get_random_word(word)
    else:
        querystring = get_querystring(word)
        random_word = word
        
    response = requests.request("GET", urban_dictionary_api_url, headers=urban_dictionary_headers, params=querystring)
    try:
        examples = response.json()['list'][0]['example'].replace("[", "").replace("]", "").replace(random_word, word)
    except IndexError:
        print("Unknown word: ", word)
        result = "Sorry I don't know any examples of " + word
        await ctx.send(result)
        return

    result = "Examples of " + word + " in a sentence:\n" + examples
    await ctx.send(result)
'''

# Run the bot
bot.run("your_token")