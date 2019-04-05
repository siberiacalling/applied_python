from .user import User
from .comment import Comment
from .post import Post
from .blog import Blog
import pymysql


class Blogs:
    @staticmethod
    def get_connection():
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='root',
                                     db='mydb',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def __init__(self):
        self.connection = self.get_connection()
        self.user = User(self.connection, self)
        self.blog = Blog(self.connection, self)
        self.post = Post(self.connection, self)
        self.comment = Comment(self.connection)
        self._session = None
        self.current_user = None

    def auth(self, login, password):
        self._session = self.user.authorization(login, password)
        self.current_user = self.user.get(self._session)
