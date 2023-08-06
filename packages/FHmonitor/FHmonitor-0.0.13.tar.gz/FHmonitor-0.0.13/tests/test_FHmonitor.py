from FHmonitor.monitor import Monitor
import pytest
from FHmonitor.store import MongoDB
from FHmonitor.atm90_e32_pi import ATM90e32
from FHmonitor.calibrate import Calibrate
import logging
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope='module')
def meter():
    meter = Monitor()

    return meter


@pytest.fixture(scope='module')
def store():
    store = MongoDB("mongodb://localhost:27017/", "FitHome_test", "aggregate")
    return store


def test_init_meter(meter):
    meter_working = meter.init_sensor()
    assert meter_working is True


def test_take_reading(meter):
    Pa, Pr = meter.take_reading()
    assert Pa > 0
    assert Pr > 0


def test_store_reading(meter, store):
    Pa, Pr = meter.take_reading()
    reading = {"Pa": Pa, "Pr": Pr, }
    result = store.save(reading)
    assert result is True


def test_calibrate_voltage():
    c = Calibrate()
    assert c.lineFreq > 0
