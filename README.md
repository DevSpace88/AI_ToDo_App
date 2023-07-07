# AI_ToDo_App

# A TodDo CRUD App that is connected to OpenAI via LangChain and chroma_db. 
Basically you ask in the AI-Field a question related to Django, then the Django-Chatbot will give you an answer of steps, that will be automatically saved in your ToDo List as a Task with severals Steps.
You can still change the steps /todos dynamically afterwards. You can also just use the normal todo form field without AI.

![grafik](https://github.com/DevSpace88/AI_ToDo_App/assets/102557040/8b4a9a98-5b4a-4be9-add3-7db002a80dde)


![grafik](https://github.com/DevSpace88/AI_ToDo_App/assets/102557040/5cec5087-6d01-4adb-9e2b-b69882b80e0c)


first you have to run `db_builder.py`

then create a `.env` with your openAI secret key in it:
`OPENAI_API_KEY = "sk-blablabla"`

then manage.py runserver etc.

