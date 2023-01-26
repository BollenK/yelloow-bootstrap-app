import logging

from sqlalchemy import create_engine
from structlog._log_levels import INFO

from src.yelloow_app.shared.config import config
from src.yelloow_app.shared.database import Session
from src.yelloow_app.shared.log import get_logger

logger = get_logger(__name__)


def initialize_db():
    """
    :return:
    """
    engine = create_engine(
        config.DATABASE_URL,
        echo=False,
        pool_size=20,
        max_overflow=5,
        pool_pre_ping=True,
        # connect_args={"application_name": config.APPLICATION_NAME},
        pool_recycle=300,
    )

    # Bind the global session to the actual engine.
    Session.configure(bind=engine)
    logger.info("DB has been initialised")

    if config.MYSQL_LOG_SQL:
        logger.warning("SQL logging enabled")
        sa_logger = logging.getLogger("sqlalchemy.engine")
        sa_logger.setLevel(INFO)
        sa_logger.addHandler(logging.StreamHandler())

    return engine


engine = initialize_db()
