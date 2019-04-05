class Blog:
    def __init__(self, connection, blogs=None):
        self._connection = connection
        self._cursor = connection.cursor()
        self._blogs = blogs

    def get_all_blogs(self):
        sql = "SELECT * FROM Blog WHERE NOT deleted"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def check_authorization(self):
        if not self._blogs.current_user:
            raise RuntimeError("User is not authorized")

    def create(self, blog_name):
        self.check_authorization()
        sql = "SELECT * FROM Blog WHERE name=%s"
        self._cursor.execute(sql, blog_name)
        if not self._cursor.rowcount:
            sql = "INSERT INTO Blog (name, User_id) VALUES (%s, %s)"
            self._cursor.execute(sql, (blog_name, self._blogs.current_user["username"]))
        else:
            raise ValueError("Blog with such name already exists.")

    def get(self, blog_id):
        sql = "SELECT * FROM Blog WHERE id=%s AND NOT deleted"
        self._cursor.execute(sql, blog_id)
        blog = self._cursor.fetchone()
        return blog

    def get_not_deleted_blogs_auth(self):
        self.check_authorization()
        sql = "SELECT * FROM Blog WHERE User_id=%s AND NOT deleted"
        self._cursor.execute(sql, self._blogs.current_user["id"])
        return self._cursor.fetchall()

    def delete(self, blog_id):
        self.check_user_rights(blog_id)
        self.check_user_rights(blog_id)

        sql = "UPDATE Blog SET deleted=True WHERE id=%s;"
        self._cursor.execute(sql, blog_id)
        if not self._cursor.rowcount:
            raise ValueError("No Blog with such name.")

    def edit_name(self, blog_id, new_blog_name):
        self.check_user_rights(blog_id)

        sql = "UPDATE Blog SET name=%s WHERE id=%s"
        self._cursor.execute(sql, (new_blog_name, blog_id))
        if not self._cursor.rowcount:
            raise ValueError("Blog with such id doesn\'t exist")

    def check_user_rights(self, blog_id):
        self.check_authorization()
        sql = "SELECT User_id FROM Blog WHERE id=%s"
        self._cursor.execute(sql, blog_id)
        if self._cursor.rowcount:
            blog_user = self._cursor.fetchone()
            if not blog_user["User_id"] == self._blogs.current_user["User_id"]:
                raise ValueError("User has no rights to modify blog.")
        else:
            raise ValueError('Blog doesn\'t exist')

