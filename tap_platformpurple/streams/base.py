import datetime
import pytz
import singer

from dateutil.parser import parse
from tap_framework.streams import BaseStream
from tap_framework.config import get_config_start_date
from tap_framework.state import get_last_record_value_for_table, incorporate, \
    save_state

LOGGER = singer.get_logger()


class BasePlatformPurpleStream(BaseStream):

    def get_stream_data(self, data):
        return [self.process(item) for item in data]

    def select_keys(self, data):
        catalog_entry = self.catalog
        to_return = {}

        for k, v in data.items():
            schema = catalog_entry.schema.properties.get(k)

            if schema.inclusion == 'automatic' or schema.selected:
                to_return[k] = v

        return to_return

    def convert_types(self, data):
        catalog_entry = self.catalog
        to_return = {}

        for k, v in data.items():
            schema = catalog_entry.schema.properties.get(k)
            datatype = schema.type
            is_datetime = schema.format == 'date-time'

            if not v:
                to_return[k] = None
            elif is_datetime:
                to_return[k] = parse(v).strftime('%Y-%m-%dT%H:%M:%SZ')
            elif "integer" in datatype:
                to_return[k] = int(v)
            elif "number" in datatype:
                to_return[k] = float(v)
            else:
                to_return[k] = v

        return to_return

    def process(self, data):
        return \
            self.convert_types(
                self.select_keys(
                    self.filter_keys(
                        data)))

    def sync_data(self):
        table = self.TABLE
        done = False

        start_date = get_last_record_value_for_table(self.state, table)

        if start_date is None:
            start_date = get_config_start_date(self.config)

        end_date = start_date + datetime.timedelta(days=7)
        max_date = start_date

        while not done:
            LOGGER.info(
                "Querying {} starting at {}".format(table, start_date))

            response = self.client.make_request(
                self.get_url(),
                'POST',
                body={
                    'filters': {
                        'environment': self.config.get('environment')
                    },
                    'startMSeconds': int(start_date.timestamp() * 1000),
                    'endMSeconds': int(end_date.timestamp() * 1000)
                })

            to_write = self.get_stream_data(response)

            with singer.metrics.record_counter(endpoint=table) as ctr:
                singer.write_records(table, to_write)

                ctr.increment(amount=len(to_write))

                for item in to_write:
                    max_date = max(
                        max_date,
                        parse(item.get('dateTime'))
                    )

            self.state = incorporate(
                self.state, table, 'start_date', start_date)

            if start_date == max_date:
                done = True

            start_date = max_date
            end_date = start_date + datetime.timedelta(days=7)

            save_state(self.state)
