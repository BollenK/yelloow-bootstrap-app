import os
import sys

cur_path = os.getcwd()
sys.path.append(cur_path + "/src")

from src.yelloow_app.shared.database import with_db_session
from src.yelloow_app.shared.database.database import engine
from yelloow_models.models import Base



@with_db_session
def main(session):
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
