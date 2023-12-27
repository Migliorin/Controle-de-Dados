from src.api.connect import Connect
from src.api.connect import AbstractConnect

class Table(AbstractConnect):
    def __init__(self, connection: Connect) -> None:
        super().__init__(connection)

    @Connect._is_open_connection
    def create_table(self,table:str, column = None, property_= None, query_sql=None) -> None:
        if(self.table_exist(table)):
            raise Exception(f"The table already exists: {table}")
        
        if(column is not None) and (property_ is not None):
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

        else:
            if(query_sql is None):
                raise Exception(f"Query SQL is None: {query_sql}")
            cursor = self.connection.cursor()
            cursor.execute(f"{query_sql}")
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