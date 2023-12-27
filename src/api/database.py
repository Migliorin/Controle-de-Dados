from src.api.connect import Connect, AbstractConnect

class Database(AbstractConnect):
    def __init__(self,connection:Connect) -> None:
        if(isinstance(connection,Connect)):
            super().__init__(connection)
        else:
            raise Exception(f"Connection type is not allowed: {type(connection)}. Use {Connect.__name__} class")
        

    @Connect._is_open_connection
    def create_database(self,database:str) -> None:
        if(self.database_exist(database)):
            raise Exception(f"The database already exists: {database}")
        
        else:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE {database}")
            print("###### Database create sucessfully ######")
    
    @Connect._is_open_connection
    def database_exist(self,database:str) -> bool:
        cursor = self.connection.cursor()

        cursor.execute("SHOW DATABASES")

        databases = [x[0] for x in cursor]
        return database in databases

    @Connect._is_open_connection    
    def use_database(self,database:str) -> None:
        if(not self.database_exist(database=database)):
            raise Exception(f"The database does not exists: {database}")
        else:
            cursor = self.connection.cursor()
            cursor.execute(f"USE {database}")
            print(f"###### Using database: {database} ######")
            

    