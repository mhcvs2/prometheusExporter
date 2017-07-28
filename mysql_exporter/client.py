import time
from collections import OrderedDict
import mysql.connector as mysqlconn
from mysql.connector import Error as MySQLError

class Error(Exception):pass

class MySQL(object):
    """
    MySQL represents the connection to and configuration of the MySQL
    process and its clients.
    """
    def __init__(self, db=None,user="root",password="root.123", port=None, host=None):
        self.db = db
        self.user = user
        self.password = password
        # state
        self.ip = "127.0.0.1"
        self._conn = None
        self._query_buffer = OrderedDict()
        self.port = port
        self.host = host

    @property
    def conn(self):
        """
        Convenience method for setting up a cached connection
        with the replication manager user.
        """
        if self._conn:
            return self._conn
        ctx = dict(user=self.user,
                   password=self.password,
                   timeout=25) # derived from ContainerPilot config ttl
        self._conn = self.wait_for_connection(**ctx)
        return self._conn

    def wait_for_connection(self, user='root', password=None, database=None,
                            timeout=10):
        """
        Polls mysqld socket until we get a connection or the timeout
        expires (raise WaitTimeoutError). Defaults to root empty/password.
        """
        while timeout > 0:
            try:
                if self.host and self.port:
                    return mysqlconn.connect(host=self.host,
                                             port=self.port,
                                             user=user,
                                             password=password,
                                             database=database,
                                             charset='utf8',
                                             connection_timeout=timeout)
                else:
                    sock = '/var/lib/mysql/mysql.sock'
                    return mysqlconn.connect(unix_socket=sock,
                                             user=user,
                                             password=password,
                                             database=database,
                                             charset='utf8',
                                             connection_timeout=timeout)
            except MySQLError as ex:
                timeout = timeout - 1
                if timeout == 0:
                    raise Error(ex)
                time.sleep(1)

    def add(self, stmt, params=()):
        """ Adds a new SQL statement to an internal query buffer """
        self._query_buffer[stmt] = params

    def execute(self, sql, params=(), conn=None):
        """ Execute and commit a SQL statement with parameters """
        self.add(sql, params)
        self._execute(conn, discard_results=True)

    def execute_many(self, conn=None):
        """
        Execute and commit all previously `add`ed statements
        in the query buffer
        """
        self._execute(conn, discard_results=True)

    def query(self, sql, params=(), conn=None):
        """ Execute a SQL query with params and return results. """
        self.add(sql, params)
        return self._execute(conn=conn)

    def _execute(self, conn=None, discard_results=False):
        """
        Execute and commit all composed statements and flushes the buffer
        """
        try:
            if not conn:
                conn = self.conn
        except (Error, MySQLError):
            raise # unrecoverable

        cur = None
        try:
            cur = conn.cursor(dictionary=True, buffered=True)
            for stmt, params in self._query_buffer.items():
                cur.execute(stmt, params=params)
                if not discard_results:
                    return cur.fetchall()

                # we discard results from writes
                conn.commit()
                try:
                    cur.fetchall()
                except MySQLError:
                    # Will get "InternalError: No result set to fetch from."
                    # for SET statements. We can safely let this slide if the
                    # `execute` call passes
                    pass
        finally:
            # exceptions are an unrecoverable situation
            self._query_buffer.clear()
            if cur:
                cur.close()

    def get_primary(self):
        """
        Returns the server-id and hostname of the primary as known to MySQL
        """
        result = self.query('show slave status')
        if result:
            return result[0]['Master_Server_Id'], result[0]['Master_Host']

        result = self.query('show slave hosts')
        if not result:
            raise Error('no prior replication setup found')
        return result[0]['Master_id'], self.ip

    def get_binlog(self):
        """ Gets the current binlog file name """
        results = self.query('show master status')
        binlog_file = results[0]['File']
        return binlog_file

    def get_user_connections(self):
        contents = self.query("show processlist;")
        users_repeat = [info["User"] for info in contents]
        users = set(users_repeat)
        res = {}
        for user in users:
            res[user] = users_repeat.count(user)
        return res

    def get_users(self):
        contents = self.query("select user from mysql.user;")
        users_repeat = [str(info["user"]) for info in contents if str(info["user"])]
        return set(users_repeat)