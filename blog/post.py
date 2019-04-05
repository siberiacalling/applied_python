class Post:
    def __init__(self, connection, blogs=None):
        self._connection = connection
        self._cursor = connection.cursor()
        self._blogs = blogs

    def check_authorization(self):
        if not self._blogs.current_user:
            raise RuntimeError("User is not authorized")

    def create(self, post_name, blogs_id, text):
        self.check_authorization()
        for blog_id in blogs_id:
            if not self._blogs.blog.get(blog_id):
                raise ValueError("One of blogs doesn\'t exists.")
        sql = "INSERT INTO Post (headline, User_id, text) " \
              "VALUES (%s, %s, %s, %s)"
        self._cursor.execute(sql, (post_name, self._blogs.current_user["User_id"], text))

        sql = "SELECT LAST_INSERT_ID() as id"
        self._cursor.execute(sql)
        post_id = self._cursor.fetchone()["User_id"]
        sql = "INSERT INTO Post_list (Blog_id, Post_id) VALUES (%s, %s)"
        for blog_id in blogs_id:
            self._cursor.execute(sql, (blog_id, post_id))

    def edit(self, post_id, new_name, new_data):
        self.check_user_rights(post_id)
        sql = "UPDATE Post SET post_name=%s, data=%s WHERE id=%s"
        self._cursor.execute(sql, (new_name, new_data, post_id))
        if not self._cursor.rowcount:
            raise ValueError("No blog with such id")

    def delete(self, blog_id):
        self.check_user_rights(blog_id)
        sql = "UPDATE Post SET deleted=True WHERE id=%s"
        self._cursor.execute(sql, blog_id)
        if self._cursor.rowcount:
            raise ValueError("No blog with such id")

    def check_user_rights(self, post_id):
        self.check_authorization()
        sql = "SELECT User_id FROM Post WHERE id=%s"
        self._cursor.execute(sql, post_id)
        if self._cursor.rowcount:
            post_user = self._cursor.fetchone()
            if not post_user["User_id"] == self._blogs.current_user["id"]:
                raise ValueError("Only owner can modify blog.")
        else:
            raise ValueError("No Blog with such name")