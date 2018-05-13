import requests
from io import BytesIO
import telebot
import conf


header = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

bot = telebot.TeleBot(conf.tk)
main_page = r'https://www.artstation.com/{img_t}'
search_url = r'https://www.artstation.com/search/projects.json?direction=desc&order=published_at&page={pages}&q={tag}&show_pro_first=true'
images_url = r'https://www.artstation.com/projects/{img}.json'



def get_img(img):
    img = requests.get(img)
    file = BytesIO(img.content)
    return file

def find_tag(tag,page,num = None):
    req = requests.get(search_url.format(pages = page,tag = tag)).json()
    count = 0
    for i in req['data'][:num]:
        image_link = requests.get(images_url.format(img = i['hash_id'])).json()
        tag_images = main_page.format(img_t = i['hash_id'])
        print(tag_images)
        print(image_link['assets'][0]['image_url'])
        count+=1
    if count <= 1:
        pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello this is find ArtStation bot, write the /find and you can find the tag from site ArtStation")


@bot.message_handler(commands=['find'])
def find_tag(message):
    bot.send_message(message.chat.id, "Send me the message like this:\n"
                                      "TAG PAGE COUNT_OF_IMAGE\n"
                                      "EXAMPLE:\n"
                                      "anime 2 10")


            # soup = BeautifulSoup(req.text, "lxml")
        # img_tags = soup.find_all('img')
        #
        # urls = [img['src'] for img in img_tags]
        # print(urls)
        # print(tags)
        # print(self.search_url.format(tag=tag))
        # print(soup.prettify())

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    text = m.text.split(' ')
    if len(text) < 3:
        bot.send_message(m.chat.id, 'You should write three parameters:\n'
                                    "TAG PAGE COUNT_OF_IMAGE\n"
                                    "EXAMPLE:\n"
                                    "anime 2 10"
                         )
    else:
        tag, page, num = text

        if page.isdigit() and num.isdigit():
            req = requests.get(search_url.format(pages=int(page), tag=tag)).json()
            count = 0
            bot.send_message(m.chat.id,'Okay, one moment please!!!')
            print(tag,page,num)
            for i in req['data'][:int(num)]:
                image_link = requests.get(images_url.format(img=i['hash_id'])).json()['assets'][0]['image_url']
                tag_images = main_page.format(img_t=i['hash_id'])
                print(image_link)
                img = get_img(image_link)
                bot.send_photo(m.chat.id,img,caption=tag_images)
                count += 1
            if count <= 0:
                bot.send_message(m.chat.id, "Sorry but I don't found any of this tag")
        else:
            bot.send_message(m.chat.id, "Invalid page or Count of images")


    # this is the standard reply to a normal message
    # bot.send_message(m.chat.id,'Nya')


if __name__ == '__main__':

    bot.polling(none_stop=True)

