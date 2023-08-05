from athena_pkg.QueryEngine import IQueryEngine
import pandas as pd
from pyathena import connect as athena_connect

class AthenaQueryEngine(IQueryEngine):
    def __init__(self):
        self.con = None
        super()
    def connect(self, config):
        self.con = athena_connect(
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            s3_staging_dir=config.s3_staging_dir,
            region_name=config.region_name
        )
        return self
    def get_calendars(self, columns):
        return pd.read_sql("select " + columns + " from calendars", self.con)
    def get_listings(self,columns):
        return pd.read_sql("select " + columns + " from details", self.con)
    def number_of_available_nights(self, date):
        return pd.read_sql("select count(*) from calendars where date like'" + date + "'", self.con)['_col0'][0]