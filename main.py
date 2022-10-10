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
    elif typ == 2:
        loop.run_until_complete(loginAccount(args))
        loop.close()
    elif typ == 3:
        loop.run_until_complete(checkCookie(args))
        loop.close()
    elif typ == 4:
        loop.run_until_complete(checkCookie(args))
        loop.close()
    elif typ == 5:
        loop.run_until_complete(joinGroup(args))
        loop.close()
    elif typ == 6:
        loop.run_until_complete(postGroup(args))
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

    v_request = requests.get("https://raw.githubusercontent.com/Tyris0001/RAC/main/version")
    if not v_request.text in open("version").read():
        print(colored("Outdated RAC version, please download the newest version from [https://github.com/Tyris0001/RAC]", "red"))
        exit()

    while 1:
        l = asyncio.new_event_loop()
        asyncio.set_event_loop(l)
        clear()
        print(colored("RAC - FREE VERSION", "blue"))
        print(colored("------------------", "white"))
        checkSolver()      
        print(colored("[Please note that cookie files are overwritten regularly, save working cookies in another directory as I have yet to implement better file-creation]", "cyan"))

        option_choice = int(input(colored("[USER] - ", "yellow")))
        clear()

        if option_choice == 1:
            thread_count = input("How many accounts do you want to generate?\n> ")
            verify_email = input("Do you want to email-verify these accounts [Y/n]?\n> ")
            
            if verify_email.lower() == "y":
                verify_email = True 
            else:
                verify_email = False

            clear()

            thread_list = []            
            created_accounts = 0
            verified_accounts = 0
            handler_list = [ThreadObject(genuser(), ''.join(random.choice(string.ascii_letters) for i in range(8)), "SIGNUP", verify_email) for i in range(int(thread_count))]
            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(1, handler, )))

            for thread in thread_list:
                thread.start()


            for thread in thread_list:
                thread.join()

            for thread in handler_list:
                if thread.status == 1:
                    created_accounts += 1
                elif thread.status == 2:
                    created_accounts += 1
                    verified_accounts += 1

            # this shit is actually ugly i'm so sorry

            print(colored("[---", "red"), end="")
            print(colored("RAC", "white"), end="")
            print(colored("---]", "red"), end="")
            print("\t-►\t", end="")
            print(colored(f"{created_accounts}/{thread_count} accounts created.", "green"))   

            print(colored("[---", "red"), end="")
            print(colored("RAC", "white"), end="")
            print(colored("---]", "red"), end="")
            print("\t-►\t", end="")
            print(colored(f"{verified_accounts}/{thread_count} accounts email verified.", "green"))   

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

        elif option_choice == 3:
            print("Cookie filename (without the .txt)")

            file_name = input(colored("[USER] - ", "yellow"))
            file_name = file_name+".txt"

            handler_list = []
            thread_list = []
            clear()

            for line in open(file_name).readlines():

                line = line.strip("\n").replace(" ", "")

                TObj = ThreadObject(None, None, "CHECK", False)
                TObj.cookie = line
                handler_list.append(TObj)

            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(3, handler, )))

            for thread in thread_list:
                thread.start()


            for thread in thread_list:
                thread.join()


            print(colored("[---", "red"), end="")
            print(colored("RAC", "white"), end="")
            print(colored("---]", "red"), end="")
            print("\t-►\t", end="")
            print(colored(f"Valid cookies have been written to valid.txt"))
            print(colored("Finished! [ENTER]", "green"), end="")    
            input()

        elif option_choice == 4:
            print("Cookie filename (without the .txt)")

            file_name = input(colored("[USER] - ", "yellow"))
            file_name = file_name+".txt"

            handler_list = []
            thread_list = []
            clear()

            for line in open(file_name).readlines():

                line = line.strip("\n").replace(" ", "")

                TObj = ThreadObject(None, None, "CHECK", True)
                TObj.cookie = line
                handler_list.append(TObj)

            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(3, handler, )))

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

        elif option_choice == 5:
            print("Cookie filename (without the .txt)")

            file_name = input(colored("[USER] - ", "yellow"))
            file_name = file_name+".txt"

            print("Group Id")
            group_id = input(colored("[USER] - ", "yellow"))

            print("Amount of joins [leave blank for entire cookie file]")
            count = input(colored("[USER] - ", "yellow"))

            handler_list = []
            thread_list = []
            clear()
            if count != "":
                count = int(count)
            ind = 0
            for line in open(file_name).readlines():
                
                line = line.strip("\n").replace(" ", "")
                
                TObj = ThreadObject(None, None, "GROUP_JOIN", True)
                TObj.cookie = line
                TObj.groupId = group_id
                handler_list.append(TObj)
                if count == "":
                    continue 
                else:
                    if count <= ind:
                        pass

                    ind += 1

            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(5, handler, )))

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

        elif option_choice == 6:
            print("Cookie filename (without the .txt)")

            file_name = input(colored("[USER] - ", "yellow"))
            file_name = file_name+".txt"

            print("Group Id")
            group_id = input(colored("[USER] - ", "yellow"))

            print("Message type\n[1] - User input\n[2] - text file")
            message_type = int(input(colored("[USER] - ", "yellow")))




            handler_list = []
            thread_list = []
            message_text = None
            message_file = None

            if message_type == 1:
                print("Message text")
                message_text = input(colored("[USER] - ", "yellow"))
            else:
                print("Filename (without the .txt)")
                message_file = input(colored("[USER] - ", "yellow"))

            


            clear()



            for line in open(file_name).readlines():

                line = line.strip("\n").replace(" ", "")

                TObj = ThreadObject(None, None, "GROUP_WALL_POST", True)
                TObj.cookie = line
                TObj.groupId = group_id
                TObj.groupMessage = message_text if message_text != None else random.choice(open(message_file+".txt").readlines())
                handler_list.append(TObj)
                
            for handler in handler_list:
                thread_list.append(threading.Thread(target=ihate_async, args=(6, handler, )))

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
