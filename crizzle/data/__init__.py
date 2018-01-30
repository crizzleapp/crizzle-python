from .rate_data_handler import RateDataHandler


def get_sources() -> dict:
    """
    Get all the available data sources

    Returns:
        all available data sources
    """
    return {'rate': RateDataHandler}
