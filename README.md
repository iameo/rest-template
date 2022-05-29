#Rest-Template

#### a simple flask setup that features user authorization using time-based encrypted tokens

#### How to run:
- fork repo and clone; cd into folder on your machine
- setup a cluster on mongodb Atlas
- rename .env-example to .env and populate accordingly
- ```cmd: pip install -r requirements.txt``` to get packages for this project
- ```cmd: python slov.py```


#### Routes

TEST LIVE SERVER: [emma-sl-rest-template](https://emma-sl.herokuapp.com)

* localhost:5000/register [POST method]
  
  required json: ```{
        "first_name": "xxxx",
        "last_name":"yyyy",
        "email": "xxxx@xx.com",
        "password": "*****",
    }```

* localhost:5000/login [POST method]

    required json: ```{
        "email": "xxxx@gmail.com",
        "password": "*****"
    }```


* localhost:5000/template [GET method]

    returns templates created by current_user

* localhost:5000/template [POST method]

    required json: ```{
        "template_name": "some",
        "subject": "night",
        "body": "i stay up"
    }```

* localhost:5000/template/xx901xxxx6f36xxdbe59xxxx [GET method]

    returns current_user's template by _Id 

* localhost:5000/template/xx901xxxx6f36xxdbe59xxxx [PUT method]

    updates current_user's template by _Id

    json: ```{
            "template_name": "some",
            "subject": "night",
            "body": "i stay up"
        }```


* localhost:5000/template/xx901xxxx6f36xxdbe59xxxx [DELETE method]

    deletes current_user template by _Id 

