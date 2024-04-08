from typing import List
import numpy as np
import cvxpy as cp
import pandas as pd
import math
import random

from .logger import setup_logging, logger_divider, colored_logger_info, colored_logger_debug
from .data import get_data_from_df, get_personal_ids_of_job_class, get_personal_ids_of_job_field, get_personal_ids_of_names
from .objective import get_flat_arrangement_objective
from .constraint import unique_existence, least_existence_for_rows, most_existence_for_rows, least_row_capability, most_row_capability, set_person2row, ng_pair

def get_constraints(df: pd.DataFrame, x: cp.Variable, hydra_cfg) -> List[cp.Expression]:
    constraints = []
    # 参加者は一つのポジションにしか座れない
    constraints += unique_existence(x)
    # # 役員は各テーブルに一人以下
    # constraints += most_existence_for_rows(x=x, maximum=1, personal_id_list=get_personal_ids_of_job_class(df, hydra_cfg.data.job_class_str, 2)[0])
    # 出向の人も各テーブルに一人以下
    constraints += most_existence_for_rows(x=x, maximum=1, personal_id_list=get_personal_ids_of_job_class(df, hydra_cfg.data.job_class_str, 3)[0])
    # ビスマネは各テーブルに一人以下
    constraints += most_existence_for_rows(x=x, maximum=1, personal_id_list=get_personal_ids_of_job_field(df, "bizmanage")[0])
    # devは各テーブルに3人以下
    constraints += most_existence_for_rows(x=x, maximum=4, personal_id_list=get_personal_ids_of_job_field(df, "dev")[0])
    # マネージャーは各テーブルに一人以上
    constraints += least_existence_for_rows(x=x, minimum=1, personal_id_list=get_personal_ids_of_job_class(df, hydra_cfg.data.job_class_str, 1)[0])
    # テーブルごとの最少人数
    constraints += least_row_capability(x=x, capability=math.floor(len(list(df.index))/hydra_cfg.data.table_num))
    # # 役員のテーブル固定
    print(get_personal_ids_of_names(df, ["北村 卓也"]))
    constraints += set_person2row(x, 2, get_personal_ids_of_names(df, ["北村 卓也"])[0][0])
    constraints += set_person2row(x, 3, get_personal_ids_of_names(df, ["吉井太郎"])[0][0])
    constraints += set_person2row(x, 6, get_personal_ids_of_names(df, ["上野智史"])[0][0])
    constraints += set_person2row(x, 7, get_personal_ids_of_names(df, ["塚本晃章"])[0][0])

    constraints += set_person2row(x, 2, get_personal_ids_of_names(df, ["高橋さん（みずほ銀行）"])[0][0])
    constraints += set_person2row(x, 3, get_personal_ids_of_names(df, ["赤松さん（千代田化工建設）"])[0][0])
    constraints += set_person2row(x, 6, get_personal_ids_of_names(df, ["高野さん（千代田化工建設）"])[0][0])
    #tsuka_id = get_personal_ids_of_names(df, ["塚本晃章"])[0][0]
    
    # for biz_id in get_personal_ids_of_job_field(df, "bizmanage")[0]:
    #     constraints += ng_pair(x, [tsuka_id, biz_id])


    return constraints

def get_objective(df: pd.DataFrame, x: cp.Variable, job_str_list: List[str]) -> cp.Expression:
    objective = 0
    # すべてのテーブルにできるだけ均等に人数を配置する
    objective += get_flat_arrangement_objective(x)
    # すべてのテーブルにできるだけ各グループの人を均等に配置する
    for job_str in job_str_list:
        objective += get_flat_arrangement_objective(x[ : ,get_data_from_df(df, [job_str]).ravel().tolist()])
    objective += get_flat_arrangement_objective(x[ : ,get_data_from_df(df, ["bizmanage"]).ravel().tolist()])
    objective += get_flat_arrangement_objective(x[ : ,get_data_from_df(df, ["dev"]).ravel().tolist()])
    return objective

def main(cfg):
    #===================#
    # solve the problem #
    #===================#
    logger = setup_logging(console_debug=cfg.logger.console_debug)
    df = pd.read_excel("kakutei.xlsx")
    #df: pd.DataFrame = pd.read_excel(cfg.data.xlsx_path)    
    # # 行をランダムにシャッフルする
    # #df_shuffled = df.sample(frac=1, random_state=202404).reset_index(drop=True)
    # df_shuffled = df.sample(frac=1).reset_index(drop=True)

    # # 新しいExcelファイルに出力する
    # df_shuffled.to_excel('suffled.xlsx', index=False)    
    # df : pd.DataFrame = pd.read_excel("suffled.xlsx")

    participants_num = df.shape[0]
    table_num = cfg.data.table_num
    job_field_name = cfg.data.job_field_str_list

    # settings fot cvxpy variables
    x = cp.Variable((table_num, participants_num), boolean=True)
    initial_values = np.random.choice([0, 1], size=(table_num, participants_num))  # TrueまたはFalseをランダムに選択します
    x.value = initial_values 
    # set constraints
    constraints = get_constraints(df, x, cfg)
    # set objective
    objective = get_flat_arrangement_objective(x)
    # solve the problem
    prob = cp.Problem(objective, constraints)
    # solve the problem
    prob.solve()

    #===================#
    # logging           #
    #===================#
    # logging about the problem
    logger_divider(logger)
    colored_logger_info(logger, f"number of participants: {participants_num}", color="yellow")
    colored_logger_info(logger, f"number of tables: {table_num}", color="yellow")

    _, board_names = get_personal_ids_of_job_class(df, cfg.data.job_class_str, 2)
    _, manager_names = get_personal_ids_of_job_class(df, cfg.data.job_class_str, 1)
    colored_logger_info(logger, f"Managers: {manager_names}", color="yellow")
    colored_logger_info(logger, f"Boards: {board_names}", color="yellow")    

    for idx, table in enumerate(x.value):
        table_bool: bool = table.astype(int).astype(bool)
        name_list = get_data_from_df(df, ["name"]).ravel().tolist()
        logger_divider(logger)
        colored_logger_info(logger, f"table {idx} participants: {np.sum(table_bool)}", color="yellow")
        colored_logger_info(logger, f"{[name for idx, name in enumerate(name_list) if table_bool.tolist()[idx]]}", color="yellow")

        for job_field in job_field_name:
            num = get_data_from_df(df, [job_field])[table_bool].sum()
            colored_logger_debug(logger, f"{job_field} num: {num}", color="green")
    logger_divider(logger)

    table_str = ""
    with open( "tables.txt", "w") as f:
        for table_idx in range(0, table_num):
            table_str += f"{table_idx},"
        print(table_str, file=f)

    with open("tables.csv", "w") as f:
        # logger.info the results
        for idx, table in enumerate(x.value):
            table_bool: bool = table.astype(int).astype(bool)
            for name in get_data_from_df(df, ["name"]).ravel()[table_bool]:
                if name != "":
                    ascii_code = (idx + 65 - 1) + 1
                    print(f"テーブル{chr(ascii_code)},{name}", file=f)
 
if __name__ == "__main__":
    main()