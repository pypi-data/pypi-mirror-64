from enum import Enum

from .covid19scope import Covid19


class Config(Enum):
    """Configurations Enum"""

    SOURCE = {
        Covid19.THAI: {
            'covid19.th-stat.com': {
                'today': 'https://covid19.th-stat.com/api/open/today',
                'timeline': 'https://covid19.th-stat.com/api/open/timeline',
                'cases': 'https://covid19.th-stat.com/api/open/cases',
                'cases_sum': 'https://covid19.th-stat.com/api/open/cases/sum',
                'area': 'https://covid19.th-stat.com/api/open/area'
            }
        }
    }
