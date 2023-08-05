import socket
import threading
import time
from abc import ABC, abstractmethod

from ghost.util import LogEngine
from .constant import Constant, TsClientField, QueryField
from .modle import AccountsProvider, OrdersProvider, PositionsProvider, OrderUpdatedEventArgs, ErrorInfo, \
    UserLoginField, OrderState, OrderCanceledReturn, OrderRejectReturn, OrderReturn, TradeReturn, QuotesProvider, \
    QuotesSubscribe, HistoryQuoteReply, OrderTicket, Withdrawal, HistoryQutoeRequest


class SocketConnector(ABC):
    """
    socket连接对象
    """

    def __init__(self):
        self.socket = None
        self.address = ""
        self.port = 0
        self.is_stop = False
        self.is_connect = False
        self.connect_num = 0
        self.writer = None
        self.reader = None
        self.logger = LogEngine()

    def connect(self):
        """
        创建socket连接
        :return: true代表连接成功
        """
        try:
            if (not self.is_connect) and (not self.is_stop):
                self.disconnect()
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.address, self.port))
                self.socket.setblocking(True)
                self.writer = self.socket.makefile(mode="w", encoding="UTF-8")
                self.reader = self.socket.makefile(mode="r", encoding="UTF-8-sig")
                self.is_connect = True
                self.connect_num += 1
                self.fire_connect()
                self.logger.info(str.format("connect to {0}:{1}", self.address, self.port))
        except Exception as ex:
            self.logger.error(ex)

        return self.is_connect

    def send(self, message):
        """
        发送信息
        :param message:信息
        :return: 0代表发送成功
        """
        try:
            self.writer.write(message + '\n')
            self.writer.flush()
            return 0
        except Exception as ex:
            self.logger.error("send error:" + str(ex))
            return -1

    def start(self):
        """
        开启后台线程
        :return: None
        """
        if self.is_stop:
            return None

        if self.is_connect:
            return

        self.connect()
        self.start_reader()

    def start_reader(self):
        """
        开启读取线程
        :return:None
        """
        if self.is_connect:
            threading.Thread(target=self.run, name="reader", daemon=True).start()
            threading.Thread(target=self.run_timer, name="timer", daemon=True).start()

    def run_timer(self):
        """
        开启心跳线程
        :return: None
        """
        self.logger.info("timer start!")
        while not self.is_stop:
            try:
                self.send("100")
                time.sleep(0.01)
            except Exception as ex:
                self.logger.error("timer error:" + str(ex))

    def run(self):
        """
        开启后台线程
        :return: None
        """
        self.logger.info("reader start!")
        try:
            while not self.is_stop:
                try:
                    message = self.reader.readline()
                    # self.logger.info(str.format("receive:{0}", message))
                    self.message_received(message.rstrip())
                except Exception as ex:
                    self.logger.error("reader error:" + str(ex))
        except Exception as ex:
            self.logger.error("run error:" + str(ex))

        self.logger.info("reader exit!")
        self.disconnect()
        self.start()

    def stop(self):
        """
        停止后台线程
        :return: None
        """
        if self.is_stop:
            return

        self.is_stop = True
        self.disconnect()
        self.logger.info("socket stop!")

    def disconnect(self):
        """
        断开连接
        :return: None
        """
        if not self.is_connect:
            return

        try:
            self.is_connect = False
            self.writer.close()
            self.writer = None
            self.reader = None
            self.socket.close()
        finally:
            self.fire_disconnect()

    @abstractmethod
    def fire_connect(self):
        """
        连接成功回调函数
        :return:
        """
        pass

    @abstractmethod
    def fire_disconnect(self):
        """
        回调函数
        :return:
        """
        pass

    @abstractmethod
    def message_received(self, message: str):
        pass


class TraderSpi(ABC):
    @abstractmethod
    def on_ts_connected(self):
        """
        Ts连接回调函数
        :return: None
        """
        pass

    @abstractmethod
    def on_ts_disconnected(self):
        """
        TS断开回调函数
        :return:
        """
        pass

    @abstractmethod
    def on_rsp_account(self, account_provider: AccountsProvider):
        """
        资金信息查询回调函数
        :param account_provider: 资金信息对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rsp_order(self, order_provider: OrdersProvider):
        """
        订单信息回调函数
        :param order_provider:订单信息对象
        :return:
        """
        pass

    @abstractmethod
    def on_guosen_disconnected(self):
        """
        柜台断开回调函数
        :return: None
        """
        pass

    @abstractmethod
    def on_guosen_connected(self):
        """
        柜台连接回调函数
        :return: None
        """
        pass

    @abstractmethod
    def on_rsp_position(self, position_provider: PositionsProvider):
        """
        仓位查询回调函数
        :param position_provider:仓位对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rtn_order(self, order_return: OrderReturn):
        """
        订单状态变化回调函数
        :param order_return:订单回报对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rtn_order_reject(self, order_reject_return: OrderRejectReturn):
        """
        订单被决绝回调函数
        :param order_reject_return:订单被拒绝对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rtn_order_canceled(self, order_canceled_return: OrderCanceledReturn):
        """
        订单被取消回调函数
        :param order_canceled_return:订单被取消对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rtn_trade(self, trade_return: TradeReturn):
        """
        订单成交回调函数
        :param trade_return:订单成交对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rtn_error(self, error: ErrorInfo):
        """
        异常信息回调函数
        :param error: 异常信息对象
        :return: None
        """
        pass

    @abstractmethod
    def on_user_login(self, user_login: UserLoginField):
        pass

    @abstractmethod
    def fire_connect(self):
        """
        socket连接回调函数
        :return: None
        """
        pass

    @abstractmethod
    def fire_disconnect(self):
        """
        socket断开连接回调函数
        :return: None
        """
        pass

    @abstractmethod
    def on_rtn_quote(self, quotes_provider: QuotesProvider):
        """
        行情回调函数
        :param quotes_provider:行情对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rsp_sub_quote(self, quote: QuotesSubscribe):
        """
        查询订阅行情列表回调函数
        :param quote: 行情列表对象
        :return: None
        """
        pass

    @abstractmethod
    def on_rsp_history_quote(self, quote: HistoryQuoteReply):
        pass


class GhostClient(SocketConnector):
    """
    ghost客户端
    """

    def __init__(self):
        super().__init__()
        self.trader_spi = None

    def set_trader_spi(self, spi):
        self.trader_spi = spi

    @staticmethod
    def parse_with_default(number):
        try:
            return int(number)
        except:
            if "9" in number:
                return 9
            if "12" in number:
                return 12
            return -1

    def order_update(self, args):
        """
        订单更新事件
        :param args:订单更新参数
        :return: None
        """
        if args.state == OrderState.canceled or args.state == OrderState.partiallyfilledurout:
            order_canceled_return = OrderCanceledReturn(args)
            self.trader_spi.on_rtn_order_canceled(order_canceled_return)
        elif args.state == OrderState.filled or args.state == OrderState.partiallyfilled:
            order_return = OrderReturn(args)
            self.trader_spi.on_rtn_order(order_return)
            trade_return = TradeReturn(args)
            self.trader_spi.on_rtn_trade(trade_return)
        elif args.state == OrderState.queued or args.state == OrderState.received or \
                args.state == OrderState.sending or args.state == OrderState.sendfailed \
                or args.state == OrderState.sent or args.state == OrderState.unsent:
            order_return = OrderReturn(args)
            self.trader_spi.on_rtn_order(order_return)
        elif args.state == OrderState.rejected:
            order_reject_return = OrderRejectReturn(args)
            self.trader_spi.on_rtn_order_reject(order_reject_return)
        else:
            self.trader_spi.on_rtn_error(ErrorInfo([Constant.ERROR_RETURN, str(args)]))

    def message_received(self, message):
        info = message.split(Constant.DICT_SEP)

        if len(info) == 2:
            key = info[0]
            value = info[1]
        elif len(info) == 1:
            key = info[0]
            value = Constant.EMPTY
        else:
            return

        field = GhostClient.parse_with_default(key)

        if field != -1:
            if field == TsClientField.RSP_QRY_ACCOUNT:
                account_provider = AccountsProvider(value)
                self.trader_spi.on_rsp_account(account_provider)

            elif field == TsClientField.RSP_QRY_ORDER:
                order_provider = OrdersProvider(value)
                self.trader_spi.on_rsp_order(order_provider)

            elif field == TsClientField.RSP_QRY_POSITION:
                position_provider = PositionsProvider(value)
                self.trader_spi.on_rsp_position(position_provider)

            elif field == TsClientField.ORDER_UPDATE:
                args = OrderUpdatedEventArgs(value)
                self.order_update(args)

            elif field == TsClientField.ON_ERROR:
                error_info = ErrorInfo(value.split(Constant.FIELD_SEP))
                self.trader_spi.on_rtn_error(error_info)

            elif field == TsClientField.TS_CONNECT:
                self.trader_spi.on_ts_connected()
            elif field == TsClientField.TS_DIS_CONNECT:
                self.trader_spi.on_ts_disconnected()

            elif field == TsClientField.USERLOGIN:
                user_login = UserLoginField(value)
                self.trader_spi.on_user_login(user_login)

            elif field == TsClientField.RTN_QUOTE:
                quote = QuotesProvider(value)
                self.trader_spi.on_rtn_quote(quote)

            elif field == TsClientField.RSP_QRY_SUB_QUOTE:
                quote = QuotesSubscribe(value)
                self.trader_spi.on_rsp_sub_quote(quote)

            elif field == TsClientField.GUOSEN_STATE:
                if value == "0":
                    self.trader_spi.on_guosen_connected()
                elif value == "1":
                    self.trader_spi.on_guosen_disconnected()

            elif field == TsClientField.RTN_PRICE_SERIES:
                history_quote_reply = HistoryQuoteReply(value)
                self.trader_spi.on_rsp_history_quote(history_quote_reply)
            else:
                return

    def fire_connect(self):
        self.trader_spi.fire_connect()

    def fire_disconnect(self):
        self.trader_spi.fire_disconnect()


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class TraderApi:
    """
    交易api
    """

    def __init__(self):
        self.gsd_client = GhostClient()
        self.gsd_client.logger.add_file_handler("gsd_log.txt")

    def send(self, key, value):
        """
        发送数据
        :param key: 键
        :param value: 值
        :return: 0代表发送成功
        """
        return self.gsd_client.send(key + Constant.DICT_SEP + value)

    def register_front(self, address, port):
        """
        注册连接地址和端口
        :param address: 连接地址
        :param port: 端口
        :return: None
        """
        self.gsd_client.address = address
        self.gsd_client.port = port

    def init(self):
        """
        初始化线程
        :return:true代表成功
        """
        self.gsd_client.start()
        return self.gsd_client.is_connect

    def exit(self):
        """
        关闭socket，退出
        :return: None
        """
        self.gsd_client.stop()

    def req_account_provider(self):
        """
        查询账户信息
        :return: None
        """
        return self.send(TsClientField.S_QUERY, QueryField.S_REQ_ACCOUNT_PROVIDER)

    def req_order_provider(self):
        """
        查询订单信息
        :return: None
        """
        return self.send(TsClientField.S_QUERY, QueryField.S_REQ_ORDERP_ROVIDER)

    def req_position_provider(self):
        """
        查询持仓信息
        :return: None
        """
        return self.send(TsClientField.S_QUERY, QueryField.S_REQ_POSITIONP_ROVIDER)

    def register_spi(self, spi: TraderSpi):
        """
        注册回调函数
        :param spi:注册spi
        :return:None
        """
        self.gsd_client.set_trader_spi(spi)

    def req_order_insert(self, order_ticket: OrderTicket):
        """
        下单
        :param order_ticket: 订单对象
        :return: 0代表成功
        """
        return self.send(TsClientField.S_INSERT_ORDER, order_ticket.to_ts())

    def req_cancel_order(self, wd: Withdrawal):
        """
        撤单
        :param wd:撤单对象
        :return: 0代表成功
        """
        return self.send(TsClientField.S_CANCEL_ORDER, wd.to_ts())

    def req_sub_quote_list(self):
        """
        查询订阅的行情列表
        :return: 0代表成功
        """
        return self.send(TsClientField.S_QUERY, QueryField.S_REQ_SUB_QUOTE)

    def req_batch_order(self, order_list: list):
        """
        批量下单：要求资金账号是同一个
        :param order_list: 下单列表，有OrderTicket对象组成的集合
        :return: 0代表成功
        """
        if len(order_list) == 1:
            return self.req_order_insert(order_list[0])

        order_lines = list()
        account_id = ""

        for order_ticket in order_list:
            if account_id == "":
                account_id = order_ticket.account_id
            elif account_id != order_ticket.account_id:
                return -2

            order_lines.append(order_ticket.to_ts())

        return self.send(TsClientField.S_BATH_ORDER, Constant.LINE_SEP.join(order_lines))

    def req_sub_quote(self, quote: QuotesSubscribe):
        """
        订阅行情
        :param quote:订阅行情对象
        :return: 0代表成功
        """
        return self.send(TsClientField.S_SUB_QUOTE, quote.to_ts())

    def req_un_sub_quote(self, quote: QuotesSubscribe):
        """
        退订行情
        :param quote:退订行情对象
        :return: 0代表成功
        """
        return self.send(TsClientField.S_UN_SUB_QUOTE, quote.to_ts())

    def req_history_quote(self, history_quote_request: HistoryQutoeRequest):
        """
        历史行情请求查询
        :param history_quote_request: 历史行情请求对象
        :return: 发送结果，0代表成功
        """
        return self.send(TsClientField.S_SUB_PRICE_SERIES, history_quote_request.to_ts())
