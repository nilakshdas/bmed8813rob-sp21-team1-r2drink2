from .hydration import setup_hydration_staging
from .table import setup_table


def setup_staging(*args, **kwargs):
    setup_table(*args, **kwargs)
    setup_hydration_staging(*args, **kwargs)
