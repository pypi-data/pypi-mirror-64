
import os
import pytest
from datetime import datetime
from vds_api_client.api_v2 import VdsApiV2
from vds_api_client.vds_api_base import getpar_fromtext
import pandas as pd


def test_gridded_config(credentials, example_config_v2):
    vds = VdsApiV2(credentials['user'], credentials['pw'])
    vds.gen_gridded_data_request(gen_uri=False,
                                 config_file=example_config_v2,
                                 products=['SM-LN_V001_100'],
                                 start_date='2018-01-01',
                                 end_date=datetime(2018, 1, 3),
                                 nrequests=2)
    assert vds._config == {'api_call': 'gridded-data',
                           'lat_min': '51.9001', 'lat_max': '52.1001',
                           'lon_min': '4.9001', 'lon_max': '5.1001',
                           'file_format': 'gtiff',
                           'start_date': '2018-01-01',
                           'end_date': '2018-01-03',
                           'products': ['SM-LN_V001_100'],
                           'nrequests': 2,
                           'zipped': False}
    with pytest.raises(RuntimeError):
        vds.gen_gridded_data_request(products=['Nonexisting'])


def test_ts_config(credentials, example_config_v2):
    vds = VdsApiV2(credentials['user'], credentials['pw'])
    vds.gen_time_series_requests(gen_uri=False,
                                 config_file=example_config_v2,
                                 products=['SM-LN_V001_100'],
                                 start_time=datetime(2018, 1, 1),
                                 end_time='2019-01-01',
                                 lats=[51.3], lons=[5.1], rois=[3249], masked=True)
    assert vds._config == {'api_call': 'time-series',
                           'products': ['SM-LN_V001_100'],
                           'lats': [51.3], 'lons': [5.1],
                           'rois': [3249],
                           'start_time': '2018-01-01',
                           'end_time': '2019-01-01',
                           'file_format': 'csv',
                           'av_win': 0,
                           'masked': True,
                           'clim': False,
                           't': None}
    with pytest.raises(RuntimeError):
        vds.gen_time_series_requests(products=['Nonexisting'])


def test_gen_uri_grid(credentials, example_config_v2):
    vds = VdsApiV2(credentials['user'], credentials['pw'])
    vds.gen_gridded_data_request(gen_uri=True, config_file=example_config_v2, products=['SM-LN_V001_100'],
                                 start_date='2018-01-01', end_date=datetime(2019,1,1),
                                 nrequests=2)
    assert vds.async_requests == ['https://maps.vandersat.com/api/v2/products/SM-LN_V001_100/gridded-data?'
                                  'lat_min=51.9001&lat_max=52.1001&lon_min=4.9001&lon_max=5.1001&'
                                  'start_date=2018-01-01&end_date=2018-07-01&format=gtiff&zipped=false',
                                  'https://maps.vandersat.com/api/v2/products/SM-LN_V001_100/gridded-data?'
                                  'lat_min=51.9001&lat_max=52.1001&lon_min=4.9001&lon_max=5.1001&'
                                  'start_date=2018-07-02&end_date=2019-01-01&format=gtiff&zipped=false'
                                  ]
    assert len(vds.async_requests) == 2
    vds.gen_uri(products=['SM-C1N_V001_100'])
    assert len(vds.async_requests) == 4
    vds.gen_uri(add=False, file_format='netcdf4')
    assert len(vds.async_requests) == 2
    assert all(['&format=netcdf4' in req for req in vds.async_requests])


def test_gen_uri_ts(credentials, example_config_v2):
    vds = VdsApiV2(credentials['user'], credentials['pw'])
    vds.gen_time_series_requests(gen_uri=True, config_file=example_config_v2, products=['SM-LN_V001_100'])
    assert vds.async_requests == ['https://maps.vandersat.com/api/v2/products/SM-LN_V001_100/point-time-series?'
                                  'start_time=2018-01-01&end_time=2018-01-31&lat=52.345&lon=4.567&'
                                  'format=csv&avg_window_days=0&include_masked_data=false&climatology=false',
                                  'https://maps.vandersat.com/api/v2/products/SM-LN_V001_100/roi-time-series?'
                                  'start_time=2018-01-01&end_time=2018-01-31&roi_id=7046&format=csv&'
                                  'avg_window_days=0&include_masked_data=false&climatology=false',
                                  'https://maps.vandersat.com/api/v2/products/SM-LN_V001_100/roi-time-series?'
                                  'start_time=2018-01-01&end_time=2018-01-31&roi_id=3249&format=csv&'
                                  'avg_window_days=0&include_masked_data=false&climatology=false'
                                  ]
    assert len(vds.async_requests) == 3
    vds.gen_uri(products=['SM-C1N_V001_100'])
    assert len(vds.async_requests) == 6
    vds.gen_uri(add=False, file_format='json')
    assert len(vds.async_requests) == 3


def test_getarea(credentials, example_config_v2, empty_save_dir):
    vds = VdsApiV2(credentials['user'], credentials['pw'])
    vds.outfold = empty_save_dir
    vds.gen_gridded_data_request(config_file=example_config_v2, products=['SM-LN_V001_100'])
    vds.submit_async_requests(queue_files=False)
    uuid = list(vds.uuids)[0]
    assert os.path.exists(uuid + '.uuid')
    fns_should = [os.path.join(empty_save_dir, fn).format(uuid[:5]) for fn in
                  ['SM-LN_V001_100_2018-02-03T000000_4.900100_52.100100_5.100100_51.900100_{}.tif',
                   'SM-LN_V001_100_2018-02-02T000000_4.900100_52.100100_5.100100_51.900100_{}.tif',
                   'SM-LN_V001_100_2018-02-01T000000_4.900100_52.100100_5.100100_51.900100_{}.tif']]

    assert not any([os.path.exists(fn) for fn in fns_should])
    vds.download_async_files()
    assert all([os.path.exists(fn) for fn in fns_should])
    assert not os.path.exists(uuid + '.uuid')


def test_getts(credentials, example_config_v2, save_dir):
    vds = VdsApiV2(credentials['user'], credentials['pw'])
    vds.outfold = save_dir
    vds.gen_time_series_requests(gen_uri=True, config_file=example_config_v2, rois=[])
    vds.submit_async_requests(queue_files=False)
    uuids = list(vds.uuids)
    fns_should = [os.path.join(save_dir, fn).format(uuid[:5]) for fn, uuid in zip(
                  ['ts_SM-LN_V001_100_2018-01-01T000000_2018-01-31T000000_4.567000_52.345000_{}.csv',
                   'ts_SM-C1N_V001_100_2018-01-01T000000_2018-01-31T000000_4.567000_52.345000_{}.csv'
                   ], vds.uuids)]
    assert all([os.path.exists(uuid + '.uuid') for uuid in uuids])
    assert not any([os.path.exists(fn) for fn in fns_should])
    vds.download_async_files()
    assert all([os.path.exists(fn) for fn in fns_should])
    assert not all([os.path.exists(uuid + '.uuid') for uuid in uuids])


def test_get_df(example_config_v2):
    vds = VdsApiV2()
    rois = getpar_fromtext(example_config_v2, 'rois')
    product = getpar_fromtext(example_config_v2, 'products')[1]
    df = vds.get_roi_df(product, rois[0], '2019-05-01', '2019-05-15')
    assert isinstance(df, pd.DataFrame)

# EOF
