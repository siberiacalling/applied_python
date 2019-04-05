class User:
    def __init__(self, connection, blogs=None):
        self._connection = connection
        self._cursor = connection.cursor()
        self._blogs = blogs

    def get_all_users(self):
        sql = "SELECT * FROM User"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def create(self, login, password, first_name, last_name):
        sql = "SELECT * FROM User WHERE login=%s"
        self._cursor.execute(sql, login)
        if self._cursor.rowcount:
            raise ValueError('This login {} already exists'.format(login))
        sql = "INSERT INTO User (login, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
        self._cursor.execute(sql, (login, password, first_name, last_name))

    def get(self, session_id):
        if session_id:
            sql = "SELECT u.* FROM Session s, User u WHERE s.User_id = u.User_id AND s.Session_id=%s"
            self._cursor.execute(sql, session_id)
            if self._cursor.rowcount:
                return self._cursor.fetchone()
            else:
                raise ValueError("Wrong username or password.")
        else:
            raise RuntimeError("User is not authorized")

    def authorization(self, login, password):
        sql = "SELECT * FROM User WHERE login=%s;"
        self._cursor.execute(sql, login)
        if not self._cursor.rowcount:
            raise ValueError('User with login {} doesn\'t already exist'.format(login))
        user = self._cursor.fetchone()
        if user["password"] == password:
            sql = "SET @id=UUID()"
            self._cursor.execute(sql)
            sql = "INSERT INTO Session (User_id, id) VALUES (%s, @id)"
            self._cursor.execute(sql, user["id"])
            sql = "SELECT @id as id"
            self._cursor.execute(sql)
            session_id = self._cursor.fetchone()["id"]
            return session_id
        else:
            raise ValueError("Wrong password")