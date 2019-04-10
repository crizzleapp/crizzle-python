from crizzle import Application, AppConfig, RunMode

config = AppConfig(name='simple', runner=RunMode.RECORD)
app = Application(config)
app.run()
