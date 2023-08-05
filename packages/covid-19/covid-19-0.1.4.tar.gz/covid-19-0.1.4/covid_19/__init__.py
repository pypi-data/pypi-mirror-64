import gunicorn.app.base

from covid_19.api import __hug_wsgi__ as wsgi_app


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    options = {
        "bind": "%s:%s" % ("127.0.0.1", "8080"),
        "worker-class": "egg:meinheld#gunicorn_worker",
    }
    StandaloneApplication(wsgi_app, options).run()
