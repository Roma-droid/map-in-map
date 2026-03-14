import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  \n/show_city [city_name] - показать город на карте\n/remember_city [city_name] - запомнить город\n/show_my_cities - показать все запомненные города\n/draw_distance [city1] [city2] - показать расстояние между городами")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    # Реализуй отрисовку города по запросу
    manager.create_graph(f"{city_name}.png", [city_name])
    with open(f"{city_name}.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo)



@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    # Реализуй отрисовку всех городов
    manager.create_graph(f"{message.chat.id}_cities.png", cities)
    with open(f"{message.chat.id}_cities.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['draw_distance'])
def handle_draw_distance(message):
    try:
        _, city1, city2 = message.text.split()
        success = manager.draw_distance(city1, city2)
        if success:
            with open("distance.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, f"Один из городов не найден. Проверьте названия: {city1}, {city2}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажи два города в формате: /draw_distance [city1] [city2]")

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()