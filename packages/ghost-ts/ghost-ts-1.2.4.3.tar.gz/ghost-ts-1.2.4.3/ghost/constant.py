class Constant:
    """
    常量分割对象
    """
    LINE_SEP = '#'
    FIELD_SEP = '|'
    AND_SEP = '&'
    EMPTY = ""
    DICT_SEP = "^"

    LOGIN_SUCCESS_ZERO = "0"
    LOGIN_SUECCESS = "登录成功"

    ERROR_RETURN = "错误成交回报"


class QueryField(object):
    """
    查询常量对象
    """
    REQ_POSITIONP_ROVIDER = 1
    REQ_ORDERP_ROVIDER = 2
    REQ_ACCOUNTP_ROVIDER = 3

    S_REQ_POSITIONP_ROVIDER = "1"
    S_REQ_ORDERP_ROVIDER = "2"
    S_REQ_ACCOUNT_PROVIDER = "3"
    S_REQ_SUB_QUOTE = "4"


class TsClientField:
    """
    功能号
    """
    ORDER_UPDATE = 1
    ON_ERROR = 2
    QUERY = 3
    INSERT_ORDER = 4
    CANCEL_ORDER = 5
    RSP_QRY_ACCOUNT = 6
    RSP_QRY_ORDER = 7
    RSP_QRY_POSITION = 8
    TS_CONNECT = 9
    USERLOGIN = 10
    GUOSEN_STATE = 11
    TS_DIS_CONNECT = 12

    RTN_QUOTE = 15
    SUB_PRICE_SERIES = 16
    RTN_PRICE_SERIES = 17
    UN_SUB_QUOTE = 18
    RSP_QRY_SUB_QUOTE = 19

    S_ORDER_UPDATE = "1"
    S_ONERROR = "2"
    S_QUERY = "3"
    S_INSERT_ORDER = "4"
    S_CANCEL_ORDER = "5"
    S_RSP_QRY_ACCOUNT = "6"
    S_RSP_QRY_ORDER = "7"
    S_RSP_QRY_POSITION = "8"
    S_TS_CONNECT = "9"
    S_USER_LOGIN = "10"
    S_GUOSEN_STATE = "11"
    S_TS_DIS_CONNECT = "12"

    S_BATH_ORDER = "13"
    S_SUB_QUOTE = "14"
    S_RTN_QUOTE = "15"

    S_SUB_PRICE_SERIES = "16"
    S_RTN_PRICE_SERIES = "17"
    S_UN_SUB_QUOTE = "18"

    S_RSP_QRY_SUB_QUOTE = "19"
