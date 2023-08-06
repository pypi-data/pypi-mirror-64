#!/usr/bin/env python3

import os
import traceback

from gv_services.proto.common_pb2 import Ack
from gv_services.settings import SHAPEFILE_NAME
from gv_utils import datetime, enums, protobuf

DATAPOINTEID = enums.AttId.datapointeid
DATATYPEEID = enums.AttId.datatypeeid
EID = enums.AttId.eid
GEOM = enums.AttId.geom
ROADEID = enums.AttId.roadeid
VALIDFROM = enums.AttId.validfrom


class Geographer:

    def __init__(self, logger, basecartopath, dbstorage):
        super().__init__()
        self.logger = logger
        self.basecartopath = basecartopath
        self.dbstorage = dbstorage

    async def add_mapping_roads_data_points(self, pbdata):
        success = False
        try:
            mapping, validat = await protobuf.decode_mapping(pbdata)
            datapoints, mapping = await Geographer._get_data_point_from_mapping(mapping, validat)
            if datapoints:
                await self.dbstorage.insert_data_points(datapoints)
            await self.dbstorage.insert_roads_data_points(mapping)
            success = True
        except:
            self.logger.error('An error occurred while adding new road - data point mappings.')
            self.logger.error(traceback.format_exc())
        return success

    @staticmethod
    async def _get_data_point_from_mapping(mapping, validat):
        datapoints = {}
        roadsdatapoints = []
        validfrom = datetime.from_timestamp(validat, True)
        for roadeid, locations in mapping.items():
            if not isinstance(locations, dict):
                for loceid in locations:
                    roadsdatapoints.append({DATAPOINTEID: loceid, ROADEID: roadeid, VALIDFROM: validfrom})
            else:
                for loceid, location in locations.items():
                    datapoints[loceid] = {EID: loceid, GEOM: location[GEOM], DATATYPEEID: location[DATATYPEEID]}
                    roadsdatapoints.append({DATAPOINTEID: loceid, ROADEID: roadeid, VALIDFROM: validfrom})
        return list(datapoints.values()), roadsdatapoints

    async def add_data_points(self, pbdata):
        success = False
        try:
            datapoints = await protobuf.decode_locations(pbdata)
            if datapoints:
                await self.dbstorage.insert_data_points(list(datapoints.values()))
            success = True
        except:
            self.logger.error('An error occurred while adding new data points.')
            self.logger.error(traceback.format_exc())
        return success

    async def import_shapefile_to_db(self):
        success = True
        try:
            await self.dbstorage.import_shapefile(os.path.join(self.basecartopath, SHAPEFILE_NAME))
        except:
            success = False
        return Ack(success=success)

    async def get_data_points(self, message):
        eids, datatype = message.eids.eids, message.datatype
        return await protobuf.encode_locations(await self.dbstorage.get_data_points(eids, datatype))

    async def get_roads(self, message):
        eids = message.eids.eids
        return await protobuf.encode_locations(await self.dbstorage.get_roads(eids))

    async def get_mapping_roads_data_points(self, message):
        roadeids, dpeids, validat = message.fromeids.eids, message.toeids.eids, message.validat.ToSeconds()
        return await protobuf.encode_mapping(await self.dbstorage.get_mapping_roads_data_points(
            roadeids, dpeids, datetime.from_timestamp(validat, True)), validat)

    async def update_roads_freeflow_speed(self, message):
        success = True
        try:
            ffspeeds = await protobuf.decode_ffspeeds(message)
            if ffspeeds:
                await self.dbstorage.update_roads_ffspeeds(ffspeeds)
        except:
            success = False
        return Ack(success=success)
