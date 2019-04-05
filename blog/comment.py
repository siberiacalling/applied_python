from pymysql.err import IntegrityError

class Comment:
    def __init__(self, connection, blogs=None):
        self._connection = connection
        self._cursor = connection.cursor()
        self._blogs = blogs

    def check_authorization(self):
        if not self._blogs.current_user:
            raise RuntimeError("User is not authorized")

    def get_comments_under_post(self, post_id):
        sql = "SELECT * FROM Comment WHERE Post_id=%s"
        self._cursor.execute(sql, post_id)
        return self._cursor.fetchall()

    def create_comment_under_post(self, post_id, text):
        self.check_authorization()
        sql = "INSERT INTO Comment (Post_id, User_id, data) " \
              "VALUES (%s, %s, %s)"
        try:
            self._cursor.execute(sql, (post_id, self._blogs.current_user["User_id"], text))
        except IntegrityError:
            raise ValueError("Post with such id doesn\'t exist")

    def create_comment_under_comment(self, comment_id, text):
        self.check_authorization()
        sql = "INSERT INTO Comment (Comment_id, User_id, data, Post_id) " \
              "VALUES (%s, %s, %s, (SELECT Post_id FROM Comment c WHERE c.id=%s))"
        try:
            self._cursor.execute(sql, (comment_id, self._blogs.current_user["User_id"], text, comment_id))
        except IntegrityError:
            raise ValueError("Comment with such id doesn\'t exist")