import quickfix as fix
import quickfix42 as fix42


class Application(fix.Application):
    def __init__(self):
        super().__init__()
        self.sessionID = None

    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")
        self.sessionID = sessionID

    def onLogon(self, sessionID):
        print(f"Logon: {sessionID}")
        self.send_order()

    def onLogout(self, sessionID):
        print(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        print(f"To Admin: {message}")

    def fromAdmin(self, message, sessionID):
        print(f"From Admin: {message}")

    def toApp(self, message, sessionID):
        print(f"To App: {message}")

    def fromApp(self, message, sessionID):
        print(f"From App: {message}")

    def send_order(self):
        order = fix42.NewOrderSingle()

        # 设置字段
        order.setField(fix.ClOrdID("ORDER_001"))
        order.setField(fix.HandlInst(fix.HandlInst_AUTOMATED_EXECUTION_ORDER_PRIVATE_NO_BROKER_INTERVENTION))  # 1 = 自动执行，代表 Best Execution
        order.setField(fix.Symbol("AAPL"))
        order.setField(fix.Side(fix.Side_BUY))  # 1 = Buy
        order.setField(fix.TransactTime())
        order.setField(fix.OrdType("2"))  # 2 = Limit

        order.setField(fix.OrderQty(100))
        order.setField(fix.Price(150.50))
        order.setField(fix.TimeInForce("0"))  # 0 = Day

        fix.Session.sendToTarget(order, self.sessionID)
        print("Order sent.")


if __name__ == "__main__":
    settings = fix.SessionSettings("clients/local.cfg")
    app = Application()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(app, storeFactory, settings, logFactory)

    try:
        initiator.start()
        input("Press <ENTER> to quit.\n")
        initiator.stop()
    except Exception as e:
        print(e)
