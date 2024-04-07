from typing import List
import cvxpy as cp

def unique_existence(x: cp.Variable, flip: bool = False) -> List[cp.Expression]:
    # 各列 (e.g. 宴会のテーブルを表す)には各行の変数 (e.g. 参加者を表す)がちょうど一つ存在する
    if flip:
        num = x.shape[0]
    else:
        num = x.shape[1]
    return [cp.sum(x[:, i]) == 1 for i in range(0, num)]

def least_existence_for_rows(x: cp.Variable, minimum: int, personal_id_list: List[int]=[]) -> List[cp.Expression]:   
    return [cp.sum(x[i, personal_id_list]) >= minimum for i in range(0, x.shape[0])]

def most_existence_for_rows(x: cp.Variable, maximum: int, personal_id_list: List[int]=[]) -> List[cp.Expression]:
    return [cp.sum(x[i, personal_id_list]) <= maximum for i in range(0, x.shape[0])]

def most_row_capability(x: cp.Variable, capability: int) -> List[cp.Expression]:
    # テーブルはcapability人まで
    return [cp.sum(x[i, :]) <= capability for i in range(0, x.shape[0])]

def least_row_capability(x: cp.Variable, capability: int) -> List[cp.Expression]:
    # テーブルはcapability人以上
    return [cp.sum(x[i, :]) >= capability for i in range(0, x.shape[0])]