from typing import List, Tuple
import pandas as pd
import numpy as np

def get_data_from_df(
        df: pd.DataFrame,
        colunm_name: List[str]
    ) -> np.array:
    
    # DataFrameからNumPy配列に変換する 
    array = df[colunm_name].to_numpy()
    return array

def get_personal_ids_of_job_field(df: pd.DataFrame, job_field_str: str) -> Tuple[List[int], List[str]]:
    # Excelファイルを読み込む
    personal_ids = list(df[df[job_field_str] == 1].index)
    name_list = get_data_from_df(df, ["name"])[personal_ids].ravel().tolist()
    return personal_ids, name_list

def get_personal_ids_of_job_class(df: pd.DataFrame, job_class_str: str, job_class_id: int) -> Tuple[List[int], List[str]]:
    # Excelファイルを読み込む
    personal_ids = list(df[df[job_class_str] == job_class_id].index)
    name_list = get_data_from_df(df, ["name"])[personal_ids].ravel().tolist()
    return personal_ids, name_list

def test():
    # Excelファイルを読み込む
    df: pd.DataFrame = pd.read_excel("sensyn.xlsx")

    # 'name'列を除いて数値のみを含むDataFrameにする
    print(df.columns)

    # consultant, solution, develop, field, biz-managiment
    job_field_array: np.array = get_data_from_df(
        df, 
        ["consul", "sol", "dev", "field", "bizmanage"]
    )
    # DataFrameからNumPy配列に変換する
    job_class_array: np.array = get_data_from_df(
        df, 
        ["job_class"]
    )
    name_array: np.array = get_data_from_df(
        df, 
        ["name"]
    )
    print(job_field_array)
    print(job_class_array)
    print(name_array)

if __name__ == "__main__":
    test()