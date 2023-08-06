import os
from jadi import component

from aj.plugins.dashboard.api import Widget

@component(Widget)
class CPUTemp(Widget):
    id = 'cpu_temp'

    # display name
    name = _('CPU Temp')

    # template of the widget
    template = '/cpu_temp:resources/partials/dash.html'

    # template of the configuration dialog
    config_template = '/cpu_temp:resources/partials/config/dash.config.html'

    def __init__(self, context):
        Widget.__init__(self, context)

    def get_value(self, config):
        if 'temp' not in config:
            config['temp'] = {}
            config['tempchart'] = {}
            config['temp']['unit'] = 'C'
            config['temp']['file'] = 'thermal_zone0/temp'
            config['tempchart']['tempmax'] = 105
            config['tempchart']['tempmin'] = 35
            
        try:
            with open('/sys/class/thermal/'+config['temp']['file'], 'r') as f:
                str = f.read()
        except IOError:
            str = 0

        return {
            'temp':{
                'value': str,
                'unit': config['temp']['unit']
            },
            'chart':{
                'max': config['tempchart']['tempmax'],
                'min': config['tempchart']['tempmin']
            },
        };