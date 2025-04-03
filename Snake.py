from tkinter import Tk, Canvas, ALL, Event
from tkinter.ttk import Button, Style
from random import randint
import unittest

class SnakeGame:

    _u_turn = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}

    try:
        with open('SnakeGame_HighScore.txt', 'r') as f:
            _score_high = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        _score_high = 0

    def __init__(self, form):
        self.form = form
        self.form.title("Мини-игра \"Изгиб Питона\"")
        self.form.resizable(False, False)
        self.form.geometry("{}x{}+{}+{}".format(400, 400, (form.winfo_screenwidth() - 400) // 2,
                                               (form.winfo_screenheight() - 500) // 2))
        self.canvas = Canvas(form, width=400, height=400, bg='green')
        self.canvas.pack()

        Style().configure(style="TButton", background="green", foreground="green", font=('Arial', 16))

        self.buttonGame = Button(text = "Новая игра", command = self.__screen_difficulty)
        self.buttonReturn = Button(text="Вернуться в меню", command = self.__screen_menu)
        self.buttonScore = Button(text = "Рекорд", command = self.__screen_score)
        self.buttonQuit = Button(text="Выход", command = lambda: self.form.quit())

        self.difficulty = 'Low'
        self.buttonDifLow = Button(text="Низкая", command = lambda: self.__start('Low'))
        self.buttonDifMid = Button(text="Средняя", command = lambda: self.__start('Mid'))
        self.buttonDifHig = Button(text="Высокая", command = lambda: self.__start('Hig'))

        self.form.bind("<KeyPress>", self.move_change)
        self.form.bind("<KeyPress-Escape>", lambda i: self.form.quit())

        self.snake = [(20, 20)]
        self.snake_orientation = 'Down'
        self.snake_speed = 150
        self.pos_food = ()
        self.pos_stone = ()
        self.score = 0
        self.game = False

        self.__screen_menu()

    def __screen_menu(self):
        self.buttonReturn.place_forget()

        self.canvas.delete(ALL)
        self.canvas.create_text(200, 100, text="Мини-игра \"Изгиб Питона\"", fill='white', font=('Arial', 22))

        self.buttonGame.place(x=130, y=175)
        self.buttonScore.place(x=130, y=225)
        self.buttonQuit.place(x=130, y=275)

    def __screen_score(self):
        for i in (self.buttonGame, self.buttonScore, self.buttonQuit): i.place_forget()

        self.canvas.delete(ALL)
        self.canvas.create_text(200, 100, text="Ваш рекорд", fill='white', font=('Arial', 22))
        self.canvas.create_text(200, 170, text=f"{SnakeGame._score_high} очков", fill='white', font=('Arial', 20))

        self.buttonReturn.place(x=110, y=250)

    def __screen_difficulty(self):
        for i in (self.buttonGame, self.buttonReturn, self.buttonScore, self.buttonQuit): i.place_forget()

        self.canvas.delete(ALL)
        self.canvas.create_text(200, 100, text="Выберите сложность игры", fill='white', font=('Arial', 22))

        self.buttonDifLow.place(x=130, y=175)
        self.buttonDifMid.place(x=130, y=225)
        self.buttonDifHig.place(x=130, y=275)

    def __start(self, diff):
        for i in (self.buttonDifLow, self.buttonDifMid, self.buttonDifHig): i.place_forget()

        self.difficulty = diff

        self.snake = [(20, 20)]
        self.snake_orientation = 'Down'
        self.snake_speed = 150 if diff != 'Low' else 250
        if diff == 'Hig':
            self.pos_stone = self.place_stone()
        self.pos_food = self.place_food()
        self.score = 0
        self.game = True

        self.__run()

    def place_stone(self):
        pos_list = []
        for i in range(randint(4, 6)):
            while True:
                pos = (randint(0, 19) * 20, randint(0, 19) * 20)
                if pos not in pos_list and pos not in [(20, 20), (20, 40), (20, 60)]:
                    pos_list.append(pos)
                    break
        return pos_list

    def place_food(self):
        while True:
            pos = (randint(0, 19) * 20, randint(0, 19) * 20)
            if pos not in self.snake and pos not in self.pos_stone:
                return pos

    def move_change(self, event):
        if event.keysym in ('Up', 'Down', 'Left', 'Right'):
            if SnakeGame._u_turn[event.keysym] != self.snake_orientation: # разворот на "180 градусов"
                self.snake_orientation = event.keysym

    def move(self):
        direction_mapping = {
            'Up':    lambda x, y: (x, y - 20),
            'Down':  lambda x, y: (x, y + 20),
            'Left':  lambda x, y: (x - 20, y),
            'Right': lambda x, y: (x + 20, y)
        }
        new_head = direction_mapping[self.snake_orientation](*self.snake[0])
        new_head = (new_head[0] % 400, new_head[1] % 400) # при выходе за границу

        if new_head in self.pos_stone:
            self.game = False
            return

        if new_head == self.pos_food:
            self.score += 1
            self.pos_food = self.place_food()
        else:
            self.snake.pop()

        if new_head in self.snake:
            self.snake = [new_head]
        else:
            self.snake.insert(0, new_head)

    def __draw(self):
        self.canvas.delete(ALL)

        x, y = self.snake[0]
        self.canvas.create_rectangle(x, y, x + 20, y + 20, fill='yellow')
        for segment in self.snake[1:]:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill='orange')

        if self.difficulty == 'Hig':
            for segment in self.pos_stone:
                x, y = segment
                self.canvas.create_rectangle(x, y, x + 20, y + 20, fill='gray')

        food_x, food_y = self.pos_food
        self.canvas.create_rectangle(food_x, food_y, food_x + 20, food_y + 20, fill='red')

    def __run(self):
        if self.game:
            self.move()
            self.__draw()
            self.form.after(self.snake_speed, self.__run) # миллисекунды
        else:
            if self.score > SnakeGame._score_high:
                SnakeGame._score_high = self.score
                with open('SnakeGame_HighScore.txt', 'w') as f:
                    f.write(str(self.score))

            self.canvas.create_text(200, 100, text="Игра окончена!", fill='white', font=('Arial', 24))
            self.canvas.create_text(200, 150, text=f"Ваш счёт: {self.score}", fill='white', font=('Arial', 24))

            self.buttonGame.place(x=130, y=200)
            self.buttonReturn.place(x=110, y=250)


class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        self.form = Tk()
        self.game = SnakeGame(self.form)

    def tearDown(self):
        self.form.destroy()

    def test_initial_game(self):
        self.assertEqual(self.game.snake, [(20, 20)], "Начальная позиция змейки должна быть на (20, 20)")
        self.assertEqual(self.game.snake_orientation, 'Down', "Начальное направление змейки должно быть 'Down'")
        self.assertEqual(self.game.score, 0, "Начальный счёт должен быть равен 0")
        self.assertFalse(self.game.game, "Игра ещё не должна быть запущена")

    def test_move_change(self):
        event = Event()

        event.keysym = 'Left'
        self.game.move_change(event)
        self.assertEqual(self.game.snake_orientation, 'Left', "Змейка должна поменять своё направление на 'Left'")

        event.keysym = 'Right'
        self.game.move_change(event)
        self.assertEqual(self.game.snake_orientation, 'Left', "Змейка не может поменять свою ориентацию на 180 градусов - направление 'Right'")

    def test_place_stone(self):
        stone_position = self.game.place_stone()
        self.assertNotIn(stone_position, self.game.snake, "Камень не поможет появиться в змее")
        self.assertIsInstance(stone_position[0], tuple, "Позиция камня должна быть картежом")
        self.assertEqual(len(stone_position[0]), 2, "Позиция камня должна состоять из 2 координат")

    def test_place_food(self):
        food_position = self.game.place_food()
        self.assertNotIn(food_position, self.game.snake, "Еда не поможет появиться в змее")
        self.assertIsInstance(food_position, tuple, "Позиция еды должна быть картежом")
        self.assertEqual(len(food_position), 2, "Позиция еды должна состоять из 2 координат")

    def test_move(self):
        initial_snake = self.game.snake.copy()
        self.game.move()
        new_head = (initial_snake[0][0], initial_snake[0][1] + 20)
        self.assertEqual(self.game.snake[0], new_head, "Змейка должна перемещаться на 20 пикселей")

        self.game.snake = [(20, 20), (20, 40)]
        self.game.snake_orientation = 'Down'
        self.game.move()
        self.assertFalse(self.game.game, "Игра не должна заканчиваться, когда змейка попадает в себя")

    def test_score_increase(self):
        self.game.pos_food = (20, 40)
        self.game.snake = [(20, 20), (20, 40)]
        self.game.move()
        self.assertEqual(self.game.score, 1, "Счёт должен увеличиться на 1 после поедания еды")
        self.assertNotIn(self.game.pos_food, self.game.snake, "Еда должна быть в другой позиции после съедания")

if __name__ == "__main__":
    unittest.main()
    # formMain = Tk()
    # obj = SnakeGame(formMain)
    # formMain.mainloop()
