import pandas as pd
# from QueryEngine import IQueryEngine

# def ConnectToAthena(aws_access_key_id,aws_secret_access_key,s3_staging_dir,region_name):
#     """Returns an instance to connect you to AWS Athena via pyAthena"""
#     from pyathena import connect
#     return connect(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,s3_staging_dir=s3_staging_dir,region_name=region_name)

# class AnotherFuckingQueryEngine(IQueryEngine):
#     def __init__(self):
#         super()
#     def connect(self, config):
#         return self
#     def get_calendars(self, column):
#         return self
#     def number_of_available_nights(self, date):
#         return self
# """
# Si un jour tu as besoin d'ajouter un autre QueryEngine tu le fais de la même façon que AthenaQueryEngine .. 
# """
# if __name__ == '__main__':
#     print('You want to use athena to query your data ... then use the factory to get it')
#     QueryEngineFactory.get_query_engine(query_engine='ATHENA').connect({}).number_of_available_nights(date='2020-06-06')
#     print('You want to use AnotherFuckingEngine ... then use the factory to get it')
#     QueryEngineFactory.\
#         get_query_engine(query_engine='ANOTHER_FUCKING_ENGINE')\
#         .connect({})\
#         .get_calendars('?????????')