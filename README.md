# E-commerce-api
#### Training project for FastAPI learning
# Development
### Add project files
```
cd existing_repo
git init 
git remote add origin git@github.com:alex22201/e-commerce-api.git
git checkout -b develop
git pull origin develop
```
### Create .env file
```
DATABASE_NAME='database.sqlite3'
FILEPATH='./static/images/'
ENVIRONMENT=local # develop, prod
SECRET='19fd4e8a741546eec75095ade223a4084ba09990'
```

### Install development requirements
```
make install
```
### Build package
```
make package
```
### Remove build and cache files
```
make clean
```
### QA
#### Linting
```
make lint
```
##  Start project

```
make start
```
