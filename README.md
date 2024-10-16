Clone the repo to your local machine: 

```
git clone https://github.com/kiran-bsv/Amazon-SQS.git 
```

Make sure you have docker installed, if not please visit this site - [Docker Installation](https://docs.docker.com/engine/install/)

Then, open the folder and paste this in the terminal where docker-compose.yml file is located.
```
docker-compose up --build
```

Make a curl request like this in terminal
```
curl -X POST http://localhost:3000/users \
-H "Content-Type: application/json" \
-d '{
  "user": "John Doe",
  "email": "john.doe@example.com",
  "age": 30
}'

```
Since the node-service and python-consumers are running simultaneously , the valid curl request data will be forwared from server -> SQS -> consumer -> MongoDB in an instant.
