from threading import Thread
import random 
import socket

# address family,socketType
#ipv4(AF_INET) and ipv6(AF_INET6)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.2'
port = 5500

# tuple
server.bind((ip_address, port))
server.listen()

list_of_clients = []
print("server is running.......")

question=[
    "what is the italian word for pie? \n a.mozarella\n b.pasty\n c.patty\n d.pizza",
    "water boils at 212 units at which scale? \n a.F\n b.C\n c.K\n d.R",
    "which sea creature has 3 hearts? \n a.dolphin\n b.octopus\n c.walrus\n d.seal",
]

answers=["d","a","b"]

def clientThread(conn):
    score=0
    conn.send("Welcome to the quizgame".encode("utf-8"))
    conn.send("you will recieve a question.The answer to that question should be one of a,b,c,d\n".encode("utf-8"))
    conn.send("good luck!\n\n".encode("utf-8"))
    index,question,answers=get_random(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower()==answers:
                    score+=1
                    conn.send(f"bravo your score is {score}\n\n".encode("utf-8"))
                else:
                    conn.send("incorrect answer\n\n".encode("utf-8"))
                remove_question(index)
                index,question,answers=get_random(conn)
            else:
                remove(conn)
        except:
            continue

def remove_question(index):
    question.pop(index)
    answers.pop(index)

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)


def get_random(conn):
    random_index=random.randint(0,len(question)-1)
    random_question=question[random_index]
    random_answer=answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index,random_question,random_answer

# accept function
while True:
    conn, address = server.accept()
    list_of_clients.append(conn)
    print(address[0]+"connected")

    newThread = Thread(target=clientThread, args=(conn, address))
    newThread.start()
