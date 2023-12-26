class TableQueryDefault():
    def __init__(self) -> None:
        pass


    def create_table_img_dataset(self,name:str) -> str:

        sql_string = f"CREATE TABLE {name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), format VARCHAR(15), width SMALLINT UNSIGNED, height SMALLINT UNSIGNED, image LONGBLOB)"

        return sql_string