from playwright.sync_api import sync_playwright
import json

def getToken(userName:str,passwd:str,context):
    page = context.new_page()
    page.goto("https://www.reddit.com/login/")
    page.locator('css=#loginUsername').fill(userName)
    page.locator('css=#loginPassword').fill(passwd)
    page.locator('css=button').get_by_text("LOG IN").click()
    with page.expect_response("https://www.reddit.com/login") as check:
        pass
    mes = page.locator('css=fieldset.m-required:nth-child(3) > div:nth-child(3)').all_text_contents()[0]
    if mes :
        context.clear_cookies()
        return (mes,False)
    with page.expect_request("https://gql.reddit.com/") as first:
        pass
    context.clear_cookies()
    return (first.value.header_value("authorization").split()[-1],True)



def main():
    accounts = []
    try:
        with open("./accounts.json","r") as f:
            accounts = json.loads(f.read())["accounts"]
    except Exception as e :
        print("Error :-",e)
        return

    if len(accounts) <= 0:
        print("There is no accounts available")
        return
    data_file_json = {}
    data_file = None
    try:
        with open("data.json") as f:
            data_file_json = json.loads(f.read().strip())      
    except OSError as e :
        print("Crating data.json => file does not exist")     
    finally:
        data_file = open("data.json","w")
        data_file_json["accounts"] = []
        if "pixels" not in data_file_json:
            data_file_json["pixels"] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        for index,account in enumerate(accounts):
            tok , ok = getToken(account["username"],account["passwd"],context)
            if ok :
                data_file_json["accounts"].append({"auth":tok,"username":account["username"]})
                print(f"({index+1}/{len(accounts)}).{account['username']} token fetched successfully")
            else:
                print(f"({index+1}/{len(accounts)}).{account['username']} token fetching failed")
        data_file.write(json.dumps(data_file_json))
        data_file.close()
        context.close()
        browser.close()

if __name__ == "__main__":
    main()

