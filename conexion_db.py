import pyodbc as podbc

class SQLServerConnector:
    def __init__(self, driver, server, database, password, trusted_connection="Yes", username = "sa", timeout = 120 ):
        self.driver = driver
        self.server = server
        self.database = database
        self.trusted_connection = trusted_connection
        self.username = username
        self.password = password
        self.timeout = timeout
    
    def connect(self):
        connection_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};'
        # Intentar la conexión
        connection = podbc.connect(connection_str, timeout=self.timeout)
        return connection
        # connection = podbc.connect(
        #     Trusted_Connection=self.trusted_connection,
        #     Driver=self.driver,
        #     Server=self.server,
        #     Database=self.database
            
        # )
        # return connection

