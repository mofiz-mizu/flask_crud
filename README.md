docker-compose up -d --build

# MY_SQL Connection Troubleshoot

docker exec -it mysql_db mysql -u root -p

## Check MySQL users

SELECT host, user FROM mysql.user;
SHOW GRANTS FOR 'flaskuser'@'%';

## Grant All Privileges To Flaskuser

GRANT ALL PRIVILEGES ON flask_crud.\* TO 'flaskuser'@'%';
FLUSH PRIVILEGES;
EXIT;

docker restart flask_app

# Test Connection Inside Flask Container

docker exec -it flask_app python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://flaskuser:flaskpass@db:3306/flask_crud")
engine.connect()
