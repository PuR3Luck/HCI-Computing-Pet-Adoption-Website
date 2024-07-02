from db_utils import sql_wrapper
from typing import List, Any

@sql_wrapper
def search(filters:List[Any]):
  raise NotImplementedError