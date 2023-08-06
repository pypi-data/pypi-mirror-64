
import os
from vds_api_client.vds_api_base import VdsApiBase, getpar_fromtext
from vds_api_client.types import Products, Product, Rois, Roi
import pytest


def test_par_from_text(example_config_v1):
    lat_min = getpar_fromtext(example_config_v1, 'lat_min')
    assert lat_min == '51.9001'
    products = getpar_fromtext(example_config_v1, 'products')
    assert products == ['SM-LN_V001_100', 'SM-C1N_V001_100']
    void = getpar_fromtext(example_config_v1, 'nonexisting')
    assert void is None
    with pytest.raises(RuntimeError):
        getpar_fromtext('nonexisting.file', 'lat_min')


def test_login(credentials):
    vds = VdsApiBase(credentials['user'], credentials['pw'])
    assert vds.products is not None


def test_login_from_environment():
    vds = VdsApiBase()
    assert vds.products is not None


def test_load_info(credentials):
    vds = VdsApiBase(credentials['user'], credentials['pw'])
    assert type(vds.usr_dict) is dict
    assert type(vds.rois) is Rois


def test_host_setter(credentials):
    vds = VdsApiBase(credentials['user'], credentials['pw'])
    vds.host = 'test'
    assert vds.host == 'test.vandersat.com/api/v2/'
    with pytest.raises(ValueError):
        vds.host = 'nonexisting'


def test_outfold_setter(credentials, empty_save_dir):
    vds = VdsApiBase(credentials['user'], credentials['pw'])
    assert vds.outfold is ''
    assert os.path.exists(empty_save_dir)
    new_dir = os.path.join(empty_save_dir, 'fold1', 'fold2')
    assert not os.path.exists(new_dir)
    vds.outfold = new_dir
    assert os.path.exists(empty_save_dir)


def test_rois(credentials, example_config_v2):
    vds = VdsApiBase(credentials['user'], credentials['pw'])
    assert isinstance(vds.rois, Rois)
    assert all([isinstance(r, Roi) for r in vds.rois])
    roi_str, roi_name = getpar_fromtext(example_config_v2, 'rois')
    assert vds.rois[roi_str] == int(roi_str)
    assert vds.rois[int(roi_str)] == int(roi_str)
    assert vds.rois[roi_name] > 0


def test_products(credentials, example_config_v2):
    vds = VdsApiBase(credentials['user'], credentials['pw'])
    assert isinstance(vds.products, Products)
    assert all([isinstance(p, Product) for p in vds.products])
    products = getpar_fromtext(example_config_v2, 'products')
    prod = vds.products[products[0]]
    assert prod.api_name is not None
    vds.check_valid_products(products)


def test_cleanup_savedir(empty_save_dir):
    assert not os.listdir(empty_save_dir)

# EOF
