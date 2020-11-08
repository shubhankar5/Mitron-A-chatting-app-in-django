# Mitron: A chatting app in django
A chatting application to add friends and chat in text and image messages which are encrypted to ensure your secrecy.    

[Start page](https://github.com/shubhankar5/Mitron-A-chatting-app-in-django/blob/main/screenshots/start.png)  | [Admin Page](https://github.com/shubhankar5/Mitron-A-chatting-app-in-django/blob/main/screenshots/admin.png)
:-------------------------:|:-------------------------:
| Start page               |  Admin Page |    
  
## Key features
* REST API with PostgreSQL database and easy to understand admin page
* AJAX message system which provides a good user experience
* AES encrypted text messages so that the secrecy of the messages are ensured
* Responsive front-end    
  
## Tools used and their functionality
* **Django & Python:** It handles the backend and runs a server in Python.
* **HTML, CSS & Javascript:** They handle the front-end which is integrated into Django as templates.
* **Bootstrap:** For styling the front-end.
* **jQuery & AJAX:** To handle the messaging and notification modules along with all the asynchronous requests for example in the search bar.
* **EmojioneArea:** To include the emoji feature in chatting. This repository is available [here](https://github.com/mervick/emojionearea)    
  
## How to use?
1. Install pip from this [link](https://pip.pypa.io/en/stable/installing/)
2. Install virtualenv from this [link](https://virtualenv.pypa.io/en/latest/installation.html)
3. Create a virtualenv and activate it. Refer [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)  
4. Create a directory called chat_app and save all the folders and files in it
5. Change the directory to chat_app
5. pip install -r requirements.txt
6. Create a superuser using:  python manage.py createsuperuser
7. Enter the superuser details in DATABASES which is located in settings.py   
8. python manage.py makemigrations
9. python manage.py migrate
10. python manage.py runserver  
  
**Note:** Enter your email address and app password(needs to be generated in Gmail) in settings.py to use the password reset feature in this project.    
  
## How to contribute?
Feel free to contribute to this repository and make this a better project. Thank you!  
**Fields to improve in this project:**  
* Encryption and decryption of text messages
* Image encryption has not been used yet
* Improvement in UI/UX
* Session handling
* New features
