
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
3. Fill the data.json with pixels data in the pixels key (Refer to Color palatte section for color names available).Put as many as pixel
    For example:-
    ```json
    "pixels":[
        {"x":234,"y":456,"color":"red"}
    ]
    ```
    x => x position of pixel , y => y position of pixel ,color => color of the pixel

4. Finally run the place.py script to place the tiles.
    ```bash
    python place.py
    ```
5. To close the script just press Ctrl+c

### Color Palatte current available 

1. orange
2. yellow
3. dark_green
4. light_green
5. dark_blue 
6. blue
7. light_blue
8. dark_purple
9. purple
10. light_pink
11. brown
12. black
13. gray
14. light_gray
16. white




