##Online Judge by Yomin
###Environmental requirements
- Python2.7
- Databases: sqlite or mysql
- flask
- flask extensions: flask login, sqlalchemy, flask-sqlalchemy, flask-wtf
- others: [lorun](https://github.com/lodevil/Lo-runner) (A moudle that tests your source code is right or not)

###How to run Online Judge
1. $ git clone git@github.com:RominYue/OnlineJudgeSystem.git
2. $ python init_db.py
3. $ python run.py
4. The admin account is already given in config.py, use this account to login in the system to add some problems
5. In another terminal, run judging.py
6. Open browser, 127.0.0.1:5000, the syetem is running