#Don't change anything in a box of #s
#############################
import praw, sqlite3, obot     
from time import sleep, time#
from random import choice   #
#############################


##################################################
conn = sqlite3.connect("giveaway.db")            #
c = conn.cursor()                                #
 #
r = obot.login()
alreadyReplied = []                              #
##################################################

giveawayString = "*MESSAGE TO BE SENT TO GIVEAWAY WINNERS HERE. PLACE '%s's WHEREVER YOU WANT THE GIVEAWAY REDEMTION KEY AND KEY VALUE TO APPEAR (WILL APPEAR IN THAT ORDER)%s"
sillies = ["*Silly responses need to be added here*", "Seperated by commas", "And surrounded by quotes"]
sillyTrigger = "Mr. Master"




#tested, works
################################################################
def create_database():                                         #
    c.execute('''CREATE TABLE IF NOT EXISTS giveaway           
                (username text, code text, value text)''')     #
    conn.commit()                                              #
                                                               #
                                           #
                                                               #
#works                                                         #
while True:                                                    #
    try:                                                       #
        CONTROL = input("Control username\n> ")            #
        print(CONTROL)
        break                                                  #
    except praw.errors.InvalidUserPass:                        #
        print("Invalid Username/password, please try again.")   #
################################################################

################################
#tested, works
#################################################################################
def inbox():                                                                    #
    unread = r.get_unread()                                                     #
    for i in unread:      
        author = i.author.name                                                  #
        if author.lower()==CONTROL.lower() and i.body.split("\n")[0].strip() == "+new giveaway":#
            #strips away the "+new giveaway line for the parser"       
            giveaway("\n".join(i.body.split("\n")[1:]).strip()) #check    
        elif author not in alreadyReplied and not i.was_comment:                #
            dispowered_giveaway(author) #check                                  #
            alreadyReplied.append(author)                                       #
        i.mark_as_read() 

#################################################################################
#works, tested
###############################################################
def giveaway(body):                                           #
    #{'username':['code', 'value']}     
                         #
    to = parse(body)        
    clear_database()                                      #
    add_database(to)
    users = []#
    for k in to:
        users.append({k:to[k]})
    print(users)
    for i in users:                                           #                 
        for j in i:                                # 
###############################################################
                                #Message title                #code   value($)
            print(i)
            r.send_message(j, "Giveaway prize", giveawayString%(i[j][0], i[j][1]))


#works, tested
#############################################################################
def clear_database():                                                       #
    c.execute("DELETE FROM giveaway")                                       #
    conn.commit()                                                           #
                                                                            #
def add_database(userDict):             
                                        #
    for k, v in userDict.items():                                                    #
        c.execute("INSERT INTO giveaway VALUES (?, ?, ?)", (k, v[0], v[1])) #        
        conn.commit()                                                      #
                                                                            #
#tested, works. Expects each line to be formatted "username: code value"    #
def parse(body):  
    temp = {}                    
    for line in body.split('\n\n'):
                                                                 #
        #['username', 'code value']                                         #
        parse1 = line.split(":")                                            #
        #{'username': ['code', 'value']}                                    #
        temp[parse1[0].strip()] = parse1[1].strip().split()  
    return temp                                                          #
#############################################################################

#tested, works.
###########################################################################################
def dispowered_giveaway(author):                                                          #
    response = c.execute("SELECT * FROM giveaway WHERE username=?", (author,))            #
    responseString = ", ".join(i[1] for i in response)                                    #
    if responseString:                                                                    #
###########################################################################################
                                #Message title    #message body
        r.send_message(author, "Giveaway code", "Your redemtion code(s): %s"%responseString)
##########
    else:#
##########                      #message title   #message body
        r.send_message(author, "Giveaway code", "404'd! No code found. If you feel this message is in error, please contact /u/project_twenty5oh1")
################################

################################
#works, tested
##################################################################################
def comments():                                                                  #
    comment_stream = praw.helpers.comment_stream(r, 'all')                       #
    i=0                                                                          #
    for j in comment_stream:                                                     #
        if j.author.name.lower() == CONTROL.lower() and j.body == sillyTrigger:  #
            silly(j)                                                             #
        if i>1500:                                                               #
            break                                                                #
        i=i+1                                                                    #
                                                                                 #
#works, tested                                                                   #
def silly(comment):                                                              #
    comment.reply(choice(sillies))                                               #
##################################################################################
################################

####################################
def main():                        #
    now = int(time())              #
    while True:                    #
        try:                       #
            inbox() #check         #
            comments() #check      #
            if (time()-now) > 300: #
                alreadyReplied = []#
                now = int(time())  #
        except KeyboardInterrupt:  #
            break                  #
        except:                    #
            pass                   #
                                   #
                                   #
if __name__ == '__main__':         #
    create_database()              #
    main()                         #
####################################
