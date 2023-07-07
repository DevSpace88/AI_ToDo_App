# AI_ToDo_App

# A TodDo App that is connected to OpenAI via LangChain and chroma_db. 
Basically you ask in the AI-Field a question related to Django, then the Django-Chatbot will giv you an answer, of steps that will be automatically saved in your ToDo List as a Task.
You can still change the todos dynamically afterwards. You can also just use the normal todo form field without AI

![grafik](https://github.com/DevSpace88/AI_ToDo_App/assets/102557040/74c9d03a-11fc-4532-9f31-0d1f593a65dd)


![grafik](https://github.com/DevSpace88/AI_ToDo_App/assets/102557040/08f3f2c8-d4c4-42d0-b5b7-541808f7b80d)

first you have to run `db_builder.py`

then create a `.env` with your openAI secret key in it:
`OPENAI_API_KEY = "sk-blablabla"`

then manage.py runserver etc.

