from src.dal.DAO.base_DAO import BaseDAO,Union,Tuple,List
class VacationsDAO(BaseDAO):
    def __init__(self):
        self.table_name = 'vacations'
        self.id_column = 'vacation_id'
    def update(self, columns: Union[tuple,str], values: Union[tuple,str], vacation_id:str):
        super().base_update(self.table_name, columns, values,self.id_column, vacation_id)
    def add(self, columns:Union[tuple,str], values:Union[tuple,str]):
        super().base_add(self.table_name,columns, values)
    def print_all(self):
        super().base_print_all(self.table_name)
    def delete_by_id(self,vacation_id:str):
        super().base_delete_by_id(self.table_name, self.id_column,vacation_id)
    def print_wanted_column_value_by_id(self,column_name:str, vacation_id:str):
        super().base_print_wanted_column_value_by_id(self.table_name, column_name, self.id_column, vacation_id)