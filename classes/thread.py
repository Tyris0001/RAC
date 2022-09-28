from classes.config import *

class ThreadObject:
    def __init__(self, username, password, captype, verify_email):
        self.__session = requests.Session()
        self.__threadname = THREAD_NAME_LIST[random.randint(0, len(THREAD_NAME_LIST)-1)].upper() + "-" +THREAD_NAME_LIST[random.randint(0, len(THREAD_NAME_LIST)-1)].upper()
        self.__proxy = None
        self.__useragent = random.choice(USERAGENTS)
        self.__retries = 0
        self.__username = username
        self.__password = password 
        self.__raw_captcha_type = captype
        self.__cookie = None
        self.__verify = verify_email
        self.__captchaId = None 
        self.__captchaToken = None
        self.__captchaBlob = None
        self.__groupId = None
        self.__status = 0
        self.__groupMessage = None

        self.__session.headers["User-Agent"] = self.__useragent

        self.log("Finished setup", "blue")
        
        if captype != "CHECK":
            self.__captcha_type = CAPTCHA_TYPES[captype]
            self.__csrf = None

    @property 
    def session(self):
        return self.__session

    @property
    def verify(self):
        return self.__verify

    @property 
    def retries(self):
        return self.__retries

    @retries.setter
    def retries(self, value):
        self.__retries = value

    @property 
    def raw_captcha_type(self):
        return self.__raw_captcha_type

    @property 
    def proxy(self):
        return self.__proxy

    @property
    def useragent(self):
        return self.__useragent

    @property
    def username(self):
        return self.__username

    @username.setter 
    def username(self, value):
        self.__username = value
    
    @property
    def password(self):
        return self.__password

    @property
    def csrf(self):
        return self.__csrf

    @property
    def captcha_type(self):
        return self.__captcha_type

    @property
    def cookie(self):
        return self.__cookie
    
    @cookie.setter 
    def cookie(self, value):
        self.__cookie = value

    @property
    def captchaId(self):
        return self.__captchaId

    @captchaId.setter 
    def captchaId(self, value):
        self.__captchaId = value 

    @property 
    def captchaToken(self):
        return self.__captchaToken

    @captchaToken.setter 
    def captchaToken(self, value):
        self.__captchaToken = value

    @property 
    def captchaBlob(self):
        return self.__captchaBlob

    @captchaBlob.setter 
    def captchaBlob(self, value):
        self.__captchaBlob = value

    @property
    def groupMessage(self):
        return self.__groupMessage

    @groupMessage.setter 
    def groupMessage(self, value):
        self.__groupMessage = value

    @property
    def status(self):
        return self.__status

    @status.setter 
    def status(self, value):
        self.__status = value

    @property 
    def groupId(self):
        return self.__groupId

    @groupId.setter 
    def groupId(self, value):
        self.__groupId = value
    
    def newproxy(self):
        le = random.choice(PROXIES).split(":")
        self.__proxy = {
            "http":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1],
            "https":"http://"+le[2] + ":" + le[3] + "@" +le[0] +":"+le[1]
        }
        self.__session.proxies = self.__proxy

                

    def getcsrf(self):
        # Scuffed 😭
        self.log("Grabbing X-CSRF-TOKEN", "blue")
        proxyerror = True
        while proxyerror:
            try:
                with self.__session.get("https://www.roblox.com/", timeout=10) as req:
                    parsed_request = re.findall(r'data-token=\"(.+)\"', req.text)
                    self.__csrf = parsed_request[0]
                    self.log("Received: "+self.__csrf, "yellow") 
                    self.__session.headers["x-csrf-token"] = self.__csrf
                    proxyerror = False
            except:
                self.log("Proxy error, grabbing new csrf token.", "red")
                self.newproxy()
                

    def log(self, text, color):
        print(colored("[", "red"), end="")
        print(colored(self.__threadname, "white"), end="")
        print(colored("]", "red"), end="")
        print("\t-►\t", end="")
        print(colored(text, color))    