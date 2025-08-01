import quickfix as fix


class Application(fix.Application):
    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        print(f"Logon: {sessionID}")

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
