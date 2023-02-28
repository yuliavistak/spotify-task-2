**Використані бібліотеки:**
flask
base64
json
pycountry
folium
dotenv
requests
geopy

* **spotify.py**
Виконане завдання 2
Програма дозволяє користувачу дізнатись інформацію про співака/групу (топ-10 найпопулярніших пісень артиста в США, список альбомів та ін)

![image](https://user-images.githubusercontent.com/116526148/221962734-6d341009-129c-4197-a200-349b8f701e4e.png)
Реалізовані функції:
* get_token
* get_auth_header
* search_for_artist
* get_songs_by_artist
* get_albums_by_artist
* search_song_in_album
* choice_1
* choice_2
* choice_3
* get_name
* check_input1
* check_input2
* main

* **spotify_map.py**
Програма дозволяє створити карту, у якій позначені країни, у яких доступна найпопулярніша виконавця, за ім'ям цього виконавця
Допоміжна програма для розробки застосунку

Реалізовані функції:
* get_token
* get_auth_header
* search_for_artist
* get_songs_by_artist
* get_available_markets_of_song
* convert_countries
* create_map
* main

* **spotify_app.py**
Програма створює веб-застосунок, використовуючи допоміжну програму, згадану вище
Виводяться перші 10 країн(якщо такі доступні), за потреби це можна змінити

![image](https://user-images.githubusercontent.com/116526148/221966265-83b24522-7001-493a-852a-731804efc2eb.png)
![image](https://user-images.githubusercontent.com/116526148/221966377-6e0a143e-540c-41f5-8f21-0af1ed0595bb.png)
![image](https://user-images.githubusercontent.com/116526148/221966522-7d8552b2-3dea-49b8-8a57-d61d80da3fe7.png)

Реалізовані функції:
* do_search
* entry_page


