# Mini-Amazon
CS 316 mini Amazon project

### Deployment

The server is deployed on a virtual machine. Please visit the address http://vcm-16419.vm.duke.edu:5000
to access the Mini-Amazon site.

### To run the code:  
If you would like to run the server + site locally, follow these steps.
1. Clone the Repo  
2. Create a virtual environment using the `requirements.txt` file in our repo (use pip3)
3. Run `python seed_db.py` to import our tables to the database
4. Run the line `export FLASK_APP=app.py` in your terminal
5. Type `flask run` into your terminal/command line  
6. Open up the site on your browser (address is `localhost`, port is `5000`)

Note: you can check the `mini_amazon.log` file, which logs some of the user requests to the server if you
run the server locally.

### Users
There are a couple of users set up which you can access. Otherwise, you can also register your
own user upon entering the site.

Example Standard User:
```
username: test
password: 123
```

Example Seller:
```
username: test3
password: 123
```
