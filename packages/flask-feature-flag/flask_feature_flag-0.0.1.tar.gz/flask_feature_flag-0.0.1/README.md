# Flask feature flag

Tool to activate and deactivate project functionalities

[![pipeline status](https://gitlab.com/terminus-zinobe/flask-feature-flag/badges/master/pipeline.svg)](https://gitlab.com/terminus-zinobe/flask-feature-flag/-/commits/master) [![coverage report](https://gitlab.com/terminus-zinobe/flask-feature-flag/badges/master/coverage.svg)](https://gitlab.com/terminus-zinobe/flask-feature-flag/-/commits/master)

## Environment
- Create
    ```shell
    $ python3 -m venv venv
    ```
- Activate
    ```shell
    $ source venv/bin/activate
    ```
- Deactivate
    ```shell
    $ deactivate
    ```

## Package installation
- Installation
    ```shell
    $ pip3 install flask-feature-flag
    ```

- You should add this to your `config.py`
    ```python
    FEATURE_FLAGS = {
        'ROUTE_ENABLED': os.environ.get('ROUTE_ENABLED', True)
    }
    ```
    `FEATURE_FLAGS` is  required