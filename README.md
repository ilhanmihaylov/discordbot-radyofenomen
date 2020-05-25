# Discord Bot for Radyofenomen

Discord Bot plays Radyofenomen at voice channels built with Python on top of ```Discord.py```

Installation
------------
1. Install ```ffmpeg``` for your operating system.
2. Install ```Python 3.6``` for your operating system.
3. Install ```pip``` for ```Python 3.6```
4. (Optional) Create Virtual Environment
5. Install dependencies with ```pip```.
    ```sh
    pip install -r requirements.txt
    ```
6. Create Discord Bot and retrieve Token.
7. Edit ```secrets.py``` and put your Token on placeholder.
8. Run ```main.py```


Docker Installation
------------
1. Create Discord Bot and retrieve Token.
2. Edit ```secrets.py``` and put your Token on placeholder.
3. Build Docker Image From Dockerfile ```docker build . -t fenomenbot```
4. Run Container From Image ```docker run -d --name fenomen fenomenbot```