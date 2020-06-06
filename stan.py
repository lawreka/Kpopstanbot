import config
import json
import requests
import time

TELEGRAMTOKEN = config.telegram_token
TELEGRAMURL = "https://api.telegram.org/bot{}/".format(TELEGRAMTOKEN)
GIPHYTOKEN = config.giphy_token
GIPHYURL = "http://api.giphy.com/v1/gifs/random?tag=kpop&api_key={}".format(GIPHYTOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates():
    url = TELEGRAMURL + "getUpdates?timeout=100"
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_gif(link, chat_id):
    url = TELEGRAMURL + "sendAnimation?animation={}&chat_id={}".format(link, chat_id)
    print(url)
    get_url(url)

def get_random_kpop():
    gifcontent = get_json_from_url(GIPHYURL)
    link = gifcontent['data']['images']['downsized']['url']
    return link

def spam(text, chat):
    while True:
        updates = get_updates()
        text, chat = get_last_chat_id_and_text(updates)
        print(text, chat)
        if text != 'STAN JUNGKOOK':
            kpopgif = get_random_kpop()
            try:
                send_gif(kpopgif, chat)
            except Exception as e:
                print(e)
        else:
            print('done for now :3')
            break


def main():
    print('alive')
    last_textchat = (None, None)
    while True:
        updates = get_updates()
        text, chat = get_last_chat_id_and_text(updates)
        print(text, chat)
        if (text, chat) != last_textchat:
            if text == 'ARMY':
                print('kpop stan active')
                spam(text, chat)
            last_textchat = (text, chat)
        time.sleep(0.5)
        

if __name__ == '__main__':
    main()
