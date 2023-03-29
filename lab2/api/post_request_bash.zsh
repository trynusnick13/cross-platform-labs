curl -X POST http://127.0.0.1:8000/movies/ -H "Content-Type: application/json"   \
-d '{"name": "Kill Bill", "director": "Quentin Tarantino", "genre": "action", "date": "2005-03-04"}'


curl -X DELETE http://127.0.0.1:8000/movies/1 -H "Content-Type: application/json"

curl -X PUT http://127.0.0.1:8000/movies/1 -H "Content-Type: application/json" -d '{"name": "Kill Bill 3", "director": "Quentin Tarantino", "genre": "action", "date": "2005-04-08"}'
