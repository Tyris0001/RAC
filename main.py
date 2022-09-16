from classes.config import *
from classes.handler import *


#    def __init__(self, proxy, useragent, username, password, debug=True):


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
        line = line.replace("\n", "").replace("\\n", "")
    return line.split(":")

handler_list = []
thread_list = []
if __name__ == "__main__":

    print(colored("RAC - FREE VERSION", "blue"))
    print(colored("------------------", "white"))
    print(colored("[1] - Generate Accounts", "green"))
    print(colored("[2] - UP2Cookie", "green"))

    option_choice = int(input(colored("[USER] - ", "yellow")))
    clear()
    if option_choice == 1:
        thread_count = input("How many accounts do you want to generate?\n> ")

        for acc in range(int(thread_count)):
            p = open("proxies.txt")
            le = random_line(p)

            prx = {
                "http":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1],
                "https":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1]
            }

            handler_list.append(Handler(prx, USERAGENTS[random.randint(0, len(USERAGENTS) - 1)], genuser(), ''.join(random.choice(string.ascii_uppercase) for i in range(8)), "SIGNUP"))


        for handler in handler_list:
            handler.getcsrf()

        for handler in handler_list:
            thread_list.append(threading.Thread(target=handler.genaccount))

        for thread in thread_list:
            thread.start()


        for thread in thread_list:
            thread.join()
    elif option_choice == 2:
        print("user:password filename (without the .txt)")
        file_name = input(colored("[USER] - ", "yellow"))
        file_name = file_name+".txt"
        for line in open(file_name).readlines():
            p = open("proxies.txt")
            le = random_line(p)

            prx = {
                "http":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1],
                "https":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1]
            }

            handler_list.append(Handler(prx, USERAGENTS[random.randint(0, len(USERAGENTS) - 1)], line.split(":")[0],  line.split(":")[1], "LOGIN"))


        for handler in handler_list:
            handler.getcsrf()

        for handler in handler_list:
            thread_list.append(threading.Thread(target=handler.login))

        for thread in thread_list:
            thread.start()

