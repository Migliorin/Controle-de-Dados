class TableQueryDefault():
    def __init__(self) -> None:
        pass


    def get_function(self,name_function:str) -> object:
        funcs_ = {
            'create_table_img_dataset': self.create_table_img_dataset,
            'fetch_image': self.fetch_image
        }
        if(name_function not in list(funcs_.keys())):
            raise Exception(f"Name not in function dict: {name_function}")
        
        return funcs_[name_function]

    def create_table_img_dataset(self,name:str) -> str:

        sql_string = f"CREATE TABLE {name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), format VARCHAR(15), width MEDIUMINT UNSIGNED, height MEDIUMINT UNSIGNED, image LONGBLOB)"

        return sql_string
    
    def fetch_image(self, table:str, column_name=[], filter_=None,type_filter='AND',operation="="):
        if(len(column_name) == 1):
            columns = f"`{column_name[0]}`"
        elif(len(column_name) == 0):
            columns = "*"
        else:
            columns = ", ".join([f"`{str(x)}`" for x in column_name])

        where_sql = None
        if(filter_ is not None):
            column = list(filter_.keys())
            property_ = [filter_[x] for x in column]

            assert len(column) == len(property_)
            assert len(column) > 0

            where_sql = "WHERE "
            for itr in range(len(column)):
                if(itr != len(column) - 1):
                    where_sql += f"`{column[itr]}` {operation} '{property_[itr]}' {type_filter} "
                else:
                    where_sql += f"`{column[itr]}` {operation} '{property_[itr]}'"

        if(where_sql is None):
            sql_string = f"SELECT {columns} FROM `{table}`"
        else:
            sql_string = f"SELECT {columns} FROM `{table}` {where_sql}"

        return sql_string