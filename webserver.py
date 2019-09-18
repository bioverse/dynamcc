#!/usr/bin/env python
"""
Copyright (c) 2016, Andrea Halweg-Edwards, Gur Pines, Assaf Pines, James Winkler
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of DYNAMCC nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
from os.path import dirname, join
from base64 import b64encode
from uuid import uuid4
import webbrowser
import tornado.web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line

from handlers.base_handlers import (
    IndexHandler
    )
from handlers.dynamcc_handlers import (
    Dynamcc0Handler, DynamccRHandler, ExploderHandler, Dynamcc4Handler)

class Application(tornado.web.Application):
    def __init__(self):
        DIRNAME = dirname(__file__)
        STATIC_PATH = join(DIRNAME, "static")
        TEMPLATE_PATH = join(DIRNAME, "templates")  # base folder for webpages
        RES_PATH = join(DIRNAME, "results")
        COOKIE_SECRET = b64encode(uuid4().bytes + uuid4().bytes)
        handlers = [
                (r"/", IndexHandler),
                (r"/results/(.*)", tornado.web.StaticFileHandler,
                 {"path": RES_PATH}),
                (r"/static/(.*)", tornado.web.StaticFileHandler,
                 {"path": STATIC_PATH}),
                (r"/dynamcc_0/", Dynamcc0Handler),
                (r"/dynamcc_R/", DynamccRHandler),
                (r"/exploder/", ExploderHandler),
                (r"/dynamcc_4/", Dynamcc4Handler)
                ]
        settings = {
            "template_path": TEMPLATE_PATH,
            "debug": True,
            "cookie_secret": COOKIE_SECRET,
            "login_url": "/",
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    port = int(os.environ.get("PORT", 5050))
    parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(port)
    print "Tornado started on port", port
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open("http://localhost:%d" % port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
