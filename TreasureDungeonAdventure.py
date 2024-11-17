import random
import time
import threading

WELCOME_MESS = '''=== Добро пожаловать в "Подземелье приключений"! ===\n
Ты — отважный искатель сокровищ, готовый спуститься в мрачные глубины. 
В комнатах подземелья тебя ждут драгоценности, смертельные ловушки и опасные монстры. 
Твоя цель — собрать как можно больше сокровищ и выйти, сохранив жизни.\n
Готов испытать свою смелость?\n
Удачи, герой!\n
Нажми клавишу "y", чтобы начать игру, "n" для выхода или "i" для прочтения инструкции'''

BYE_MESS = '''=== Спасибо за игру в "Подземелье приключений"! === \n
Надеемся, ты получил море впечатлений и адреналина. 
Возвращайся за новыми сокровищами и испытаниями в любое время!\n
До новых встреч, герой! \n'''

INSTRUCTION_MESS = '''=== Как играть: ===\n
Используй клавиши для перемещения:\n
y - чтобы продолжить
n - чтобы закончить
Нажми i, чтобы вывести эту инструкцию на экран в любой момент.\n
=== Описание комнат: ===\n
Сокровищница: приносит дополнительные очки.\n
Ловушка: теряешь одну жизнь.\n
Монстр: есть шанс победить и остаться целым или потерять одну жизнь.\n
=== Цель игры: ===\n
Cобрать 5 очков, не потеряв все свои жизни. Каждый уровень состоит из нескольких комнатных испытаний. Пройди их все, чтобы продолжить приключение!\n '''

BAD_MOVE_MESS = 'Неверная команда! Используйте только y, n во время прохождения, e для выхода из игры или i для прочтения инструкции.'

TREASURE_MESS = '''\n=== Вы вошли в комнату с сокровищами! ===\n
Вы вошли в комнату, и перед вами появился сундук с сокровищами. Внутри блестят золотые монеты! Хотите открыть сундук?\n
Нажми клавишу "y", чтобы открыть сундук или любую другую клавишу, чтобы идти дальше.'''

TRAP_MESS = '''\n=== Ловушка! ===\n
Вы вошли в комнату, и тут же услышали странный звук. Внезапно пол под вами начинает опускаться, и вы попали в ловушку! Что будете делать?\n
Нажми клавишу "y", чтобы попробовать избежать ловушки\n 
Осторожно, у Тебя мало времени!'''

MONSTER_MESS = '''\n=== Монстр в комнате! ===\n
Вы вошли в комнату, и перед вами появился ужасный монстр! Он рычит и готов напасть. Что будете делать?\n
Нажмите "y", чтобы сразиться, или любую другую клавишу, чтобы убежать.'''

NEXT_LEVEL_MESS = '''\n=== НОВЫЙ УРОВЕНЬ ===\n
Поздравляем! Вы прошли {floor} уровень.\n
У вас {lifes} жизней и {points} очков.\n
Вы поднялись на следующий этаж, и впереди вас ждут еще более опасные испытания! 
Но не бойтесь — каждый новый этаж дает шанс на большее количество сокровищ.\n
Готовы продолжить приключение? Нажмите "y" для перехода на следующий этаж или "n" для выхода из игры.'''

class Player:
  def __init__(self):
    self.lifes = 3
    self.points = 0
    self.inventory = []
    self.player_input = ''
    self.input_received = False
    self.stop_event = threading.Event()
    self.current_floor = 1

  def check_lives(self):
    if self.lifes <= 0:
      if 'зелье' in self.inventory:
        self.lifes += 1
        print(f'Благодаря зелью Вы получаете дополнительную жизнь: {self.lifes}')
        self.inventory.remove('зелье')
      else:
        print('=== Игра окончена. === \n Вы потеряли все жизни! ')
        print(BYE_MESS)
        exit()
    
  def treasure_room(self, treasure):
    print(TREASURE_MESS)
    reward_type = {'sword': 'меч', 'potion': 'зелье'}
    reward = random.choice(list(reward_type.values()))
    s = input().strip().lower()

    if s == 'y':
      self.points += treasure
      if self.current_floor >= 2:
        print('Кроме сокровищ, в сундуке есть что-то еще. Взять? "y" если да')
        s = input().strip().lower()
        if s == 'y':
          self.inventory.append(reward)
          return (f'Теперь в вашем инвентаре: {", ".join(self.inventory)}.\n'
                f'И вы нашли сокровище! Очки: +{treasure}. Всего очков: {self.points}')
        else:
          return f'Вы нашли сокровище! Очки: +{treasure}. Всего очков: {self.points}'
      else:
          return f'Вы нашли сокровище! Очки: +{treasure}. Всего очков: {self.points}'
    else:
      return 'Вы решили не брать сокровище и покинули комнату.'
    
  def countdown(self):
    for i in range(3, 0, -1):
      if self.stop_event.is_set():
        return
      print(i)
      time.sleep(1)
    if not self.stop_event.is_set():
      print('Ловушка сработала!')
      self.stop_event.set()
  
  def get_input(self):
      self.player_input = input().lower()
      self.input_received = True
      self.stop_event.set()
    
  def trap_room(self):
    print(TRAP_MESS)

    self.stop_event.clear()
    countdown_thread = threading.Thread(target=self.countdown) 
    input_thread = threading.Thread(target=self.get_input)

    countdown_thread.start()
    input_thread.start()

    countdown_thread.join()
    input_thread.join()
    self.check_lives()

    if self.input_received and self.player_input == 'y':
      return 'Вы выбрались! Жизни не потеряны.'
    else:
      self.lifes -= 1
      return f'Вы не выбрались из ловушки. Осталось жизней: {self.lifes}'

  def monster_room(self):
    print(MONSTER_MESS)
    
    if input().strip().lower() == 'y':
      chance = random.randint(1, 101)
      chance2 = 60
      time.sleep(1)
      print(f'Шансы монстра: {chance}%\n')
      if 'меч' in self.inventory:
        chance2 += 20
        time.sleep(1)
        print(f'С мечем Ваши шансы на победу растут: {chance2}%\n')
        self.inventory.remove('меч')
      time.sleep(1)
      if chance < chance2:
        return 'Вы победили монстра! Жизни не потеряны.'
      else:
        self.lifes -= 1
        self.check_lives()
        return f'Монстр вас ранил! Осталось жизней: {self.lifes}'
    else:
      return 'Вы сбежали от монстра'
    

class Room:
  def __init__(self):
    self.name = None

  def get_room(self, player, floor_number):
    room_types = ['treasure', 'trap', 'monster']
    room_weight = {1: [3, 1, 0], 2 : [3, 3, 1], 3 : [2, 3, 3]}
    chosen_room = random.choices(room_types, room_weight[floor_number])[0]

    if chosen_room == 'treasure':
      self.name = 'treasure'
      treasure = random.randint(1, 5)
      return player.treasure_room(treasure)
    elif chosen_room == 'trap':
      self.name = 'trap'
      return player.trap_room()
    elif chosen_room == 'monster':
      self.name = 'monster' 
      return player.monster_room()

class Dungeon:
  def __init__(self):
    self.floors = []
    
  def get_map(self, player):
    for floor_number in range(1, 4):
      rooms_on_floor = []
      number_of_rooms = floor_number * 3
      for _ in range(number_of_rooms):
        room = Room()
        room_result = room.get_room(player, floor_number)
        rooms_on_floor.append(room.name)
        print(room_result)
        time.sleep(2)
      if player.lifes <= 0:
        print('=== Вы потеряли все жизни! ===')
        print(BYE_MESS)
        exit()
      self.floors.append(rooms_on_floor)
      if player.points >= 5:
        if floor_number == 3:  
          print('=== Поздравляем! Вы прошли все уровни и завершили игру. ===')
          print(f'Ваш итоговый счёт: {player.points} очков и {player.lifes} жизней.')
          print(BYE_MESS)
          exit()
        print(NEXT_LEVEL_MESS.format(floor = floor_number, lifes = player.lifes, points = player.points))
        player.current_floor += 1
        next_move = input("Ваш выбор: ").strip().lower()
        if next_move != 'y':
          print(BYE_MESS)
          exit()
      else:
        print('=== Игра окончена.=== \n Вы не набрали достаточно очков для перехода на следующий уровень.')
        print(BYE_MESS)
        break
    return self.floors

player = Player()
dungeon = Dungeon()

while player.lifes > 0:
  print(WELCOME_MESS)
  user_choice = input("Твой выбор: ").strip().lower()
   
  if user_choice == 'y':
    dungeon.get_map(player)
  elif user_choice == 'n':
    print(BYE_MESS)
    exit()
  elif user_choice == 'i':
    print(INSTRUCTION_MESS)
  else:
    print(BAD_MOVE_MESS)
    continue
