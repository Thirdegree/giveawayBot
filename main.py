import praw, sqlite3
from time import sleep

giveawayString = "*MESSAGE TO BE SENT TO GIVEAWAY WINNERS HERE. PLACE '%s' WHEREVER YOU WANT THE GIVEAWAY REDEMTION KEY TO APPEAR"
conn = sqlite3.connect("giveaway.db")
c = conn.cursor()

def create_database():
    c.execute('''CREATE TABLE IF NOT EXISTS giveaway
                (username text, code text)''')
    conn.execute()

def _login():
    USERNAME = raw_input("Username?\n> ")
    r.login(USERNAME, "")
    return USERNAME

while True:
    try:
        USERNAME = _login()
        CONTROL = raw_input("Control username\n> ")
        break
    except praw.errors.InvalidUserPass:
        print "Invalid Username/password, please try again."


def inbox():
    unread = r.get_unread()
    for i in unread:
        author = i.author
        if author==CONTROL:
            giveaway(i.body)
        else:
            dispowered_giveaway(author)
        i.mark_as_read()

def giveaway(body):
    #{'username':'code'}
    to = parse(body)
    for k, v in to.items():
        send_message(k, "Giveaway prize", giveawayString%v)
        sleep(2)

def parse(body):
    temp = {}
    for line in body.split('\n'):
        #['username', 'code']
        parse1 = line.split(":")
        temp[parse1[0].strip()] = parse1[1].strip()
    return temp

def dispowered_giveaway(author):
    response = c.execute("SELECT * FROM giveaway WHERE username=?", (author,))





def main():
    while True:
        inbox()
        comments()


if __name__ == '__main__':
    create_database()
    main()