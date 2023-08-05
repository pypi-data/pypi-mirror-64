from abc import ABCMeta, abstractmethod
import pandas as pd
from athena_pkg.AthenaQueryEngine import AthenaQueryEngine

class QueryEngineFactory:
    @staticmethod
    def get_query_engine(query_engine):
        if query_engine == 'ATHENA':
            return AthenaQueryEngine()
        # elif query_engine == 'ANOTHER_FUCKING_ENGINE':
        #     return AnotherFuckingQueryEngine()
        else:
            raise AssertionError('Sorry this query engine is not taken into account')
class IQueryEngine(metaclass=ABCMeta):
    @abstractmethod
    def connect(self, config):
        """Method that return the object it self"""
    @abstractmethod
    def get_calendars(self, columns):
        """Returns the whole DataFrame of the calendars
         data"""
    @abstractmethod
    def get_listings(self, columns):
        """Returns the whole DataFrame of the listings data"""
    @abstractmethod
    def number_of_available_nights(self, date):
        """Returns numbers of available nights for a specific date"""