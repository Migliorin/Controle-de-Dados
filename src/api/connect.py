import mysql.connector

class Connect():
    def __init__(self, host:str, user:str, password:any, database=None, port=3306) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

        self.connection = None
        self.start_connection()

    def start_connection(self) -> None:
        try:
            if(self.database is None):
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port 
                )
            else:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port 
                )

            print("###### Sucessflly connected ######")
        except mysql.connector.Error as error:
            if(self.database is None):
                raise Exception(f"Failed to stable connection with {self.user}@{self.host}:{self.port}\nError: {error}")
            else:
                raise Exception(f"Failed to stable connection with {self.user}@{self.host}:{self.port} -> Database: {self.database}\nError: {error}")
            
    
    def _is_open_connection(func):
        def _decorator(self,*args,**kwargs):
            if(self.connection is None):
                raise Exception("###### Start a connection to start send commands ######")
            if(self.connection.is_connected()):
                return func(self,*args,**kwargs)
            else:
                raise Exception("###### Connection is not established ######")
            
        return _decorator



    @_is_open_connection
    def close(self) -> None:
        print(f"###### Closing connection ######")
        self.connection.close()
        print(f"###### Connection closed ######")



class AbstractConnect():
    def __init__(self,connection:Connect) -> None:
        self.connection = connection.connection
        self.connection_class = connection