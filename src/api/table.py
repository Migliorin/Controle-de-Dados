from src.api.connect import Connect
from src.api.connect import AbstractConnect

class Table(AbstractConnect):
    def __init__(self, connection: Connect,table_query_default=None) -> None:
        super().__init__(connection)
        self.table_query_default = table_query_default


    @Connect._is_open_connection
    def get_value_table(self,table:str,info_: str,query_size=1,**kwargs) -> list:
        if(not self.table_exist(table)):
            raise Exception(f"The table does not exists: {table}")
        
        if(isinstance(info_,str)):
            if(self.table_query_default is None):
                raise Exception("Table query default didn't define: None")
            sql_query = self.table_query_default.get_function(info_)
            sql_query = sql_query(table,**kwargs)
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(f"{sql_query}")
            print("###### Value get sucessfully ######")

            result_query = cursor.fetchmany(query_size)

            return result_query
        
        else:
            raise Exception("Invalid format for get_value_table function")

    @Connect._is_open_connection
    def create_table(self,table:str, info_: dict) -> None:    

        if(self.table_exist(table)):
            raise Exception(f"The table already exists: {table}")
        
        if(isinstance(info_,dict)):
            column = list(info_.keys())
            property_ = [info_[x] for x in column]

            assert len(column) == len(property_)
            assert len(column) > 0

            sql_query = f"CREATE TABLE {table} ("

            for itr in range(len(column)):
                if(isinstance(property_[itr],tuple) or isinstance(property_[itr],list)):
                    sql_query += f"{column[itr]} {' '.join(property_[itr])}"
                else:
                    sql_query += f"{column[itr]} {property_[itr]}"
                if(itr != len(column)-1):
                    sql_query += ', ' 

                else:
                    sql_query += ')' 
                
            print(f"###### Creating table with SQL query: {sql_query} ######")
            cursor = self.connection.cursor()
            cursor.execute(f"{sql_query}")
            print("###### Table create sucessfully ######")

        elif(isinstance(info_,str)):
            if(self.table_query_default is None):
                raise Exception("Table query default didn't define: None")
            sql_query = self.table_query_default.get_function(info_)
            sql_query = sql_query(table)
            cursor = self.connection.cursor()
            cursor.execute(f"{sql_query}")
            print("###### Table create sucessfully ######")

    @Connect._is_open_connection
    def send_values_table(self,table:str,info:dict) -> None:
        if(not self.table_exist(table)):
            raise Exception(f"The table does not exists: {table}")
        
        columns = list(info.keys())
        values = [info[x] for x in columns]

        if(columns is not None) and (values is not None):
            assert len(columns) == len(values)
            assert len(columns) > 0

        sql_insert_blob_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))})"
        cursor = self.connection.cursor()
        print(f"###### Creating SQL query to send info: {sql_insert_blob_query} ######")
        cursor.execute(sql_insert_blob_query,tuple(values))
        self.connection.commit()
        print(f"###### Add info to table {table} sucessfully ######")


    @Connect._is_open_connection
    def table_exist(self,table:str) -> None:

        cursor = self.connection.cursor()

        cursor.execute("SHOW TABLES")

        tables = [x[0] for x in cursor]
        return table in tables