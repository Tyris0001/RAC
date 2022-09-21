from classes.config import *



async def verifyEmail(thread):
    thread.log("Verifying email...", "blue")
    
    email_address = thread.username.replace("_", "")
    email_verified = False 

    # using lasagna.email we have to "initialize" an email address. 
    try:
        with requests.get("https://lasagna.email/") as req:
            SBod = BeautifulSoup(req.text, 'lxml')
            emailbutton = SBod.find_all(class_="btn")[0]
            email_address = emailbutton.get("href")
            email_address = email_address.split("/")[2]
    except requests.exceptions.ProxyError:
        thread.log("Proxy error, get better proxies maybe?", "red")
        return 
    
    except Exception as ex:
        thread.log("Exception: " + ex)
        return


    thread.log(f"Using email: {email_address}", "yellow")
    time.sleep(5)
    thread.session.cookies.update({
        ".ROBLOSECURITY":thread.cookie
    })
    thread.getcsrf()
    email_json = {
        "emailAddress":email_address,
        "password":""
    }

    while not email_verified:
        try:
            with thread.session.post("https://accountsettings.roblox.com/v1/email", json=email_json) as req:
                if req.status_code != 200:
                    if req.json()["errors"][0]["code"] == 8:
                        thread.log("Account already has email or other error...", "red")
                        return
                    
                    if req.json()["errors"][0]["code"] == 6:
                        thread.log("Too many attempts", "red")
                        return
                    
                    if req.json()["errors"][0]["code"] == 0:
                        thread.log(req.json()["errors"][0]["message"], "red")
                        thread.newproxy()
                        thread.getcsrf()
                        

                elif req.status_code == 200:
                    thread.log("Requested verification email, waiting 10 seconds...", "blue")
                    await asyncio.sleep(10)
                    
                    body = requests.get(f"https://lasagna.email/api/inbox/{email_address}").json()["emails"][0]["Body"]
                    SBod = BeautifulSoup(body, 'lxml')
                    emailbutton = SBod.find_all(class_="email-button")[0]
                    emailurl = emailbutton.get("href")
                    
                    ticket_json = {
                        "ticket": urllib.parse.unquote(emailurl.split("=")[1])
                    }
                    email_tk = thread.session.post("https://accountinformation.roblox.com/v1/email/verify", json=ticket_json)
                    
                    if email_tk.status_code == 200:
                        thread.log("Email successfully verified!", "green")
                        Verified=False

                        verified_file = open('verified.txt', 'a')
                        verified_file.writelines(thread.cookie+"\n")
                        verified_file.close()

                        return True
                    else:
                        thread.log("Failed to verify email for unknown reason!", "red")
                        return False
        except requests.exceptions.ProxyError:
            thread.log("Proxy error, if this error happens often get better proxies (iproyal, speedproxies etc.)")
            return
"""
1secmail doesn't work at the moment
async def verifyEmail(thread):
    
    thread.log("Verifying email...", "blue")

    email_address = thread.username.replace("_", "")
    email_verified = False

    thread.log("Using email: " + email_address + "@kzccv.com", "yellow")


    
    thread.session.cookies.update({
        ".ROBLOSECURITY": thread.cookie
    })  
    thread.getcsrf()
    email_json = {
        "emailAddress":email_address+"@kzccv.com",
        "password":""
    }
    print(email_json)
    while not email_verified:
        try:
            with thread.session.post("https://accountsettings.roblox.com/v1/email", json=email_json) as req:
                print(req.text)
                if req.status_code != 200:
                    if req.json()["errors"][0]["code"] == 8:
                        thread.log("Account already has email or other error...", "red")
                        return
                    
                    if req.json()["errors"][0]["code"] == 6:
                        thread.log("Too many attempts", "red")
                        return
                    
                    if req.json()["errors"][0]["code"] == 0:
                        thread.log(req.json()["errors"][0]["message"], "red")
                        thread.newproxy()
                        thread.getcsrf()
                        

                elif req.status_code == 200:
                    thread.log("Requested verification email, waiting 10 seconds...", "blue")
                    await asyncio.sleep(10)
                    print("Wait over")
                    
                    em_id = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email_address}&domain=kzccv.com").json()[0]["id"]
                    body = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email_address}&domain=kzccv.com&id={em_id}").json()["body"]
                    print(body)
                    SBod = BeautifulSoup(body, 'lxml')
                    emailbutton = SBod.find_all(class_="email-button")[0]
                    emailurl = emailbutton.get("href")
                    
                    ticket_json = {
                        "ticket": emailurl.split("=")[1]
                    }
                    print(ticket_json["ticket"])
                    email_tk = thread.session.post("https://accountinformation.roblox.com/v1/email/verify", json=ticket_json)
                    
                    if email_tk.status_code == 200:
                        thread.log("Email successfully verified!", "green")
                        Verified=False

                        verified_file = open('verified.txt', 'a')
                        verified_file.writelines(thread.cookie+"\n")
                        verified_file.close()

                        return True
                    else:
                        thread.log("Failed to verify email for unknown reason!", "red")
                        return False
        except requests.exceptions.ProxyError:
            thread.log("Proxy error, if this error happens often get better proxies (iproyal, speedproxies etc.)")
            return
"""
async def login(thread):
    login_status = 400
    while login_status != 200:


        login_data = {
            "captchaId":thread.captchaId,
            "captchaToken":thread.captchaToken,
            "ctype":"Username",
            "cvalue":thread.username,
            "password":thread.password
        }

        with thread.session.post("https://auth.roblox.com/v2/login", json=login_data) as req:
            login_status = req.status_code

            if req.status_code == 200:
                thread.log("Valid account saved!", "green")
                rsec = re.findall(r'\.ROBLOSECURITY=(.+); domain=\.roblox\.com;', req.headers["set-cookie"])

                cookie_file = open('cookies_login.txt', 'a')
                cookie_file.writelines(rsec[0]+"\n")
                cookie_file.close()

                cookie_file = open('upc_login.txt', 'a')
                cookie_file.writelines(thread.username+":"+thread.password+":"+rsec[0]+"\n")
                cookie_file.close()

                thread.cookie = rsec[0]

            elif "Token Validation Failed" in req.text:
                thread.newproxy()
                thread.getcsrf()
                await asyncio.sleep(10)

            elif req.status_code == 403:
                if req.json()["errors"][0]["code"] == 1:
                    thread.log("Invalid username/password.", "red")
                    return 
                if req.json()["errors"][0]["code"] == 2:
                    thread.log("Captcha failed to solve. retrying!", "red")
                    cap_json = json.loads(req.json()["errors"][0]["fieldData"])
                    captcha_id, captcha_blob = cap_json["unifiedCaptchaId"], cap_json["dxBlob"] 

                    if thread.retries >= 3:
                        thread.log("Max retires 3/3 reached, aborting handler.", "red")
                        return

                    thread.retries += 1
                    solved_captcha_token = await captchaTask(thread)

            else:
                print(req.text)
                print(req.status_code)



async def createCaptcha(thread):
    captcha_creation_status = False
    while not captcha_creation_status:

        if len(thread.session.headers["x-csrf-token"]) == 0:
            thread.getcsrf()
        
        
        signup_gen_data = {
            "username":thread.username,
            "password":thread.password,
            "birthday":"1962-04-08T23:00:00.000Z",
            "gender":2,
            "isTosAgreementBoxChecked":True,
            "captchaId":thread.captchaId,
            "captchaToken":thread.captchaToken,
            "agreementIds":
            [
                "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
                "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
            ]
        }

        login_gen_data = {
            "ctype":"Username",
            "cvalue":thread.username,
            "password":thread.password
        }

        #SCUFFED!!!!!
        with thread.session.post("https://auth.roblox.com/v2/"+thread.raw_captcha_type.lower(), json=signup_gen_data if thread.raw_captcha_type == "SIGNUP" else login_gen_data) as req:
            captcha_parsed = json.loads(req.text)
            if req.status_code == 429 or not "fieldData" in req.text:
                if "token validation failed" in req.text.lower():
                    thread.log("Invalid csrf token, grabbing new one!", "red")
                    thread.getcsrf()
                    await asyncio.sleep(3)
                    continue
                thread.log("Captcha creation: Ratelimited, changing proxy.", "red")
                await asyncio.sleep(10)
                thread.newproxy()
                thread.getcsrf()
            else:
                captcha_creation_status = True
            
            captcha_id = ""
            captcha_blob = ""

            if thread.raw_captcha_type == "SIGNUP":
                captcha_id = (captcha_parsed["errors"][0]["fieldData"]).split(",")[0]
                captcha_blob = (captcha_parsed["errors"][0]["fieldData"]).split(",")[1]
            else:
                captcha_fp = json.loads(captcha_parsed["errors"][0]["fieldData"])
                captcha_id = captcha_fp["unifiedCaptchaId"]
                captcha_blob = captcha_fp["dxBlob"]
            
            thread.log("Received: "+captcha_id, "blue") 

            thread.captchaId = captcha_id
            thread.captchaBlob = captcha_blob

            return True

    return False


async def finishAccount(thread):

    # preparing the data we're going to send to generate the account
    gen_data = {
        "username":thread.username,
        "password":thread.password,
        "birthday":"1962-04-08T23:00:00.000Z",
        "gender":2,
        "isTosAgreementBoxChecked":True,
        "captchaId":thread.captchaId,
        "captchaToken":thread.captchaToken,
        "agreementIds":
        [
            "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
            "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
        ]
    }


    with thread.session.post("https://auth.roblox.com/v2/signup", json=gen_data) as req:
        if req.status_code == 200:
            thread.log("Account generated successfully!", "green")
            rsec = re.findall(r'\.ROBLOSECURITY=(.+); domain=\.roblox\.com;', req.headers["set-cookie"])

            temp_cookie = open('cookies.txt', 'a')
            temp_cookie.writelines(rsec[0]+"\n")
            temp_cookie.close()

            temp_cookie = open('upc.txt', 'a')
            temp_cookie.writelines(thread.username+":"+thread.password+":"+rsec[0]+"\n")
            temp_cookie.close()

            thread.cookie = rsec[0]
            
            if thread.verify:
                await verifyEmail(thread)
            else:
                return True

        elif "Token Validation Failed" in req.text:
            thread.newproxy()
            await asyncio.sleep(5)
            createAccount(thread)

async def createUsername(thread):
    username_response = "Invalid"
    while not "Username is valid" in username_response:
        thread.username = genuser()
        with thread.session.get("https://auth.roblox.com/v1/usernames/validate?request.birthday=12-12-2004&request.context=Signup&request.username="+thread.username) as req:
            username_response = req.text 
            await asyncio.sleep(2)

    return True


async def captchaTask(thread):
    # not using sessions here fuck you

    site_end = ""
    if thread.captcha_type == CAPTCHA_TYPES["SIGNUP"]:
        site_end = ""
    elif thread.captcha_type == CAPTCHA_TYPES["LOGIN"]:
        site_end = "login"
    
    solver_proxy = thread.session.proxies["http"].replace("http://", "").replace("@", ":").split(":")

    captcha_payload = {
        "key": CAPTCHA_KEY,
        "task": {
            "type": "FunCaptchaTask",
            "proxy_type": "http",
            "username": solver_proxy[0],
            "password": solver_proxy[1].strip("\n"),
            "ip": solver_proxy[2],
            "port": solver_proxy[3],
            "site_url": "https://www.roblox.com/"+site_end,
            "public_key": thread.captcha_type,
            "service_url": "https://roblox-api.arkoselabs.com/",
            "blob": thread.captchaBlob,
            #"user_agent": thread.useragent
        }
    }

    thread.log("Prepared captcha payload", "yellow") 
    thread.log("Sending captcha to solving service", "blue") 

    task_created = False
    solve_captcha = None

    while not task_created:
        solve_captcha = requests.post("https://captcha.rip/api/create", json=captcha_payload)
        solve_captcha_json = solve_captcha.json()
        if "id" in solve_captcha.text:
            task_created = True
            continue
        if solve_captcha_json["code"] == 17:
            thread.log("Task limit reached, waiting 10 seconds.", "red")
            await asyncio.sleep(10)

    solve_captcha_id = solve_captcha.json()["id"]

    thread.log("Captcha task created", "yellow") 

    captcha_status = "pending"

    captcha_receive_payload = {
        "key": CAPTCHA_KEY,
        "id": solve_captcha_id
    }

    while captcha_status not in ("Solved", "Unable to solve captcha", "Unsupported game type", "Task not found"):
        await asyncio.sleep(3)
        thread.log("Waiting on captcha solver", "blue") 
        rCap = requests.post("https://captcha.rip/api/fetch", json=captcha_receive_payload)
        captcha_status = rCap.json()["message"]

    # check what the response is 
    solved_captcha_token = ""

    if captcha_status == "Solved":
        solved_captcha_token = rCap.json()["token"]
        thread.log(captcha_status, "green")
        thread.captchaToken = solved_captcha_token
        return True
    else:
        thread.log(captcha_status, "red")
        return False
    


