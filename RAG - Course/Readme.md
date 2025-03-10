
# 

Inspiration 
https://colab.research.google.com/drive/18BhYFyIUmMgBPiiF5kL70TtH1WChlwpa
Credit to course

Download a CSV FILE, 
Load the CSV File into Postgress
Do a query and save it in REDIS

Searchs and hit redis.

# REDIS

Run the container locally
```cli
docker run -p 6379:6379 redis/redis-stack-server:latest
```
You can access to it usng REDIS CLI.
->

# Postgress

Run the container locally.

POSTGRESS:

https://hub.docker.com/_/postgres


```cli
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```
The default postgresuser and database are created in the entrypoint with initdb.
Password: mysecretpassword  user: postgres   database name: postgres

You can have access to it with PG ADMIN



# Elasticsearch

## ELASTICEARCH 

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  X75eZVaxvPg=5eXc7Q*s


Run the kibana container
```cli
docker network create elastic             
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.15.2   
docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.15.2
docker pull docker.elastic.co/kibana/kibana:8.15.2               
docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.15.2
```


# Chroma DB

```
docker run -d -p 8000:8000 -v chroma-data:/chromadb/data chromadb/chroma
```

