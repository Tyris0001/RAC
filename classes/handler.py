from classes.config import *
from classes.roblox import *


async def createAccount(thread):

    # first let's make sure the generated username isn't invalid
    await createUsername(thread)
    
    # now let's generate an invalid captcha id, blob 
    await createCaptcha(thread)

    # let's send the captcha id, blob to our solving service
    await captchaTask(thread)

    # once finished we'll wrap it up by finishing our account
    await finishAccount(thread)

async def loginAccount(thread):

    # let's create a captcha first since no need to check username validity
    await createCaptcha(thread)

    # now let's solve the captcha 
    await captchaTask(thread)

    # once that's done let's try and login
    await login(thread)

    # That's all folks  

async def checkCookie(thread):

  
    valid_file = open("valid.txt", "a")
    # not that much code required for a cookie checker
    thread.session.cookies.update({
        ".ROBLOSECURITY":thread.cookie
    })
    with thread.session.get("https://www.roblox.com/mobileapi/userinfo") as req:
        if req.status_code == 200:
            valid_file.write(thread.cookie+"\n")
            
            cookie_info = req.json()
            thread.username = cookie_info["UserName"]
            

            if thread.verify:
                await verifyEmail(thread)

    valid_file.close()
