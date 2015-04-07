import praw, sqlite3
from time import sleep
from random import choice

giveawayString = "*MESSAGE TO BE SENT TO GIVEAWAY WINNERS HERE. PLACE '%s's WHEREVER YOU WANT THE GIVEAWAY REDEMTION KEY AND KEY VALUE TO APPEAR (WILL APPEAR IN THAT ORDER)%s"
conn = sqlite3.connect("giveaway.db")
c = conn.cursor()
sillies = ["*Silly responses need to be added here*", "Seperated by commas", "And surrounded by quotes"]
r = praw.Reddit("Giveaway bot by /u/Thirdegree")
sillyTrigger = "Mr. Master"

#tested, works
def create_database():
    c.execute('''CREATE TABLE IF NOT EXISTS giveaway
                (username text, code text, value text)''')
    conn.commit()

#works
def _login():
    USERNAME = raw_input("Username?\n> ")
    r.login(USERNAME, "")
    return USERNAME

#works
while True:
    try:
        USERNAME = _login()
        CONTROL = raw_input("Control username\n> ")
        break
    except praw.errors.InvalidUserPass:
        print "Invalid Username/password, please try again."

################################
#tested, works
def inbox():
    unread = r.get_unread()
    for i in unread:
        author = i.author.name
        if author==CONTROL:
            if i.body.split("\n")[0].strip() == "+new giveaway":
                #strips away the "+new giveaway line for the parser"
                giveaway("\n".join(i.body.split("\n")[1:]).strip()) #check
        else:
            dispowered_giveaway(author) #check
        i.mark_as_read()

#works, tested
def giveaway(body):
    #{'username':['code', 'value']}
    to = parse(body)
    add_database(to)
    for k, v in to.items():
                                                        #code   value($)
        r.send_message(k, "Giveaway prize", giveawayString%(v[0], v[1]))

#works, tested
def add_database(userDict):
    c.execute("DELETE FROM giveaway")
    conn.commit()
    for k, v in userDict.items():
        c.execute("INSERT INTO giveaway VALUES (?, ?, ?)", (k, v[0], v[1]))
        conn.commit()

#tested, works. Expects each line to be formatted "username: code value"
def parse(body):
    temp = {}
    for line in body.split('\n\n'):
        #['username', 'code value']
        parse1 = line.split(":")
        #{'username': ['code', 'value']}
        temp[parse1[0].strip()] = parse1[1].strip().split()
    return temp

#tested, works.
def dispowered_giveaway(author):
    response = c.execute("SELECT * FROM giveaway WHERE username=?", (author,)).fetchone()
    if response:
        r.send_message(author, "Giveaway code", "Your redemtion code is %s"%response[1])
    else:
        r.send_message(author, "Giveaway code", "404'd! No code found. If you feel this message is in error, please contact /u/project_twenty5oh1")
################################

################################
#works, tested
def comments():
    comment_stream = praw.helpers.comment_stream(r, 'all')
    i=0
    for j in comment_stream:
        if j.author.name.lower() == CONTROL.lower() and j.body == sillyTrigger:
            silly(j)
        if i>1000:
            break
        i=i+1

#works, tested
def silly(comment):
    comment.reply(choice(sillies))
################################


def main():
    while True:
        inbox() #check
        comments() #check


if __name__ == '__main__':
    create_database()
    main()