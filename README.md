# FastAPI MongoDB Template

---

### Requirements:

```
docker
docker-compose
```

### How to Run:

```
cp config/.env.example config/.env
docker-compose up -d
```

### Tests:

```
docker exec -it boilerplate-api pytest
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
GET    /boilerplate/list/all            # boilerplate list

GET    /                                # health check
```

---
