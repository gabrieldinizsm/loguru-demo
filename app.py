from loguru import logger
import sys

# Log levels ordenados por severidade e verbosidade crescente
logger.trace("A trace message.")
logger.debug("A debug message.")
logger.info("An info message.")
logger.success("A success message.")
logger.warning("A warning message.")
logger.error("An error message.")
logger.critical("A critical message.")

# Criando um novo handler e colocando o log level padrão para INFO
logger.remove(0)
logger.add(sys.stderr, level="INFO")

# Criando um custom log level
logger.level("FATAL", no=60, color="<red>", icon="!!!")
logger.log("FATAL", "A user updated some information.")
