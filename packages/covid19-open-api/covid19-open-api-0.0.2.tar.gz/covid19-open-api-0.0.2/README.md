# Covid19-Open-API



### Example usage

```python
from covid19openapi import ThaiCovid19

if __name__ == '__main__':
    thai = ThaiCovid19()
    today = thai.get('today')
    timeline = thai.get('timeline')
    all_field = thai.get_all()

    print(today)
    print(all_field)
```

**You can pass your source to the constructor 
also you will need to somehow register api in config.py** <br><br>
 **Default source is "covid19.th-stat.com"** <br><br> 
 Get api based on your source field. e.g.
 - today
 - timeline
 - cases
 - cases_sum
 - area

> requests.get is used so you can pass kwargs as documented at https://requests.readthedocs.io/en/master/user/quickstart/

## REFERENCES: https://covid19.th-stat.com/
