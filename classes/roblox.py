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
        thread.log("Exception: " + ex,  "red")
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
                    body = ""
                    try:
                        body = requests.get(f"https://lasagna.email/api/inbox/{email_address}").json()["emails"][0]["Body"]
                    except:
                        thread.log("Email could not be sent, aborting...", "red")
                        return
                    SBod = BeautifulSoup(body, 'lxml')
                    emailbutton = SBod.find_all(class_="email-button")[0]
                    emailurl = emailbutton.get("href")
                    
                    ticket_json = {
                        "ticket": urllib.parse.unquote(emailurl.split("=")[1])
                    }
                    email_tk = thread.session.post("https://accountinformation.roblox.com/v1/email/verify", json=ticket_json)
                    
                    if email_tk.status_code == 200:
                        thread.log("Email successfully verified!", "green")
                        thread.status = 2
                        Verified=False

                        verified_file = open('verified.txt', 'a')
                        verified_file.writelines(thread.cookie+"\n")
                        verified_file.close()

                        return True
                    else:
                        thread.log("Failed to verify email for unknown reason!", "red")
                        return False
        except requests.exceptions.ProxyError:
            thread.log("Proxy error, if this error happens often get better proxies (iproyal, speedproxies etc.)", "red")
            return


async def checkGroup(thread):
    thread.session.cookies.update({
        ".ROBLOSECURITY":thread.cookie
    })
    thread.getcsrf()
    await asyncio.sleep(5)
    try:
        with thread.session.post(f"https://groups.roblox.com/v1/groups/{thread.groupId}/users", json={"sessionId":"","redemptionToken":""}) as req:
            if "You are already a member of this group." in req.text:
                return True 
            elif "Token validation failed" in req.text:
                checkGroup(thread)
            else:
                return False
    except Exception as ex:
        print("ERROR", ex)

async def groupMessage(thread):
    message_status = 400
    while message_status != 200:
        
        message_data = {
            "captchaId":thread.captchaId,
            "captchaProvider":"PROVIDER_ARKOSE_LABS",
            "captchaToken":thread.captchaToken,
            "body":thread.groupMessage
        }

        try:
            with thread.session.post(f"https://groups.roblox.com/v1/groups/{thread.groupId}/wall/posts", json=message_data) as req:
                message_status = req.status_code
                if req.status_code == 200:
                    thread.log(f"Successfully posted message [{thread.groupMessage}]", "green")
                    return 
                elif req.status_code == 403:
                    if thread.retries >= 3:
                        thread.log("Retries 3/3, aborting...", "red")
                        message_status == 200
                        return
                    cap_json = json.loads(req.json()["errors"][0]["fieldData"])
                    thread.captchaId, thread.captchaBlob = cap_json["unifiedCaptchaId"], cap_json["dxBlob"] 
                    await captchaTask(thread)
                    thread.retries += 1
        except Exception as ex:
            print("ERROR", ex)


async def rojoinGroup(thread):
    join_status = 400
    while join_status != 200:

        join_data = {
            "captchaId":thread.captchaId,
            "captchaProvider":"PROVIDER_ARKOSE_LABS",
            "captchaToken":thread.captchaToken,
            "redemptionToken":"",
            "sessionId":""
        }

        try:
            with thread.session.post(f"https://groups.roblox.com/v1/groups/{thread.groupId}/users", json=join_data) as req:
                join_status = req.status_code
                if req.status_code == 200:
                    thread.log("Successfully joined group!", "green")
                elif req.status_code == 403:
                    if thread.retries >= 3:
                        thread.log("Retries 3/3, aborting...", "red")
                        return
                    if "fieldData" in req.text:
                        cap_json = json.loads(req.json()["errors"][0]["fieldData"])
                        thread.captchaId, thread.captchaBlob = cap_json["unifiedCaptchaId"], cap_json["dxBlob"] 
                        await captchaTask(thread)
                    else:
                        thread.newproxy()
                        await asyncio.sleep(1)
                        thread.getcsrf()

                    thread.retries += 1
                elif "Token validation" in req.text:
                    thread.log("Invalid CSRF Token, regenerating...", "red")
                    thread.getcsrf()
                    await asyncio.sleep(5)
        except Exception as ex:
            print("ERROR", ex)


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
        try:
            with thread.session.post("https://auth.roblox.com/v2/login", json=login_data) as req:
                login_status = req.status_code

                if req.status_code == 200:
                    thread.log("Valid account saved!", "green")
                    rsec = re.findall(r'\.ROBLOSECURITY=(.+); domain=\.roblox\.com;', req.headers["set-cookie"])
                    
                    thread.status = 1

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
        except requests.exceptions.ProxyError:
            thread.newproxy()


async def createCaptcha(thread):
    captcha_creation_status = False
    while not captcha_creation_status:

        if len(thread.session.headers["x-csrf-token"]) == 0:
            thread.getcsrf()
        
        


        ro_data = {}

        ro_url = ""
        if thread.raw_captcha_type == "SIGNUP":
            ro_url = "https://auth.roblox.com/v2/signup"
            ro_data = {
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

        elif thread.raw_captcha_type == "LOGIN":
            ro_url = "https://auth.roblox.com/v2/login"
            ro_data = {
                "ctype":"Username",
                "cvalue":thread.username,
                "password":thread.password
            }

        elif thread.raw_captcha_type == "GROUP_JOIN":
            ro_url = f"https://groups.roblox.com/v1/groups/{thread.groupId}/users"
            ro_data = {"sessionId":"","redemptionToken":""}
            thread.session.cookies.update({
                ".ROBLOSECURITY":thread.cookie
            })
        elif thread.raw_captcha_type == "GROUP_WALL_POST":
            ro_url = f"https://groups.roblox.com/v1/groups/{thread.groupId}/wall/posts"
            ro_data = {"body":thread.groupMessage}
            thread.session.cookies.update({
                ".ROBLOSECURITY":thread.cookie
            })

        else:
            ro_url = "https://auth.roblox.com/v2/signup"
            ro_data = {}


        #SCUFFED!!!!!
        with thread.session.post(ro_url, json=ro_data) as req:
            captcha_parsed = json.loads(req.text)
            if req.status_code == 429 and not "fieldData" in req.text:
                if "token validation failed" in req.text.lower():
                    thread.log("Invalid csrf token, grabbing new one!", "red")
                    thread.getcsrf()
                    await asyncio.sleep(3)
                    continue
                thread.log("Captcha creation: Ratelimited, changing proxy.", "red")
                await asyncio.sleep(10)
                thread.newproxy()
                thread.getcsrf()
            elif req.status_code == 200 and thread.raw_captcha_type == "GROUP_WALL_POST" and "buildersClubMembershipType" in req.text:
                thread.log(f"Successfully posted message [{thread.groupMessage.strip()}]", "green")
                return False
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
    created = False
    while not created:
        try:
            with thread.session.post("https://auth.roblox.com/v2/signup", json=gen_data) as req:
                if req.status_code == 200:
                    thread.log("Account generated successfully!", "green")
                    rsec = re.findall(r'\.ROBLOSECURITY=(.+); domain=\.roblox\.com;', req.headers["set-cookie"])

                    thread.status = 1

                    temp_cookie = open('cookies.txt', 'a')
                    temp_cookie.writelines(rsec[0]+"\n")
                    temp_cookie.close()

                    temp_cookie = open('upc.txt', 'a')
                    temp_cookie.writelines(thread.username+":"+thread.password+":"+rsec[0]+"\n")
                    temp_cookie.close()

                    created = True

                    thread.cookie = rsec[0]
                    
                    if thread.verify:
                        await verifyEmail(thread)
                    else:
                        return True

                elif "Token Validation Failed" in req.text:
                    thread.newproxy()
                    await asyncio.sleep(5)
                    
        except requests.exceptions.ProxyError:
            thread.newproxy()

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
        #print(solve_captcha.text)
        if (solve_captcha_json.get("id") is not None):
            task_created = True
            continue
        elif (solve_captcha_json.get("code") is not None):
            code = solve_captcha_json["code"]
            if code == 17:
                thread.log("Task limit reached, waiting 10 seconds.", "red")
                await asyncio.sleep(10)
            elif code == 24:
                thread.log(f"Public key ({thread.raw_captcha_type})[{thread.captcha_type}] blacklisted, please do not use this feature until key is whitelisted.", "red")
                exit()
            else:
                thread.log(solve_captcha_json["message"], "red")
                exit()

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
    


