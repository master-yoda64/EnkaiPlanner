from typing import List
import numpy as np
import cvxpy as cp
import pandas as pd
import math

from .logger import setup_logging, logger_divider, colored_logger_info, colored_logger_debug
from .data import get_data_from_df, get_personal_ids_of_job_class
from .objective import get_flat_arrangement_objective
from .constraint import unique_existence, least_existence_for_rows, most_existence_for_rows, least_row_capability

def get_constraints(df: pd.DataFrame, x: cp.Variable, hydra_cfg) -> List[cp.Expression]:
    constraints = []
    # 参加者は一つのポジションにしか座れない
    constraints += unique_existence(x)
    # 役員は各テーブルに一人以下
    constraints += most_existence_for_rows(x=x, maximum=1, personal_id_list=get_personal_ids_of_job_class(df, hydra_cfg.data.job_class_str, 2)[0])
    # マネージャーは各テーブルに一人以上
    constraints += least_existence_for_rows(x=x, minimum=1, personal_id_list=get_personal_ids_of_job_class(df, hydra_cfg.data.job_class_str, 1)[0])
    # テーブルごとの最少人数
    constraints += least_row_capability(x=x, capability=math.floor(len(list(df.index))/hydra_cfg.data.table_num))
    return constraints

def get_objective(df: pd.DataFrame, x: cp.Variable, job_str_list: List[str]) -> cp.Expression:
    objective = 0
    # すべてのテーブルにできるだけ均等に人数を配置する
    objective += 100 * get_flat_arrangement_objective(x)
    # すべてのテーブルにできるだけ各グループの人を均等に配置する
    for job_str in job_str_list:
        objective += get_flat_arrangement_objective(x[ : ,get_data_from_df(df, [job_str]).ravel().tolist()])
    return objective

def main(cfg):
    #===================#
    # solve the problem #
    #===================#
    logger = setup_logging(console_debug=cfg.logger.console_debug)
    df: pd.DataFrame = pd.read_excel(cfg.data.xlsx_path)
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
                print(name, "name")
                if name != "":
                    print(f"テーブル{idx + 1},{name}", file=f)
 
if __name__ == "__main__":
    main()