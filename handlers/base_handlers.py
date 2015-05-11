from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    """Index page"""
    def get(self):
        self.render("index.html")
