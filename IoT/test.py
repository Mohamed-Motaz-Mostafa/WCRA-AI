from http import client
from pymongo import MongoClient
import pymongo
import pprint
import time 

def printDB(moves):
    for aa in moves:
        print( aa)



def MoveFromDic(dic):

    f=dic['from']
    t=dic['to']
    M=f+t
    return M


   



def SetUp():

    conn_str="mongodb+srv://arm:123321@moves.yxjpv.mongodb.net/?retryWrites=true&w=majority"
    client=MongoClient(conn_str)

    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB") 

    return client


def AcessDB(client):
    db=client["myFirstDatabase"]
    print('this is db : =====>',db) #collection
    moves=db["moves"]
    MovesToPrint=db["moves"].find()
    return moves,MovesToPrint




def AddNewMove(HumanMove,moves):
    moves.insert_one({'move':{"from":HumanMove[0]+HumanMove[1],"to":HumanMove[2]+HumanMove[3]}})
    



def ReadLastMove(lastAddedmoveByRaspberry):
    while True :
        moves,_ =AcessDB(client)
        name=moves.find().limit(1).sort([('$natural',-1)])
        for aa in name:
            dic=aa['move']
            print("Move dic : ",aa['move'])
        lastmove=MoveFromDic(dic)
        if lastmove != lastAddedmoveByRaspberry :
            print("last move :",lastmove)
            return lastmove
            
        else :
            print ('the same move')
            time.sleep(5)

            


client=SetUp()
Moves,MP = AcessDB(client)



HumanMove = 'e7e5'

AddNewMove(HumanMove,Moves)
print("e7e5 was added ")


lastMove=ReadLastMove(HumanMove)

print('new move ============>>>>>>>>>>',lastMove)

printDB(MP)





















