### Intro

Welcome to the friendly app. Is a simplistic micro-social app where registered
user can post content and like/unlike posts from others.

### Decisions

- I considered having thin API layer with little business logic with the view
that clients using the APIs should implement most of the business logic and
call the respective API depending on the need.

- I use docker for development and production. I also use Django and
djangorestframework backed by Postgresql database. For async tasks, I have
celery with redis as a broker.

- Allow only signed up users to create posts and either like or unlike them.

- I was majorly guided by the requirements list and did not go deeper on some
product design decisions eg should we categorize posts, can an author like
their own post, can we effectively delete posts and users etc.

### Endpoints

| url              | method | parameters                                 | description                     |
| :--------------- | :----: | :----------------------------------------- | :------------------------------ |
| `user/`          | `POST` | Required `username`, `email`, `password`   | Create a user                   |
| `user/{id}/`     | `GET`  | Required `id`                              | Fetch a user by their id        |
| `post/`          | `POST` | Required `content`                         | Create a post                   |
| `post/{id}/`     | `GET`  | Required `id`                              | Fetch a post by its id          |
| `login/`         | `POST` | Required `username`, `password`            | Login user                      |
| `logout/`        | `POST` | None                                       | Logout user                     |
| `likes/{id}/`    | `GET`  | Required `id`                              | Like/Unlike a post given its id |

### Access the App

- `git clone https://github.com/gabeno/friendly.git`

_For Development environment_

- Run app: `docker compose up --build -d`
- Flush database: `docker compose exec api python manage.py flush --no-input`
- Run database migrations: `docker compose exec api python manage.py migrate --no-input`
- View logs: `docker compose logs {db,api,celery,redis}` choose one service to
view related logs or omit all of them to view all logs. Optionally add
`--follow` to tail logs. Helpful if checking logs for a service.

Test the endpoints via postman or curl or httpie.

Other helpful commands are:

- Access shell: `docker compose exec api python manage.py shell`
- Inspect database: `docker compose exec db psql -Ualluma -dfriendly_dev`
- Create migrations: `docker compose exec api python manage.py makemigrations api`
- Stop service: `docker compose down -v`

_For Production environment_

- Run app: `docker compose -f docker-compose.prod.yml up --build -d`
- Run migrations: `docker compose -f docker-compose.prod.yml exec api python manage.py migrate --noinput`
- Run tests: `docker compose -f docker-compose.prod.yml exec api pytest`

At this point the service is up and is accessible via `http://localhost:8000`.
One may check out the endpoints as listed above.

- Stop service: `docker compose -f docker-compose.prod.yml down -v`

### Challenges

- I have not extensively worked with Django before so learnt a lot of things
about it as I tackled this. I do hope the api is django-esque :)
Some interesting things I now know are serializers and their usage, the
special user model, and models relationships.

### Next Steps

This list includes things that would be nice to have:

- A more elaborate product design roadmap and implementation
- Logging and metrics
- Choose a standard way to return response objects to easen clients
implementations eg [json-api](https://jsonapi.org/) or prior in-house art.
- e2e tests with seeded database plus unit tests running in a CI build pipeline
- Add API documentation with Swagger or a viable alternative
- Deploy with a load balancer sitting on top of the app layer eg with kubernetes
