fampay
==============================

__Version:__ 0.0.0

Fampy Assignment

## Getting up and running


!!! note
    For setting up locally using `Docker`, check [here](docs/backend/docker_setup.md)


Minimum requirements: **pip, python3.9, poetry, redis & [PostgreSQL 11][install-postgres]**, setup is tested on Mac OSX only.

```
brew install python3 poetry libmagic postgres
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

In your terminal, type or copy-paste the following:

    git clone git@github.com:ShubhamBansal1997/fampay-backend.git; cd fampay-backend; make install

Go grab a cup of coffee, we bake your hot development machine.

Useful commands:

- `make run` - start [django server](http://localhost:8000/)
- `make deploy_docs` - deploy docs to server
- `make test` - run the test locally with ipdb
- `make docker` - setup docker and start [django server](http://localhost/)

**NOTE:** Checkout `Makefile` for all the options available and how they do it.

## API Endpoints
|Endpoint                                | Purpose                                  |
-----------------------------------------|------------------------------------------|
|/api/video                              | Video List                               |
|/api/video?offset=30&per_page=30        | Video List Paginated                     |
|/api/video?ordering=video_published_at  | Video List Sorted By published_at (ASC)  |
|/api/video?ordering=-video_published_at | Video List Sorted By published_at (DESC) |
|/api/video?search=search_term           | Search Video using title and description |
|/api/video/search?search_query=virat    | Full Text Search                         |

Note: For detailed API description refer [Postman collection](Youtube.postman_collection.json)

## Managing dependencies

### Poetry

To guarantee repeatable installations, all project dependencies are managed using [Poetry](https://python-poetry.org/). The project’s direct dependencies are listed in `pyproject.toml`.
Running `poetry lock` generates `poetry.lock` which has all versions pinned.

You can install Poetry by using `pip install --pre poetry` or by following the official installation guide [here](https://github.com/python-poetry/poetry#installation).

*Tip:* We recommend that you use this workflow and keep `pyproject.toml` as well as `poetry.lock` under version control to make sure all computers and environments run exactly the same code.

### Other tools

For compatibility, `requirements.txt` and `requirements_dev.txt` can be updated by running

```bash
poetry export --without-hashes -f requirements.txt -o requirements.txt
```

and

```bash
poetry export --without-hashes -f requirements.txt -o requirements_dev.txt --with dev
```

, respectively.


## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server.

Check out detailed server setup instruction [here](docs/backend/server_config.md).

## How to release fampay

Execute the following commands:

```
git checkout master
make test
bump2version patch  # 'patch' can be replaced with 'minor' or 'major'
git push origin master
git push origin master --tags
git checkout qa
git rebase master
git push origin qa
```

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!

Refer to [CONTRIBUTING.md][contributing]

[contributing]: http://github.com/ShubhamBansal1997/fampay-backend/tree/master/CONTRIBUTING.md
