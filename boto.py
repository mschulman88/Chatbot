"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

username = ''
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

    # FIRST ROUND FUNCTION CHECK FOR USERNAME
    if counter_response == 1:
        if "I am" or "i am" in user_msg:
            index = user_msg_list.index('am')
            username = user_msg_list[index+1]
        elif "my name is" in user_msg:
            index = user_msg_list.index('is')
            username = user_msg_list[index+1]
        elif "call me" in user_msg:
            index = user_msg_list.index('me')
            username = user_msg_list[index+1]
        else:
            username = user_msg_list[0]
        return json.dumps({"animation": "excited", "msg": "Hi-diddly-ho "+username+
                                                          "! You seem like a great Neighbor-eeno!"})

    if "money" in user_msg:
        return json.dumps({"animation": "money", "msg": "MAKE THAT SKRILLA " + username})


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
