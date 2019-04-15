from crizzle import Application, AppConfig, runners
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(name)32s] [%(levelname)8s] -- %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

config = AppConfig(name='simple', runner=runners.RunMode.RECORD)
app = Application(config)
app.run()
