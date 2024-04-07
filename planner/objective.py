import cvxpy as cp

def get_flat_arrangement_objective(x: cp.Variable) -> cp.Expression:
    """ Objective = |sum of table1 - sum of table2| + |sum of table2 - sum of table3| + ... + |sum of tableN - sum of table1|

    Args:
        x (cp.Variable): x shape = (table_num, target_participants_num)

    Returns:
        cp.Expression: cvxpy objective
    """
    table_num = x.shape[0]
    return cp.Minimize(
        cp.sum(
            [cp.abs(cp.sum(x[i, :]) - cp.sum(x[i + 1, :])) for i in range(0, table_num - 1)]
        ) \
        +cp.abs(cp.sum(x[table_num - 1 , :]) - cp.sum(x[0, :]))
    )   
