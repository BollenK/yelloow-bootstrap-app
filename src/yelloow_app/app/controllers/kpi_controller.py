from datetime import datetime
from typing import List, Optional, Type

from sqlalchemy.orm.session import Session  # noqa

from src.yelloow_app.kpis import BaseKPI
from yelloow_models import get_latest_value_dt_by_kpi_id
from src.yelloow_app.shared import get_logger
from yelloow_models.models import Value

logger = get_logger(__name__)


class KPIController:
    def __init__(self, session: Session) -> None:
        """
        :param session: The database session
        """
        self.session: Session = session

    def udpate_kpi_data(
        self,
        kpi_id: int,
        organisation_name: str,
        kpi_class: Type[BaseKPI],
        end_dt: datetime,
        start_dt: Optional[datetime] = None,
    ):
        """
        :param kpi_id: The id of the KPI
        :param organisation_name: The name of the organisation
        :param kpi_class: The class of the KPI
        :param end_dt: The end date of the data
        :param start_dt: The start date of the data
        """
        latest_value_dt: datetime = get_latest_value_dt_by_kpi_id(
            self.session, kpi_id
        )[0]

        start_dt = (
            start_dt
            if start_dt is not None
            else latest_value_dt
            if latest_value_dt is not None
            else kpi_class.default_start_dt
        )
        kpi: Type[BaseKPI] = kpi_class(kpi_id, organisation_name, self.session)
        data: List[Value] = kpi.get_data(from_dt=start_dt, till_dt=end_dt)
        try:
            self.session.add_all(data)
            self.session.commit()
            pass
        except Exception as e:
            logger.warning("Could not save value for kpi:", e)
            self.session.rollback()
