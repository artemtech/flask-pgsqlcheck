# flask-pgsqlcheck
flask version of xinetd for pgsqlcheck

## Build docker image
```
docker build -t flask-pgsqlcheck ./
```

## Usage
```bash
# set environment variable
nano .env
POSTGRESQL_HOST=
POSTGRESQL_DB=
POSTGRESQL_USER=
POSTGRESQL_PASS=

# run docker image
docker run -dti --name flask-pgsqlcheck --network-mode host flask-pgsqlcheck

# test hit
curl http://localhost:25432/
```

## Usage for haproxy check
```
...
frontend db-primary
    bind *:5432
    default_backend db-backend-primary

frontend db-standby
    bind *:5433
    default_backend db-backend-standby

backend db-backend-primary
    option httpchk GET / HTTP/1.1
    http-check expect status 200
    server db-01 1.2.3.4:5432 check port 25432
    server db-02 1.2.3.4:5432 check port 25432

backend db-backend-standby
    option httpchk GET / HTTP/1.1
    http-check expect status 206
    server db-01 1.2.3.4:5432 check port 25432
    server db-02 1.2.3.4:5432 check port 25432  
```
