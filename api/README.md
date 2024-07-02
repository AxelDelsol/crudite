# Getting started

```shell
cd api
poetry shell
poetry install
```

# Starting the tests

```shell
pytest
```

# Running the API locally

```
fastapi dev crudite/main.py
```

With the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension, use the sample requests in requests.http to play around.

# Running the API "as in" production

```
fastapi run crudite/main.py
```