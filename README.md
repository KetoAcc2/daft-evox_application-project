# daft-evox_application-project
------------------
# Models

For this assignment I've decided to create 3 models.

model "Message"

![image](https://user-images.githubusercontent.com/82528000/119565809-b85b1900-bdaa-11eb-9038-6e477d1d0cba.png)

This model is used to store messages into the database in appropriate form. There are three fields:
  id_message - a unique identifier of every message
  message_text - message's content
  view_counter - field storing the amount of times the message was viewed
the objects of "Message" are used directly to communicate with database

model "MessageRequestDto"

![image](https://user-images.githubusercontent.com/82528000/119567421-982c5980-bdac-11eb-9f25-fe42cf74ec21.png)

This one is used to retreive the data from request in appropriate form. As during process of making the request it isn't needed to put every single field, but needed to put the message text only. So, there is only one field - message_text.
One more thing to tell about the model is that I use @validator here which I found really useful to check whether the message is empty or not as it does validate instantly after the request was sent.

model "Message_Model"
This model is really simple and is equal to regular "Message" model, but with one field (id_message) being excluded. It is used exclusively for response in GET message.

# Authentication

![image](https://user-images.githubusercontent.com/82528000/119567914-302a4300-bdad-11eb-97bf-5556548726d3.png)

For authentication I use fastapi.security.api_key. In the beggining I specify constant API_KEY which contains string value that is the only string, can be used to authenticate. There are two ways to send api key: via query or header. None of the endpoints can be accessed without authentication. In case of trying to access the endpoint without api key or with invalid one, user will get 403 (forbidden) status code.

Link to Heroku: https://daftcode-evox-application-proj.herokuapp.com/

# Endpoints

POST('/get_openapi')

url = 'http://127.0.0.1:8000/get_openapi'

![image](https://user-images.githubusercontent.com/82528000/119568204-89927200-bdad-11eb-89b9-e011d7f6a2cd.png)

This one is not necessary endpoint but it can be useful to see the whole information about api. I won't talk about it something more.

POST('/messages')

url = 'http://127.0.0.1:8000/messages'

![image](https://user-images.githubusercontent.com/82528000/119568568-dbd39300-bdad-11eb-822d-fb5a767cb1ac.png)

This endpoint is used for sending messages to database. Here I receive an object of "MessageRequestDto" provided by the user in JSON. I create an object of "Message", by providing message_text (taken from user's input) and view_counter (always initially equal to 0) (id_message is generated automatically), and saving it to the database. As response, user gets an information that message was succesfully sent to the database and message's unique id for probable further manipulations with it. For succesful response, 201 (created) status code is sent.

PUT('/messages/{id_message}')

url = 'http://127.0.0.1:8000/messages/{id_message}'

![image](https://user-images.githubusercontent.com/82528000/119568672-06bde700-bdae-11eb-8eae-2059c316caa7.png)

This endpoint is used for updating the content of certain message (specified by id_message). Here I receive an object of "MessageRequestDto" and, additionally, id_message. At first, I get a reference to Message object from the database via id_message. Then I provide new (updated, given by the user) value to the field message_text and set value of field view_counter to zero. Finally, resaving it to the database with updated data. For succesful response, 204 (no content) status code is sent.

GET('/messages/{id_message}')

url = 'http://127.0.0.1:8000/messages/{id_message}'

![image](https://user-images.githubusercontent.com/82528000/119568839-3e2c9380-bdae-11eb-935b-7dbaebedf198.png)

This endpoint is used to retrieve the certain message (specified by id_message) to see it's content and view_counter. Here I receive id_message only. Firstly, I get a reference to Message object from the database via id_message. Then I increment value of field view_counter by 1 as user is about to have a view of the message. In the end, I save message to the database with updated counter and send response to the user in the form of Message_Model.

DELETE('/messages/{id_message}')

url = 'http://127.0.0.1:8000/messages/{id_message}'

![image](https://user-images.githubusercontent.com/82528000/119569123-9a8fb300-bdae-11eb-8434-34fefa52a129.png)

This endpoint is used to delete the certain message (specified by id_message) from the database. Here I receive id_message only. Then I get a reference to Message object via id_message and simply delete it from the database. For succesful response, 204 (no content) status code is sent.



Link to Heroku: https://daftcode-evox-application-proj.herokuapp.com/









