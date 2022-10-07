# object-snake
Объектно-ориентированная змейка на `pygame`.

## Особенности
* Игра написана в стиле ООП, логика игры максимально отделена от "графического движка":
* * Класс `Engine` отвечает за вывод картинки на экран и обработку ввода;
* * В классе `Game` прописана игровая логика с использованием объектов `Board`, `Snake`, `Block`, `Highscores`.
* Реализовано сохранение статистики игр в классе `Highscores` и её загрузка при запуске игры при помощи модуля
`pickle`.

## Установка на MacOS X / Linux
```bash
$ cd /usr/projects
$ git clone https://github.com/hazadus/object-snake
$ virtualenv object-snake
$ cd ./object-snake
$ source bin/activate
$ pip install -r requirements.txt
```
При установке на Raspbian, была встречена такая ошибка:
`NotImplementedError: font module not available (ImportError: libSDL2_ttf-2.0.so.0: cannot open shared object file: 
No such file or directory)`.
Решилось всё установкой следующего пакета:
```bash
$ sudo apt-get install python3-sdl2
```

## Запуск
```bash
$ cd /usr/projects/object-snake
$ source bin/activate
$ python ./object-snake.py
```

## Прочее
При отсутствии в системе шрифтов, названия которых указаны в начале метода `Engine.draw_frame()` они будут заменены на
другой (скорее всего, корявый) шрифт. Замените названия шрифтов на имеющиеся в системе по своему предпочтению!
```python
def draw_frame(self):
    font_logo_name = 'PT Mono'
    font_info_line_name = 'PT Mono'
    font_paused_name = 'Chalkboard'
    ...
```

## References
- Inspired by: [Создаём первую игру на Python и Pygame](https://skillbox.ru/media/code/sozdayem-pervuyu-igru-na-python-i-pygame/)