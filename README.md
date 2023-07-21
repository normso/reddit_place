Fill the data.json file with the auth token of the accounts
And pixels field with the pixels you want to fill 

### Requirements

1. python 


### Install packages before run

```bash
pip install requests
pip install pytest-playwright
playwright install chromium
```

### Steps to use the bot

1. Put accounts username and password in accounts.json
2. Run the auth.py script to generate auth token for each accounts in the accounts.json (Note :- this step does not to be run every time only if token get expire or after every 6-8 hr to just refersh the new tokens).
```bash
python auth.py
```
3. Finally run the place.py script to place the tiles.
```bash
python place.py
```
4. To close the script just press Ctrl+c


