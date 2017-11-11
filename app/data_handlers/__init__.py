from .rate_data_handler import RateDataHandler


def get_sources() -> dict:
    """
    Get all the available data sources
    :return: all available data handlers
    """
    return {'rate': RateDataHandler}
