
from json import dumps

from . import name_constant, add_enum_constant, set_constant, add_statistics
from ..stats.calculate.power import Power, ExtendedPowerCalculator

POWER_ESTIMATE_CNAME = 'PowerEstimate'


def add_power_estimate(s, c, activity_group,
                       bike='${Constant:Power.${SegmentReader:kit}:None}',
                       rider_weight='${DiaryTopic:Weight:DiaryTopic \"Status\" (d)}',
                       vary='wind_speed, wind_heading, slope'):
    '''
    Add the constants necessary to estimate power output.
    '''
    activity_group_constraint = str(activity_group)
    power_name = name_constant(POWER_ESTIMATE_CNAME, activity_group)
    power = add_enum_constant(s, power_name, Power, single=False, constraint=activity_group_constraint,
                              description='Data needed to estimate power - see Power reftuple')
    set_constant(s, power, dumps({'bike': bike, 'rider_weight': rider_weight, 'vary': vary}))
    add_statistics(s, ExtendedPowerCalculator, c, owner_in='[unused - data via activity_statistics]',
                   power=name_constant(POWER_ESTIMATE_CNAME, activity_group))
