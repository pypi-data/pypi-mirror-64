# Flask authentication service with mongo

Flask JWT authentication package with mongo.


## Installing
- Install and update using pip:
    ```shell
    $ pip3 install -U flask-auth-service-mongo
    ```

## Configuration

-   Define the following environment variables
    * Key with which the token is generated
        ```
        SECRET_KEY=
        ```
    * (bool) Turn the token whitelist on or off
        ```
        WHITE_LIST_TOKEN=
        ```
    * Minimum username length
        ```
        USERNAME_MIN_LENGTH=
        ```
    - Minimum password length
        ```
        PASSWORD_MIN_LENGTH=
        ```

## Links

- [Documentation.](https://flask-auth-service-mongo.readthedocs.io/en/latest/index.html)
