# tools-efl-coach 🧰
Prototype for **Tools.EFL.Coach** ("TEFLC"), a concept for a subdomain of my site [EFL.Coach](https://efl.coach/). This project intends to provide English as a Foreign Language (EFL) teachers with a platform to teach vocabulary lists with dynamically-generated activities and materials. 


![Creating a wordlist](/TEFLC/static/screenshots/creating_a_wordlist.gif "Creating a wordlist")
*To peruse all screeenshots of this project, please navigate to [/TEFLC/static/screenshots](https://github.com/chris-p-schneider/tools-efl-coach/tree/main/TEFLC/static/screenshots)*


# User Features 📚
- **Interactive web-apps for teaching vocabulary**
  - "No Prep Apps" accessible without login _(pictured above)_
  - "Vocabulary Apps" use connected user word lists (requires login) _(pictured above)_
  - "Print Apps" allow generating printable assets for lessons
- Customizable user account profile pictures _(pictured above)_
- Custom editable word lists _(pictured above)_


# Featured Web-Apps 💻
- **[Poggle](https://github.com/chris-p-schneider/tools-efl-coach/blob/main/TEFLC/static/screenshots/6_poggle.jpg)**: Boggle clone that generates boards with a pausable timer _(pictured below)_
- **[Visual Story Generator](https://github.com/chris-p-schneider/tools-efl-coach/blob/main/TEFLC/static/screenshots/6_visual_story_generator.jpg)**: generates story prompts via [Lorem Picsum](https://picsum.photos/)
- **[Unscramble](https://github.com/chris-p-schneider/tools-efl-coach/blob/main/TEFLC/static/screenshots/7_unscramble.jpg)**: mini-game that scrambles active word list and records high scores _(pictured below)_
- **[Word Lotto](https://github.com/chris-p-schneider/tools-efl-coach/blob/main/TEFLC/static/screenshots/7_word_lotto.jpg)**: a simple EFL game for young learners to practice reading and writing vocabulary _(pictured below)_
- **[Word Search Generator](https://github.com/chris-p-schneider/tools-efl-coach/blob/main/TEFLC/static/screenshots/8_wordsearch_generator.jpg)**: unlike other word searches, this one generates filler characters based on the [relative letter frequency](https://en.wikipedia.org/wiki/Letter_frequency) in the English language


![Trying some apps](/TEFLC/static/screenshots/no_prep_and_vocabulary_apps.gif "Trying some apps")


# Back End Features 🔨
- [Flask Jinja2](https://flask.palletsprojects.com/en/2.1.x/templating/) templatized HTML
- All custom HTML/CSS organized with [SMACSS](http://smacss.com/)
- Web-apps built with JavaScript and/or Python served with Flask
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) database of user information (including word lists)
- [wordInfo.py](https://github.com/chris-p-schneider/tools-efl-coach/blob/main/TEFLC/wordInfo.py) generates detailed information about a word and stores it in JSON
  - This script uses a combination of API calls ([DataMuse](https://github.com/gmarmstrong/python-datamuse/), [GoogleTrans](https://pypi.org/project/googletrans/), [ENG_to_IPA](https://pypi.org/project/eng-to-ipa/)) and web-scraping with [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- All SVG image assets created by me with [Inkscape](https://inkscape.org/)/[GIMP](https://www.gimp.org/)


# Sample Word JSON 📑
```
{
    "word": "apple",
    "wordV": 0,
    "ipa": "/ˈæpəl/",
    "audio": "https://lex-audio.useremarkable.com/mp3/apple_us_1.mp3",
    "type": "noun",
    "typeV": 0,
    "definition": "a round fruit with red, yellow, or green skin and firm white flesh",
    "definitionV": 0,
    "images": [
        "https://live.staticflickr.com/1708/24591388896_bb7bec70c1_b.jpg",
        "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?ixlib=rb-1.2.1",
        "https://purepng.com/public/uploads/large/big-red-apple-xad.png"
    ],
    "imagesV": 0,
    "imageSelected": "",
    "syllables": 2,
    "syllablesV": 0,
    "sentence": "The rotten apple injures its neighbours.",
    "sentenceV": 0,
    "related": [
        "applaud",
        "applause",
        "applet",
        "appliance",
        "applicable",
        "applicant",
        "application",
        "applied",
        "applique",
        "apply"
    ],
    "relatedV": 0,
    "synonyms": [
        "aquamarine",
        "beryl",
        "blue-green",
        "chartreuse",
        "fir",
        "forest",
        "grass",
        "jade",
        "kelly",
        "olive"
    ],
    "synonymsV": 0,
    "antonyms": [
        "experienced",
        "expert",
        "old",
        "skilled",
        "withered"
    ],
    "antonymsV": 0,
    "rhymes": [
        "appel",
        "appell",
        "chapel",
        "chappel",
        "chappell",
        "chapple",
        "grapple",
        "kappel",
        "snapple",
        "stapel"
    ],
    "rhymesV": 0
}
```

# Final Notes 📝
This project was guided by Corey Schaefer's [Flask Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) series. This was my big pandemic lockdown project and was all self-taught through YouTube, documentation, and experimentation. I learned a lot about using Python for web development and templatizing code. 

I have left most of my files unedited to include my detailed comments, concerns, and to-dos. Though I consider this project unfinished and this version limited, everything included above is functional. I hope to rebuild this project later into my current studies as a Software Development student. 
