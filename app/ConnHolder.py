class ConnHolder(object):
    def __init__(self):
        self.conn=None
    def set_conn(self,conn):
        self.conn=conn
    def close(self):
        self.conn.close()