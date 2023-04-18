
import tgbot.config as config
from datetime import datetime
from .database import DBManager

# list of games
GAMES = ['🔮 Dice Classic', '🔮 Tall and Bass', '🔮 DBong']

# instance of database
db = DBManager(config.DATABASE)


def register_user(user: int):
    
    if not db.exist_user(user.id):
        db.add_user(user.id, user.username, 0, user.full_name)

def get_money(user: int):

    user = db.get_user_by_id(user)

    return user['money']

def send_money(gid: int, user: int, number: int, money: float, game: str):

    time = datetime.now()

    db.add_betting(gid, parse_numbers(number, game), money, game, time, user)

def validate_betting(betting_id: int):

    db.set_betting(betting_id)

def send_deposite(gid: int, money: float, user: int):

    db.add_deposite(gid, money, user)

def remove_deposite(gid: int):

    db.remove_deposite(gid)

def accepted_deposite(gid: int):
    
    deposite = db.get_deposite_by_id(gid)
    user = db.get_user_by_id(deposite['user'])

    money = float(user['money'] + deposite['money'])

    db.set_user(money, user['id'])
    remove_deposite(gid)

    return user, money

# Auxiliar Methods

def parse_numbers(number, game):

    if game == GAMES[0]:

        return str(number)

    if game == GAMES[1]:

        if number <= 3:
        
            return '1 2 3'
        
        return '4 5 6'
    
    return ' '.join([str(i) for i in range(1, 7) if i != number])
