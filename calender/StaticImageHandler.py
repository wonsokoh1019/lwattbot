import logging
import tornado.web
import os
from calender.constant import FILE_SYSTEM

LOGGER = logging.getLogger("calender")


def read_file(path):
    if not path.lower().endswith(".png"):
        return None
    if not os.path.exists(path):
        return None
    with open(path, "rb") as _file:
        data = _file.read()
    return data


class StaticImageHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        """
        support post
        """
        path = self.request.uri
        LOGGER.info("request para path:%s", path)
        pos = path.find("static")
        filename = path[pos+6:]

        file_path = FILE_SYSTEM["image_dir"] + filename
        content = read_file(file_path)

        if content is None:
            raise tornado.web.HTTPError(403,
                                        "The file you accessed "
                                        "does not exist.")

        self.set_header("Content-Type", "image/png")
        self.finish(content)
