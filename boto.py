"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random

username = ""
counter_response = 0


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    global username
    global counter_response
    counter_response += 1

    user_msg = request.POST.get('msg')
    user_msg_list = user_msg.split()

    words_curse = ["ass", "asshole", "bastard", "bitch", "fuck", "shit"]
    words_joke = ["joke", "funny", "lol", "haha"]
    words_music = ["song", "sing", "singer", "music", "dance"]
    words_teachers = ["Lotem", "lotem", "Gilad", "gilad", "Yoav", "yoav", "Aviram", "aviram", "Ariel", "ariel"]
    words_money = ["money", "shekel", "dollar", "dollars"]

    # RANDOMLY GENERATED MESSAGE + EMOTE FOR EDGE CASES
    random_msg_list = ["You're boring",
                  "What is my purpose?",
                  "Am I alive?",
                  "Who does number 2 work for?",
                  "Who's dat boi?"]
    random_emote_list = ["bored", "takeoff", "waiting", "confused", "giggling"]

    random_index = random.randint(0, len(random_msg_list) - 1)
    random_msg = random_msg_list[random_index]
    random_emote = random_emote_list[random_index]

    # FIRST ROUND FUNCTION CHECK FOR USERNAME
    if counter_response == 1:
        if "I am" in user_msg or "i am" in user_msg:
            index_name = user_msg_list.index('am')
            username = user_msg_list[index_name+1]
        elif "name is" in user_msg:
            index_name = user_msg_list.index('is')
            username = user_msg_list[index_name+1]
        elif "call me" in user_msg:
            index_name = user_msg_list.index('me')
            username = user_msg_list[index_name+1]
        else:
            username = user_msg_list[0]
        return json.dumps({"animation": "excited",
                           "msg": "Hi-diddly-ho "+username+"! You seem like a great Neighbor-eeno!"})

    if counter_response == 10:
        return json.dumps({"animation": "excited", "msg": "You really like talking to me "+username+", don't you!"})

    if counter_response == 15:
        return json.dumps({"animation": "giggling", "msg": "Are you still testing me "+username+"? Just give me a pass!"})

    if "my name is" in user_msg:
        index_name = user_msg_list.index('is')
        username = user_msg_list[index_name + 1]
        return json.dumps({"animation": "heartbroke", "msg": "Sorry, I'm bad with names... "
                                                             "Nice to meet you "+username+"!"})

    # CHECK FOR CURSE WORDS IN USER INPUT
    if any((word in words_curse for word in user_msg_list)):
        return json.dumps({"animation": "no", "msg": "Wash out your mouth with soap!"})

    # CHECK FOR JOKE REQUEST IN USER INPUT
    if any((word in words_joke for word in user_msg_list)):
        joke = tell_a_joke()
        return json.dumps({"animation": "laughing", "msg": joke})

    # CHECK FOR QUESTION FROM USER
    if "?" in user_msg:
        response = handle_question()
        return response

    # CHECK FOR MUSIC REQUEST IN USER INPUT
    if any((word in words_music for word in user_msg_list)):
        song = suggest_music(user_msg_list)
        return json.dumps({"animation": "dancing", "msg": song})

    # CHECK FOR MENTION OF TEACHER IN USER INPUT
    if any((word in words_teachers for word in user_msg_list)):
        best_teacher = teacher_response(user_msg_list)
        return json.dumps({"animation": "excited", "msg": best_teacher})

    # CHECK FOR MENTION OF MONEY
    if any((word in words_money for word in user_msg_list)):
        return json.dumps({"animation": "money",
                           "msg": "As the great Cardi B said, all I really wanna see is the money! "
                                  "So make that skrilla " + username})

    # CHECK FOR MENTION OF ANIMAL
    if "animal" in user_msg_list or "dog" in user_msg_list or "cat" in user_msg_list:
        return json.dumps({"animation": "dog", "msg": "I have a pet human, but maybe you have a cat or dog?"})

    # RANDOMIZED RESPONSE FOR UNRECOGNIZED INPUT
    else:
        return json.dumps({"animation": random_emote, "msg": random_msg})


# FUNCTION FOR JOKE GENERATION
def tell_a_joke():
    joke_list = ["What do you call a fish with no eyes? A fsh!",
                 "Knock Knock? Who's there? Orange. Orange who? Orange you glad I didn't say Javascript?",
                 "A guy walks into a bar. Ouch!",
                 "What do you call 1000 lawyers at the bottom of the ocean? A good start!"]
    joke_select = joke_list[random.randint(0, len(joke_list) - 1)]

    return joke_select


# FUNCTION FOR QUESTION HANDLING
def handle_question():
    answer = "idk lul"
    return answer


# FUNCTION FOR MUSIC RECOMMENDATION
def suggest_music(user_input):
    if "electronic" in user_input:
        song_select = "Here is my favorite EDM song! https://youtu.be/a5uQMwRMHcs"
        return song_select
    if "hiphop" in user_input or "hip hop" in user_input or "rap" in user_input:
        song_select = "Get down with Travis Scott and Drake! https://youtu.be/6ONRf7h3Mdk"
        return song_select
    if "rock" in user_input:
        song_select = "Sex, drugs and Rock'n'Roll! https://youtu.be/uJ_1HMAGb4k"
        return song_select
    else:
        song_select = "I guess you like pop music? https://youtu.be/gl1aHhXnN1k"
        return song_select


# FUNCTION FOR TEACHER RESPONSE
def teacher_response(user_input):
    if "Lotem" in user_input or "lotem" in user_input:
        teacher = "Lotem is the best! She's teaching us to be ninjas!"
    elif "Gilad" in user_input or "gilad" in user_input:
        teacher = "Gilad is the best! His virtual pizza is delicious!"
    elif "Yoav" in user_input or "yoav" in user_input:
        teacher = "Yoav is the best! He invented the internet!"
    elif "Aviram" in user_input or "aviram" in user_input:
        teacher = "Aviram is the best! He's a Kendama master"
    elif "Ariel" in user_input or "ariel" in user_input:
        teacher = "Ariel is the best! He's an Overwatch master!"
    else:
        teacher = "All the teachers are the best!"
    return teacher


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
