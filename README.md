# Friday-AI
**Friday - A python based AI Personal Assistant based on the Movie "Iron Man"**

To run, from terminal in the project folder type "python main.py"

It uses OpenAI's GPT-3 to answer questions and also caches the questions for later usage and enlargement of its memory. It also has some pre-loaded question answer sets of various general knowledge MCQ's and trick questions.
To store the data, it uses SQLITE which also allows it to question the user about similar queries and sort the most accepted prediction for next time.
It takes input directly by voice also if internet is not available its can take text input from the user as currently available offline voice recognition libraries are not efficient.

**Dont froget to change the API key of OpenAI in brain.py**.

You can get your API from here https://openai.com/api/.

The API is almost free, I mean its a toy not a production level application so their free tier should be enough. Have fun!
