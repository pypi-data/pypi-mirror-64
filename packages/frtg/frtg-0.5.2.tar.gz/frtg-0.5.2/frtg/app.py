import frtg
import logging

logging.basicConfig(level=logging.DEBUG)

app = frtg.create_app()

if __name__ == '__main__':
    app.run(host='::', port='19191')
