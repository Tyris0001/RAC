from classes.config import *

class Handler:
    def __init__(self, proxy, useragent, username, password, captype, debug=True):
        self.debug = debug
        self.__threadname = THREAD_NAME_LIST[random.randint(0, len(THREAD_NAME_LIST)-1)].upper() + "-" +THREAD_NAME_LIST[random.randint(0, len(THREAD_NAME_LIST)-1)].upper()
        self.__proxy = proxy
        self.__useragent = useragent
        self.__username = username
        self.__password = password
        self.__csrf = None
        self.__captcha_type = CAPTCHA_TYPES[captype]
        self.__captcha_payload = None
        self.__session = requests.Session()
        self.__session.mount('http://', HTTPAdapter(max_retries=555))
        self.__cookie = None
        self.__retries = 0
        self.print("Handler created with parameters\n\t\t\t\t-Proxy: "+proxy["http"]+"\n\t\t\t\t-Username: "+ username +"\n\t\t\t\t-Password: "+ password, "green")


    def verifyEmail(self):
        self.getcsrf()
        self.print("Verifying email...", "blue")
        email_addy = self.__username.replace("_", "")
        email_verified = False
        self.print("Using email: " + email_addy+"@vddaz.com", "yellow")
        Verified = False
        while not Verified:
            email_request = requests.post("https://accountsettings.roblox.com/v1/email", headers={"X-CSRF-TOKEN":self.__csrf, "User-Agent":self.__useragent}, json={"emailAddress":email_addy+"@vddaz.com", "password":""}, cookies={".ROBLOSECURITY":self.__cookie}, proxies=self.__proxy)
            print(email_request.text)
            if email_request.status_code != 200:
                if email_request.json()["errors"][0]["code"] == 8:
                    self.print("Account already has email", "red")
                    return
                if email_request.json()["errors"][0]["code"] == 6:
                    self.print("Too many attempts", "red")
                    return
                if email_request.json()["errors"][0]["code"] == 0:
                    self.print(email_request.json()["errors"][0]["message"], "red")
                    self.newproxy()
                    self.getcsrf()
            elif email_request.status_code == 200:
                self.print("Requested verification email", "blue")
                time.sleep(10)
                em_id = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email_addy}&domain=vddaz.com").json()[0]["id"]
                body = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email_addy}&domain=vddaz.com&id={em_id}").json()["body"]
                SBod = BeautifulSoup(body, 'lxml')
                emailbutton = SBod.find_all(class_="email-button")[0]
                emailurl = emailbutton.get("href")
                email_tk = requests.post("https://accountinformation.roblox.com/v1/email/verify", proxies=self.__proxy, cookies={".ROBLOSECURITY":self.__cookie},json={"ticket": emailurl.split("=")[1]}, headers={"X-CSRF-TOKEN": self.__csrf})
                if email_tk.status_code == 200:
                    self.print("Email successfully verified!", "green")
                    Verified=False
                    xx = open('verified.txt', 'a')
                    xx.writelines(self.__cookie+"\n")
                    xx.close()
                else:
                    self.print("Failed to verify email for unknown reason!", "red")
                    return


    def captchaTask(self, captcha_blob):

            site_end = ""
            if self.__captcha_type == CAPTCHA_TYPES["SIGNUP"]:
                site_end = ""
            elif self.__captcha_type == CAPTCHA_TYPES["LOGIN"]:
                site_end = "login"
            
            solver_proxy = self.__proxy["http"].replace("http://", "").replace("@", ":").split(":")
            self.__captcha_payload = {
                "key": CAPTCHA_KEY,
                "task": {
                    "type": "FunCaptchaTask",
                    "proxy_type": "http",
                    "username": solver_proxy[0],
                    "password": solver_proxy[1],
                    "ip": solver_proxy[2],
                    "port": solver_proxy[3],
                    "site_url": "https://www.roblox.com/"+site_end,
                    "public_key": self.__captcha_type,
                    "service_url": "https://roblox-api.arkoselabs.com/",
                    "blob": captcha_blob,
                    #"user_agent": self.__useragent
                }
            }

            self.print("Prepared captcha payload", "yellow") 
            self.print("Sending captcha to solving service", "blue") 

            solve_captcha_code = 0
            solve_captcha = None
            while solve_captcha_code == 0:
                solve_captcha = requests.post("https://captcha.rip/api/create", json=self.__captcha_payload)
                solve_captcha_json = solve_captcha.json()
                if "id" in solve_captcha.text:
                    solve_captcha_code = 1
                    continue
                if solve_captcha_json["code"] == 17:
                    self.print("Task limit reached, waiting 10 seconds.", "red")
                    time.sleep(10)
            
            solve_captcha_id = solve_captcha.json()["id"]

            self.print("Captcha task created", "yellow") 
            self.print(solve_captcha_id, "yellow") if self.debug else ""    

            captcha_status = "pending"

            captcha_receive_payload = {
                "key": CAPTCHA_KEY,
                "id": solve_captcha_id
            }


            while captcha_status not in ("Solved", "Unable to solve captcha", "Unsupported game type", "Task not found"):
                time.sleep(3)
                self.print("Waiting on captcha solver", "blue") 
                rCap = requests.post("https://captcha.rip/api/fetch", json=captcha_receive_payload)
                captcha_status = rCap.json()["message"]

            # check what the response is 
            solved_captcha_token = ""

            if captcha_status == "Solved":
                solved_captcha_token = rCap.json()["token"]
                self.print(captcha_status, "green")
                return solved_captcha_token
            else:
                self.print(captcha_status, "red")

            return None 

    


    @property 
    def threadname(self):
        return self.__threadname

    @threadname.setter 
    def threadname(self, value):
        self.__threadname = value


    @property
    def captcha_payload(self):
        return self.__captcha_payload

    @captcha_payload.setter
    def captcha_payload(self, payload):
        self.__captcha_payload = payload

    @property
    def csrf(self):
        return self.csrf

    @captcha_payload.setter
    def csrf(self, csrf):
        self.csrf = csrf

        

    def print(self, message, color):
        print(colored("["+self.__threadname+"]\t-►\t", "white"), colored(message, color))

    def newproxy(self):
        le = random.choice(open("proxies.txt").readlines()).split(":")
        self.__proxy = {
            "http":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1],
            "https":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1]
        }

    

    def getcsrf(self):
        # Get the X-CSRF-TOKEN
        self.print("Grabbing X-CSRF-TOKEN", "blue")
        proxyerror = True
        while proxyerror:
            try:
                csrf_requets = requests.get("https://www.roblox.com/", cookies={".ROBLOSECURITY":self.__cookie}, proxies=self.__proxy, headers={"User-Agent":self.__useragent})
                parsed_request = re.findall(r'data-token=\"(.+)\"', csrf_requets.text)
                self.__csrf = parsed_request[0]
                self.print("Received: "+self.__csrf, "yellow") 
                proxyerror = False
            except:
                self.print("Proxy error, grabbing new proxy.", "red")
                time.sleep(1)
                self.newproxy()
               
                

    
    def loginaccount(self):
        self.print("Logging in")

    def genaccount(self):
        self.print("Captcha Metadata: " + self.__captcha_type, "yellow")
        self.print("Grabbing captcha info", "blue") 

        captcha_creation_status = False
        # lets check usernames before creating (I'm retarded for not doing this from the start)
        username_response = "Invalid"
        while not "Username is valid" in username_response:
            self.__username = genuser()
            username_request = requests.get("https://auth.roblox.com/v1/usernames/validate?request.birthday=12-12-2004&request.context=Signup&request.username="+self.__username, proxies=self.__proxy)
            username_response = username_request.text 
            #print(username_response)
            time.sleep(2)



        while not captcha_creation_status:
            captcha_req = requests.post("https://auth.roblox.com/v2/signup", headers={"x-csrf-token":self.__csrf, "User-Agent":self.__useragent}, json={"username":(str)(self.__username),"password":(str)(self.__password),"birthday":"1962-04-08T23:00:00.000Z","gender":2,"isTosAgreementBoxChecked":True,"agreementIds":["848d8d8f-0e33-4176-bcd9-aa4e22ae7905","54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"]}, proxies=self.__proxy)
            captcha_parsed = json.loads(captcha_req.text)
            #print(captcha_req.text)
            if captcha_req.status_code == 429 or not "fieldData" in captcha_req.text:
                self.print("Captcha creation: Ratelimited, changing proxy.", "red")
                time.sleep(10)
                self.newproxy()
                self.getcsrf()
            else:
                captcha_creation_status = True
            self.print("Captcha creation:"+ str(captcha_req.status_code), "yellow") if self.debug else ""



        captcha_id = (captcha_parsed["errors"][0]["fieldData"]).split(",")[0]
        captcha_blob = (captcha_parsed["errors"][0]["fieldData"]).split(",")[1]
        
        self.print("Received: "+captcha_id, "blue") 

        # need to reformat proxy lol
        solved_captcha_token = self.captchaTask(captcha_blob)

        stat_code = 400
        while stat_code != 200:
            x1 = requests.post("https://auth.roblox.com/v2/signup", headers={"x-csrf-token":self.__csrf, "User-Agent":self.__useragent}, json={"username":(str)(self.__username),"password":(str)(self.__password),"birthday":"1962-04-08T23:00:00.000Z","gender":2,"isTosAgreementBoxChecked":True,"captchaId":captcha_id, "captchaToken":solved_captcha_token,"agreementIds":["848d8d8f-0e33-4176-bcd9-aa4e22ae7905","54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"]}, proxies=self.__proxy)
            stat_code = x1.status_code
            if x1.status_code == 200:
                self.print("Account generated successfully!", "green")
                roblosec = re.findall(r'\.ROBLOSECURITY=(.+); domain=\.roblox\.com;', x1.headers["set-cookie"])
                xx = open('cookies.txt', 'a')
                xx.writelines(roblosec[0]+"\n")
                xx.close()
                xx1 = open('upc.txt', 'a')
                xx1.writelines(self.__username+":"+self.__password+":"+roblosec[0]+"\n")
                xx1.close()
                self.__cookie = roblosec[0]
                #self.verifyEmail()

            elif "Token Validation Failed" in x1.text:
                self.newproxy()
                self.getcsrf()
                time.sleep(10)

    def login(self):
        self.print("Captcha Metadata: " + self.__captcha_type, "yellow")
        self.print("Grabbing captcha info", "blue") 

        captcha_creation_status = False

        while not captcha_creation_status:
            captcha_req = requests.post("https://auth.roblox.com/v2/login", headers={"x-csrf-token":self.__csrf, "User-Agent":self.__useragent}, json={"ctype":"Username", "cvalue":(str)(self.__username),"password":(str)(self.__password)}, proxies=self.__proxy)
            captcha_parsed = json.loads(captcha_req.text)
            #print(captcha_req.text)
            if captcha_req.status_code == 429 or not "fieldData" in captcha_req.text:
                self.print("Captcha creation: Ratelimited, changing proxy.", "red")
                time.sleep(10)
                self.newproxy()
                self.getcsrf()
            else:
                captcha_creation_status = True
            self.print("Captcha creation:"+ str(captcha_req.status_code), "yellow") if self.debug else ""

        captcha_fp = json.loads(captcha_parsed["errors"][0]["fieldData"])
        #captcha_id = (captcha_parsed["errors"][0]["fieldData"]).split(",")[0]
        #captcha_blob = (captcha_parsed["errors"][0]["fieldData"]).split(",")[1]
        
        captcha_id = captcha_fp["unifiedCaptchaId"]
        captcha_blob = captcha_fp["dxBlob"]


        self.print("Received: "+captcha_id, "blue") 

        # need to reformat proxy lol
        solved_captcha_token = self.captchaTask(captcha_blob)

        stat_code = 400
        while stat_code != 200:

            login_headers = {
                "x-csrf-token":self.__csrf,
                "User-Agent":self.__useragent
            }

            login_data = {
                "captchaId":captcha_id,
                "captchaToken":solved_captcha_token,
                "ctype":"Username",
                "cvalue":self.__username,
                "password":self.__password
            }


            x1 = requests.post("https://auth.roblox.com/v2/login", headers=login_headers, json=login_data, proxies=self.__proxy)
            stat_code = x1.status_code
            if x1.status_code == 200:
                self.print("Valid account saved!", "green")
                roblosec = re.findall(r'\.ROBLOSECURITY=(.+); domain=\.roblox\.com;', x1.headers["set-cookie"])
                xx = open('cookies_login.txt', 'a')
                xx.writelines(roblosec[0]+"\n")
                xx.close()
                xx1 = open('upc_login.txt', 'a')
                xx1.writelines(self.__username+":"+self.__password+":"+roblosec[0]+"\n")
                xx1.close()
                self.__cookie = roblosec[0]
                #self.verifyEmail()

            elif "Token Validation Failed" in x1.text:
                self.newproxy()
                self.getcsrf()
                time.sleep(10)
            elif x1.status_code == 403:
                if x1.json()["errors"][0]["code"] == 1:
                    self.print("Invalid username/password.", "red")
                    return 
                if x1.json()["errors"][0]["code"] == 2:
                    self.print("Captcha failed to solve. retrying!", "red")
                    cap_json = json.loads(x1.json()["errors"][0]["fieldData"])
                    captcha_id, captcha_blob = cap_json["unifiedCaptchaId"], cap_json["dxBlob"] 

                    if self.__retries >= 3:
                        self.print("Max retires 3/3 reached, aborting handler.", "red")
                        return

                    self.__retries += 1
                    solved_captcha_token = self.captchaTask(captcha_blob)

            else:
                print(x1.text)
                print(x1.status_code)


        





