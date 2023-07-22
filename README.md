
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
3. Fill the data.json with pixels data in the pixels key (Refer to Color palate section for color names available).Put as many as pixel
    For example:-
    ```json
    "pixels":[
        {"x":<x pos>,"y":<y pos>,"color":"<color name>"}
    ]
    ```

4. Finally run the place.py script to place the tiles.
```bash
python place.py
```
5. To close the script just press Ctrl+c

### Color Palate current available 

'''toml
orange:3
yellow:4
dark_green:6
light_green:8
dark_blue:12
blue:13
light_blue:14
dark_purple:18
purple:19
light_pink:23
brown:25
black:27
gray:29
light_gray:30
white:31 
'''



