from typing import List, Tuple
import pandas as pd
import numpy as np

from src.data import get_data_from_df

def test():
    # Excelファイルを読み込む
    df: pd.DataFrame = pd.read_excel("data/sensyn.xlsx")

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