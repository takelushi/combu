"""Create badges."""

from pybadges import badge

data_list = [{
    'name': 'python',
    'value': ' | '.join(['3.6', '3.7', '3.8', '3.9']),
    'color': 'blue',
    'path': './doc/badge/python.svg',
}, {
    'name': 'coverage',
    'value': '100%',
    'color': 'brightgreen',
    'path': './doc/badge/coverage.svg',
}, {
    'name': 'license',
    'value': 'MIT',
    'color': 'blue',
    'path': './doc/badge/license.svg',
}]

for data in data_list:
    b = badge(left_text=data['name'],
              right_text=data['value'],
              right_color=data['color'])
    with open(data['path'], 'w', encoding='UTF-8') as f:
        f.write(b)
