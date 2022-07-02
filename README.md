# py-screen-capture
A python program to take an image snippet, extract meaningful text from it and store it in a database.
## Installation
1. Download python for windows: https://www.python.org/downloads/ 
2. Open a cmd prompt and run: ```python get-pip.py``` 
3. Download the zip for this repo and extract the files
4. Open a cmd prompt again, navigate to the project directory and run: ```pip install requirements.txt``` to install dependencies
## Preview
**Find a private shop**
![step1](https://user-images.githubusercontent.com/74625690/177009782-8feba27f-14d4-41a2-baa6-f7c3fcf3cd80.png)

**Right-click mouse button to open overlay**
![step2](https://user-images.githubusercontent.com/74625690/177009794-0f65fc78-febf-4e31-bf1a-fd14a4e98bda.jpg)

**Left click to drag a rectangle around the shop. Release to take snapshot**
![step3](https://user-images.githubusercontent.com/74625690/177009807-9279d174-9068-4980-99a7-d4f5360ecb3c.jpg)

**Finally, the program will pre-process the image and use ocr to extract data. The data can be edited on the form and submitted to an sqlite database.**
![step4](https://user-images.githubusercontent.com/74625690/177009818-674a9c00-fbd4-4daf-818f-e8bd67ee3409.png)
