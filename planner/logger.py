import logging

# カラーコードの定義
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_BLUE = '\033[94m'

def setup_logging(console_debug=False):
    # ロガーの作成
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # ログレベルを設定

    # ログのフォーマット設定
    formatter = logging.Formatter(COLOR_GREEN +  '%(asctime)s - %(levelname)s' + COLOR_RESET + '- %(message)s')

    # コンソールハンドラの作成
    console_handler = logging.StreamHandler()
    if console_debug:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)  # コンソールに出力するログレベルを設定
    console_handler.setFormatter(formatter)  # フォーマットを設定
    logger.addHandler(console_handler)  # ハンドラをロガーに追加

    return logger

def logger_divider(logger):
    # ハイフンの数を自動で決定
    message = 'This is a message'  # ダミーメッセージ
    message_length = len(logger.handlers[-1].formatter.format(logging.LogRecord('', 0, '', 0, message, (), None))) + 30
    
    logger.info(COLOR_BLUE +  '-' * message_length + COLOR_RESET)  # 区切り線をログに出力する

def colored_logger_info(logger, string, color):
    if color == "red":
        logger.info(COLOR_RED + string + COLOR_RESET)
    elif color == "green":
        logger.info(COLOR_GREEN + string + COLOR_RESET)
    elif color == "yellow":
        logger.info(COLOR_YELLOW + string + COLOR_RESET) 
    else:
        logger.info(string)

def colored_logger_debug(logger, string, color):
    if color == "red":
        logger.debug(COLOR_RED + string + COLOR_RESET)
    elif color == "green":
        logger.debug(COLOR_GREEN + string + COLOR_RESET)
    elif color == "yellow":
        logger.debug(COLOR_YELLOW + string + COLOR_RESET) 
    else:
        logger.debug(string)

def colored_logger_warning(logger, string, color):
    if color == "red":
        logger.warning(COLOR_RED + string + COLOR_RESET)
    elif color == "green":
        logger.warning(COLOR_GREEN + string + COLOR_RESET)
    elif color == "yellow":
        logger.warning(COLOR_YELLOW + string + COLOR_RESET) 
    else:
        logger.warning(string)

def colored_logger_error(logger, string, color):
    if color == "red":
        logger.error(COLOR_RED + string + COLOR_RESET)
    elif color == "green":
        logger.error(COLOR_GREEN + string + COLOR_RESET)
    elif color == "yellow":
        logger.error(COLOR_YELLOW + string + COLOR_RESET) 
    else:
        logger.error(string)