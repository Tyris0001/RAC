from classes.config import *
from classes.thread import *
from classes.roblox import *
from classes.handler import *

#    def __init__(self, proxy, useragent, username, password, debug=True):


def ihate_async(typ, args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if typ == 1:
        loop.run_until_complete(createAccount(args))
        loop.close()
    else:
        loop.run_until_complete(loginAccount(args))
        loop.close()

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
        line = line.replace("\n", "").replace("\\n", "")
    return line.split(":")


if __name__ == "__main__":
    while 1:
        l = asyncio.new_event_loop()
        asyncio.set_event_loop(l)
        clear()
        print(colored("RAC - FREE VERSION", "blue"))
        print(colored("------------------", "white"))
        print(colored("[1] - Generate Accounts", "green"))
        print(colored("[2] - UP2Cookie", "green"))

        option_choice = int(input(colored("[USER] - ", "yellow")))
        clear()

        if option_choice == 1:
            thread_count = input("How many accounts do you want to generate?\n> ")
            verify_email = input("Do you want to email-verify these accounts [Y/n]?\n> ")
            
            if verify_email.lower() == "y":
                verify_email = True 
            else:
                verify_email = False

            thread_list = []

            clear()

        
                
            # taken from Aurora source-code, thanks novuh
            #loop = asyncio.new_event_loop()
            #loop.run_until_complete(conGather(*handler_list))




            handler_list = [ThreadObject(genuser(), ''.join(random.choice(string.ascii_letters) for i in range(8)), "SIGNUP", verify_email) for i in range(int(thread_count))]
            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(1, handler, )))

            for thread in thread_list:
                thread.start()


            for thread in thread_list:
                thread.join()


            print(colored("[---", "red"), end="")
            print(colored("RAC", "white"), end="")
            print(colored("---]", "red"), end="")
            print("\t-►\t", end="")
            print(colored("Finished! [ENTER]", "green"), end="")    
            input()

        elif option_choice == 2:
            print("user:password filename (without the .txt)")

            file_name = input(colored("[USER] - ", "yellow"))
            file_name = file_name+".txt"

            handler_list = []
            thread_list = []
            clear()

            for line in open(file_name).readlines():

                line = line.strip("\n").replace(" ", "")
            
                handler_list.append(ThreadObject(line.split(":")[0].strip(), line.split(":")[1].strip(), "LOGIN", False))
                
                # taken from Aurora source-code, thanks novuh
                
            #loop = asyncio.new_event_loop()
            #loop.run_until_complete(conGather(*handler_list))



            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(2, handler, )))

            for thread in thread_list:
                thread.start()


            for thread in thread_list:
                thread.join()



            print(colored("[---", "red"), end="")
            print(colored("RAC", "white"), end="")
            print(colored("---]", "red"), end="")
            print("\t-►\t", end="")
            print(colored("Finished! [ENTER]", "green"), end="")    
            input()

