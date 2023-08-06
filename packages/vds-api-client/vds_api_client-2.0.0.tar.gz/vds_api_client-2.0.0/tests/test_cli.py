
from vds_api_client.api_cli import api


def test_base_cli(runner):
    result = runner.invoke(api)
    assert result.exit_code == 0


def test_cli_test(runner):
    result = runner.invoke(api, ['test'])
    assert result.exit_code == 0


def test_cli_info(runner):
    result = runner.invoke(api, ['info'])
    assert result.exit_code == 0


def test_cli_v2_grid_base(runner, empty_save_dir):
    result = runner.invoke(api, ['grid',
                                 '--product', 'SM-LN_V001_100',
                                 '--lon_range', '4.9', '5.1',
                                 '--lat_range', '51.9', '52.1',
                                 '--date_range', '2018-01-01', '2018-01-02',
                                 '--n_proc', '1',
                                 '-o', empty_save_dir])
    assert result.exit_code == 0
    assert not result.exception


def test_cli_v2_grid_nczip(runner, empty_save_dir):
    result = runner.invoke(api, ['grid',
                                 '--product', 'SM-LN_V001_100',
                                 '--lon_range', '4.9', '5.1',
                                 '--lat_range', '51.9', '52.1',
                                 '--date_range', '2018-01-01', '2018-01-02',
                                 '--n_proc', '1',
                                 '--format', 'netcdf4',
                                 '--zipped',
                                 '-o', empty_save_dir])
    assert result.exit_code == 0
    assert not result.exception


def test_cli_v2_ts_base(runner, empty_save_dir):
    result = runner.invoke(api, ['ts',
                                 '--product', 'SM-LN_V001_100',
                                 '--latlon', '51.9', '5.12',
                                 '--latlon', '52.0', '5.12',
                                 '--date_range', '2018-01-01', '2018-01-02',
                                 '-o', empty_save_dir])
    assert result.exit_code == 0
    assert not result.exception


def test_cli_v2_ts_allopts(runner, empty_save_dir):
    result = runner.invoke(api, ['ts',
                                 '--product', 'SM-LN_V001_100',
                                 '--latlon', '51.9', '5.12',
                                 '--latlon', '52.0', '5.12',
                                 '--date_range', '2018-01-01', '2018-01-10',
                                 '--masked',
                                 '--av_win', '3',
                                 '--clim',
                                 '-t', '10',
                                 '-o', empty_save_dir])
    assert result.exit_code == 0
    assert not result.exception

# EOF
