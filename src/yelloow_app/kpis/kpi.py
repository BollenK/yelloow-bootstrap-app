from datetime import datetime
from typing import Any, List

import pandas as pd

from yelloow_models import enums
from yelloow_models.models import Date, Value
from yelloow.shared.organisation.crud import get_organisation_by_name

from .interfaces import IKPI


class BaseKPI(IKPI):
    """
    Base class for KPIs that are based on a pandas dataframe. It provides some  
    helper methods to transform the data into a list of Value objects. 
    """
    default_start_dt: datetime = datetime.strptime("20220101", "%Y%m%d")

    def __init__(self, kpi_id: int, organisation_name: str, session) -> None:
        """
        :param kpi_id: The id of the KPI
        :param organisation_name: The name of the organisation
        :param session: The database session
        """
        super().__init__()
        self.kpi_id = kpi_id
        self.organisation_name = organisation_name
        self.session = session

    def get_data(self, from_dt: datetime, till_dt: datetime) -> List[Value]:
        """
        :param from_dt: The start date of the data
        :param till_dt: The end date of the data
        :return: A list of Value objects
        """
        raise NotImplementedError()

    def transform_data(self, data: Any) -> List[Value]:
        """
        :param data: The data to transform
        :return: A list of Value objects
        """
        raise NotImplementedError()

    def set_schedule(self):
        raise NotImplementedError()

    def transform_data_from_df(
        self, data: pd.DataFrame, value_amount_column: str
    ) -> List[Value]:
        """
        :param data: The data to transform
        :param value_amount_column: The name of the column that contains the
        value amount
        :return: A list of Value objects
        """
        values: List = []
        organisation_id: int = get_organisation_by_name(
            self.session, self.organisation_name
        ).id

        for idx, row in data.iterrows():
            value_datetime = idx
            values.append(
                Value(
                    date_id=Date.get_date_key_by_datetime(value_datetime),
                    #  TODO: Make this dynamic
                    value_type=enums.ValueType.REVENUE,
                    amount=float(row[value_amount_column]),
                    kpi_id=self.kpi_id,
                    organisation_id=organisation_id,
                )
            )
        return values

    def get_date_range_slice_from_df(
        self,
        from_dt: datetime,
        till_dt: datetime,
        data: pd.DataFrame,
        dt_column: str,
    ) -> pd.DataFrame:
        """
        :param from_dt: The start date of the data
        :param till_dt: The end date of the data
        :param data: The data to slice
        :param dt_column: The name of the column that contains the datetime
        :return: A slice of the data
        """ 
        mask = (data[self.dt_column] > from_dt) & (
            data[self.dt_column] <= till_dt
        )
        return data.loc[mask]
