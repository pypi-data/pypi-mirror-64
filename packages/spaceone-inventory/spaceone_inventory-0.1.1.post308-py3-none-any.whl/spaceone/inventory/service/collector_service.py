# -*- coding: utf-8 -*-

import logging
from google.protobuf.json_format import MessageToDict

from spaceone.core.service import *
from spaceone.inventory.error import *
from spaceone.inventory.manager.collector_manager import CollectorManager
from spaceone.inventory.manager.region_manager import RegionManager
from spaceone.inventory.manager.zone_manager import ZoneManager
from spaceone.inventory.manager.pool_manager import PoolManager
from spaceone.inventory.info.collector_info import PluginInfo

_LOGGER = logging.getLogger(__name__)

@authentication_handler
@authorization_handler
@event_handler
class CollectorService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['name', 'plugin_info', 'domain_id'])
    def create(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        return collector_mgr.create_collector(params)

    @transaction
    @check_required(['collector_id', 'domain_id'])
    def update(self, params):
        """
        Args:
            - name
            - priority
            - tags
            - plugin_info(dict)
        """
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        collector_id = params['collector_id']
        domain_id = params['domain_id']
        try:
            collector_vo = collector_mgr.get_collector(collector_id, domain_id)
        except Exception as e:
            raise ERROR_NO_COLLECTOR(collector_id=collector_id, domain_id=domain_id)

        # If plugin_info exists, we need deep merge with previous information
        merged_params = self._get_merged_params(params, collector_vo.plugin_info)
        _LOGGER.debug(f'[update] params: {params}')
        _LOGGER.debug(f'[update] merged_params: {merged_params}')

        return collector_mgr.update_collector_by_vo(collector_vo, params)


    @transaction
    @check_required(['collector_id', 'domain_id'])
    def delete(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        collector_id = params['collector_id']
        domain_id = params['domain_id']
        #collector_mgr.delete_schedulers_by_collector_id(collector_id, domain_id)

        return collector_mgr.delete_collector(collector_id, domain_id)

    @transaction
    @check_required(['collector_id', 'domain_id'])
    def get(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        collector_id = params['collector_id']
        domain_id = params['domain_id']
        return collector_mgr.get_collector(collector_id, domain_id)

    @transaction
    @check_required(['collector_id', 'domain_id'])
    def enable(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        collector_id = params['collector_id']
        domain_id = params['domain_id']
        return collector_mgr.enable_collector(collector_id, domain_id)

    @transaction
    @check_required(['collector_id', 'domain_id'])
    def disable(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        collector_id = params['collector_id']
        domain_id = params['domain_id']
        return collector_mgr.disable_collector(collector_id, domain_id)

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['collector_id','name','state','priority', 'plugin_id', 'domain_id'])
    def list(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        domain_id = params['domain_id']
        query = params.get('query', {})
        return collector_mgr.list_collectors(query)

    @transaction
    @check_required(['collector_id', 'domain_id'])
    def collect(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        job_info = collector_mgr.collect(params)
        return job_info

    @transaction
    @check_required(['collector_id', 'domain_id'])
    def verify_plugin(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        # TODO: change secret_id
        collector_id = params['collector_id']
        secret_id = params.get('credential_id', None)
        domain_id = params['domain_id']
        updated_option = collector_mgr.verify_plugin(collector_id, secret_id, domain_id)
        # If you here, succeed verify
        return {'status': True}

    @transaction
    @check_required(['collector_id', 'schedule', 'domain_id'])
    def add_schedule(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        collector_id = params['collector_id']
        domain_id = params['domain_id']

        collector_vo = collector_mgr.get_collector(collector_id, domain_id)
        params['collector'] = collector_vo

        scheduler_info = collector_mgr.add_schedule(params)
        return scheduler_info

    @transaction
    @check_required(['scheduler_id', 'domain_id'])
    def update_schedule(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        scheduler_id = params['scheduler_id']
        domain_id = params['domain_id']
        collector_vo = collector_mgr.update_scheduler(params)
        return collector_vo


    @transaction
    @check_required(['scheduler_id', 'domain_id'])
    def delete_schedule(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        scheduler_id = params['scheduler_id']
        domain_id = params['domain_id']
        return collector_mgr.delete_scheduler(scheduler_id, domain_id)

    @transaction
    @check_required(['collector_id', 'domain_id'])
    @append_query_filter(['collector_id', 'scheduler_id', 'domain_id'])
    def list_schedules(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        domain_id = params['domain_id']
        query = params.get('query', {})
        return collector_mgr.list_schedulers(query)



    ############################
    # for scheduler
    ############################
    @check_required(['schedule'])
    def scheduled_collectors(self, params):
        """ Search all collectors in this schedule

        This is global search out-of domain
        Args:
            schedule(dict): {
                    'hours': list,
                    'minutes': list
                }

            domain_id: optional

        ex) {'hour': 3}

        Returns: collectors_info 
        """
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')

        # state: ENABLED
        #filter_query = [{'k':'collector.state','v':'ENABLED','o':'eq'}]
        filter_query = []

        if 'domain_id' in params:
            domain_id = params['domain_id']
            # update query
            filter_query.append(_make_query_domain(domain_id))

        # parse schedule
        schedule = params['schedule']
        if 'hour' in schedule:
            # find plugins which has hour rule
            filter_query.append(_make_query_hour(schedule['hour']))

        elif 'minute' in schedule:
            # find pluings which has minute rule
            filter_query.append(_make_query_minute(schedule['minute']))

        else:
            # TODO:
            pass

        # make query for list_collector
        query = {'filter':filter_query}

        _LOGGER.debug(f'[scheduled_collectors] query: {query}')
        return collector_mgr.list_schedulers(query)

    @check_required(['credential_group_id', 'domain_id'])
    def get_credentials_by_grp_id(self, params):
        collector_mgr: CollectorManager = self.locator.get_manager('CollectorManager')
        creds_info = collector_mgr._get_credentials_by_cred_grp_id(params['credential_group_id'], params['domain_id'])
        result = []
        for cred in creds_info.results:
            result.append(cred.credential_id)
        return result

    ###############
    # Internal
    ###############
    def _get_region(self, region_id, domain_id):
        region_mgr:RegionManager = self.locator.get_manager('RegionManager')
        return region_mgr.get_region(region_id, domain_id)

    def _get_zone(self, zone_id, domain_id):
        zone_mgr:ZoneManager = self.locator.get_manager('ZoneManager')
        return zone_mgr.get_zone(zone_id, domain_id)

    def _get_pool(self, pool_id, domain_id):
        pool_mgr:PoolManager = self.locator.get_manager('PoolManager')
        #return pool_mgr.get_pool(pool_id, domain_id)
        return pool_mgr.get_pool(pool_id)

    def _get_merged_params(self, params, plugin_info_vo):
        """ if there is plugin_info at params,
        We need to merge plugin_info with plugin_info_vo
        """
        plugin_info = PluginInfo(plugin_info_vo)
        dict_plugin_info = MessageToDict(plugin_info, preserving_proto_field_name=True)
        
        new_plugin_info = params.get('plugin_info', {})
        new_plugin_info.update(dict_plugin_info)

        new_params = params.copy()
        new_params['plugin_info'] = new_plugin_info
        return new_params


def _make_query_domain(domain_id):
    return {
        'k': 'domain_id',
        'v': domain_id,
        'o': 'eq'
        }

def _make_query_hour(hour: int):
    # make query hour
    return {
        'k': 'schedule.hours',
        'v': hour,
        'o': 'contain'
        }

def _make_query_minute(minute: int):
    # make minute query
    return {
        'k': 'schedule.minute',
        'v': minute,
        'o': 'contain'
        }


