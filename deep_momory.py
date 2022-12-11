import sqlite3
from neurons import *
from talk import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
conn = sqlite3.connect('Knowledge/Deepmemory')
def find(question):
    try:
        c = conn.cursor()
        c.execute("SELECT id, question, answer FROM questions where question like ? or answer like ?",('%'+question+'%', '%'+question+'%',))
        result = c.fetchall()
        if(len(result) > 1):
            return nural_think(question, result)
        elif(len(result) == 1):
            return result[0][2]
        else:
            return 0
    except:
        print("DEEP MEMORY: "+bcolors.FAIL+"Too deep info, may or may not compleated"+bcolors.ENDC)
        return 0

def add(question, answer):
    try:
        c = conn.cursor()     
        c.execute('INSERT INTO questions (question, answer) VALUES (?, ?)', (question, answer,))
        conn.commit()
    except:
        print("DEEP MEMORY: "+bcolors.FAIL+"Memory Add failure"+bcolors.ENDC)