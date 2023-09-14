# FastAPI MongoDB with Pydantic v2 Template

---

### Requirements:

```
docker
docker-compose
```

### How to Run:

```
cp config/.env.example config/.env
docker-compose up --build -d
```

### Tests:

```
docker exec -it boilerplate-api pytest
```

### Coverage:

```
docker exec -it boilerplate-api coverage run -m pytest
docker exec -it boilerplate-api coverage report
```

### Docs:

```
localhost:8000/docs
```

### Endpoints:

```http request
POST   /boilerplate                     # boilerplate create
GET    /boilerplate/{boilerplate_id}    # boilerplate get
PATCH  /boilerplate/{boilerplate_id}    # boilerplate update
DELETE /boilerplate/{boilerplate_id}    # boilerplate delete
GET    /boilerplate                     # boilerplate list

GET    /                                # health check
```

---
