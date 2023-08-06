# -*- coding: UTF-8 -*-

import os
import pytest

try:
    from unittest.mock import MagicMock, call
except ImportError:
    from mock import MagicMock, call

from implib2.imp_modules import Module, ModuleError


class TestModule:

    def setup(self):
        self.serno = 31002
        self.bus = MagicMock()
        self.mod = Module(self.bus, self.serno)

        self.protocols = {
            'IMPBUS': 0,
            'SDI12': 1}

        self.event_modes = {
            "NormalMeasure": 0x00,
            "TRDScan": 0x01,
            "AnalogOut": 0x02,
            "ACIC_TC": 0x03,
            "SelfTest": 0x04,
            "MatTempSensor": 0x05}

        self.measure_modes = {
            "ModeA": 0x00,
            "ModeB": 0x01,
            "ModeC": 0x02}

        self.average_modes = {
            "CA": 0x00,
            "CK": 0x01,
            "CS": 0x02,
            "CF": 0x03}

    def test___init___protocols(self):
        assert self.mod.protocols == self.protocols

    def test___init___event_modes(self):
        assert self.mod.event_modes == self.event_modes

    def test___init___measure_modes(self):
        assert self.mod.measure_modes == self.measure_modes

    def test___init___average_modes(self):
        assert self.mod.average_modes == self.average_modes

    def test_unlock(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'SupportPW'
        value = 66 + 0x8000
        self.bus.set.return_value = True

        assert self.mod.unlock()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    @pytest.mark.parametrize("mode", [
        "NormalMeasure",
        "TRDScan",
        "AnalogOut",
        "ACIC_TC",
        "SelfTest",
        "MatTempSensor"])
    def test_get_event_mode(self, mode):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'Event'

        self.bus.get.return_value = (self.mod.event_modes[mode] + 0x80,)

        assert self.mod.get_event_mode() == mode
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_event_mode_UNKNOWN(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'Event'
        value = 0x06

        self.bus.get.return_value = (value,)

        with pytest.raises(ModuleError, message="Unknown event mode: {}".format(value)):
            self.mod.get_event_mode()
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_set_event_mode_InvalidMode(self):
        mode = 'UNKNOWN'

        self.mod.unlock = MagicMock()

        with pytest.raises(ModuleError, message="{}: Invalid event mode!".format(mode)):
            self.mod.set_event_mode(mode)
        self.mod.unlock.assert_not_called()

    def test_set_event_mode_SetEventModeFailed(self):
        mode = 'NormalMeasure'

        self.mod.unlock = MagicMock()
        self.bus.set.return_value = False

        with pytest.raises(ModuleError, message="Failed to set event mode!"):
            self.mod.set_event_mode(mode)
        self.mod.unlock.assert_called_once_with()

    @pytest.mark.parametrize("mode", [
        "NormalMeasure",
        "TRDScan",
        "AnalogOut",
        "ACIC_TC",
        "SelfTest",
        "MatTempSensor"])
    def test_set_event_mode_Failed(self, mode):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'Event'
        value = self.event_modes[mode]

        self.mod.unlock = MagicMock()
        self.bus.get.return_value = [value]
        expected = [call(self.serno, table, param),
                    call(self.serno, table, param),
                    call(self.serno, table, param),
                    call(self.serno, table, param),
                    call(self.serno, table, param)]

        with pytest.raises(ModuleError, message="Failed to set event mode!"):
            self.mod.set_event_mode(mode)
        self.mod.unlock.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])
        assert self.bus.get.call_args_list == expected

    @pytest.mark.parametrize("mode", [
        "NormalMeasure",
        "TRDScan",
        "AnalogOut",
        "ACIC_TC",
        "SelfTest",
        "MatTempSensor"])
    def test_set_event_mode_FourAttempts(self, mode):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'Event'
        value = self.event_modes[mode]

        self.mod.unlock = MagicMock()
        self.bus.get.side_effect = [[value], [value], [value],
                                    [value], [value + 0x80]]
        expected = [call(self.serno, table, param),
                    call(self.serno, table, param),
                    call(self.serno, table, param),
                    call(self.serno, table, param),
                    call(self.serno, table, param)]

        assert self.mod.set_event_mode(mode)
        self.mod.unlock.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])
        assert self.bus.get.call_args_list == expected

    @pytest.mark.parametrize("mode", [
        "NormalMeasure",
        "TRDScan",
        "AnalogOut",
        "ACIC_TC",
        "SelfTest",
        "MatTempSensor"])
    def test_set_event_mode(self, mode):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'Event'
        value = self.event_modes[mode]

        self.mod.unlock = MagicMock()
        self.bus.get.return_value = [value + 0x80]

        assert self.mod.set_event_mode(mode)
        self.mod.unlock.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])
        self.bus.get.assert_called_once_with(self.serno, table, param)

    #
    # get_measure_mode() tests
    #

    @pytest.mark.parametrize("mode", [
        "ModeA",
        "ModeB",
        "ModeC"])
    def test_get_measure_mode(self, mode):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'MeasMode'

        self.bus.get.return_value = (self.mod.measure_modes[mode],)

        assert self.mod.get_measure_mode() == mode
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_measure_mode_UnknownMode(self):
        value = 0x03
        self.bus.get.return_value = (value,)

        with pytest.raises(ModuleError, message="Unknown measure mode: %s!".format(value)):
            self.mod.get_measure_mode()

    def test_set_measure_mode_InvalidMeasureMode(self):
        mode = "ModeD"
        with pytest.raises(ModuleError, message="{}: Invalid measure mode!".format(mode)):
            self.mod.set_measure_mode(mode)

    def test_set_measure_mode_WrongEventModeMode(self):
        mode = 'ModeA'

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotNormalMeasure"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'NormalMeasure'!"):
            self.mod.set_measure_mode(mode)
        self.mod.get_event_mode.assert_called_once_with()

    def test_set_measure_mode(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'MeasMode'
        mode = 'ModeA'
        value = self.measure_modes[mode]

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NormalMeasure"

        assert self.mod.set_measure_mode(mode)
        self.mod.get_event_mode.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    @pytest.mark.parametrize("mode", [
        "ModeA",
        "ModeB",
        "ModeC"])
    def test_get_default_measure_mode(self, mode):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'DefaultMeasMode'

        self.bus.get.return_value = (self.mod.measure_modes[mode],)

        assert self.mod.get_default_measure_mode() == mode
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_default_measure_mode_UnknownMode(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'DefaultMeasMode'
        value = 0x03

        self.bus.get.return_value = (value,)

        with pytest.raises(ModuleError, message="Unknown default measure mode: {}!".format(value)):
            self.mod.get_default_measure_mode()
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_set_default_measure_mode_InvalidDefaultMeasureMode(self):
        mode = "ModeD"
        with pytest.raises(ModuleError, message="{}: Invalid default measure mode!".format(mode)):
            self.mod.set_default_measure_mode(mode)

    def test_set_default_measure_mode_WrongEventModeMode(self):
        mode = 'ModeA'

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotNormalMeasure"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'NormalMeasure'!"):
            self.mod.set_default_measure_mode(mode)
        self.mod.get_event_mode.assert_called_once_with()

    def test_set_default_measure_mode(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'DefaultMeasMode'
        mode = 'ModeA'
        value = self.measure_modes[mode]

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NormalMeasure"

        assert self.mod.set_default_measure_mode(mode)
        self.mod.get_event_mode.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    @pytest.mark.parametrize("mode", ["CA", "CK", "CS", "CF"])
    def test_get_average_mode(self, mode):
        table = 'APPLICATION_PARAMETER_TABLE'
        param = 'AverageMode'

        self.bus.get.return_value = (self.mod.average_modes[mode],)

        assert self.mod.get_average_mode() == mode
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_average_mode_UnknownMode(self):
        table = 'APPLICATION_PARAMETER_TABLE'
        param = 'AverageMode'
        value = 0x04

        self.bus.get.return_value = (value,)

        with pytest.raises(ModuleError, message="Unknown average mode: {}!".format(value)):
            self.mod.get_average_mode()
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_set_average_mode_InvalidAverageMode(self):
        mode = "CX"
        with pytest.raises(ModuleError, message="{}: Invalid average mode!".format(mode)):
            self.mod.set_average_mode(mode)

    def test_set_average_mode(self):
        table = 'APPLICATION_PARAMETER_TABLE'
        param = 'AverageMode'
        mode = 'CA'
        value = self.average_modes[mode]

        assert self.mod.set_average_mode(mode)
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test_get_table(self):
        with pytest.raises(NotImplementedError):
            self.mod.get_table('TABLE')

    def test_set_table(self):
        with pytest.raises(NotImplementedError):
            self.mod.set_table('TABLE', None)

    def test_get_serno(self):
        table = 'SYSTEM_PARAMETER_TABLE'
        param = 'SerialNum'
        self.bus.get.return_value = (self.serno,)

        assert self.mod.get_serno() == self.serno
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_set_serno(self):
        table = 'SYSTEM_PARAMETER_TABLE'
        param = 'SerialNum'
        value = self.serno + 1

        self.bus.set.return_value = True
        self.mod.unlock = MagicMock()

        assert self.mod.set_serno(value)
        assert self.mod._serno == value
        self.mod.unlock.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test_read_eeprom(self):
        with pytest.raises(NotImplementedError):
            self.mod.read_eeprom()

    def test_write_eeprom(self):
        head = os.urandom(250)
        midl = os.urandom(250)
        tail = os.urandom(128)
        gen = (x for x in [head, midl, tail])

        eeprom = MagicMock()
        eeprom.__iter__.return_value = gen

        self.bus.set_eeprom_page.return_value = True
        self.mod.unlock = MagicMock()

        assert self.mod.write_eeprom(eeprom)
        self.mod.unlock.assert_called_once_with()
        expected = [call(self.serno, x, y) for x, y in
                    enumerate([head, midl, tail])]
        assert self.bus.set_eeprom_page.call_args_list == expected

    def test_write_eeprom_EEPROMWritingFailed(self):
        head = os.urandom(250)
        midl = os.urandom(250)
        tail = os.urandom(128)
        gen = (x for x in [head, midl, tail])

        eeprom = MagicMock()
        eeprom.__iter__.return_value = gen

        self.bus.set_eeprom_page.side_effect = [False]

        with pytest.raises(ModuleError, message="Writing EEPROM failed!"):
            self.mod.write_eeprom(eeprom)

    def test_get_hw_version(self):
        table = 'SYSTEM_PARAMETER_TABLE'
        param = 'HWVersion'
        self.bus.get.return_value = (1.12176287368173,)

        assert self.mod.get_hw_version() == '1.12'
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_fw_version(self):
        table = 'SYSTEM_PARAMETER_TABLE'
        param = 'FWVersion'
        self.bus.get.return_value = (1.11176287368173,)

        assert self.mod.get_fw_version() == '1.111763'
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_start_measure_WrongEventMode(self):
        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotNormalMeasure"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'NormalMeasure'!"):
            self.mod.start_measure()
        self.mod.get_event_mode.assert_called_once_with()

    def test_start_measure_WrongMeasureMode(self):
        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NormalMeasure"

        self.mod.get_measure_mode = MagicMock()
        self.mod.get_measure_mode.return_value = 'NotModeA'

        with pytest.raises(ModuleError, message="Wrong measure mode, need 'ModeA'!"):
            self.mod.start_measure()
        self.mod.get_event_mode.assert_called_once_with()
        self.mod.get_measure_mode.assert_called_once_with()

    def test_start_measure_AlreadyRunning(self):
        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NormalMeasure"

        self.mod.get_measure_mode = MagicMock()
        self.mod.get_measure_mode.return_value = 'ModeA'

        self.mod.measure_running = MagicMock()
        self.mod.measure_running.return_value = True

        with pytest.raises(ModuleError, message="Measurement cycle already in progress!"):
            self.mod.start_measure()
        self.mod.get_event_mode.assert_called_once_with()
        self.mod.get_measure_mode.assert_called_once_with()
        self.mod.measure_running.assert_called_once_with()

    def test_start_measure(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'StartMeasure'
        value = 1

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NormalMeasure"

        self.mod.get_measure_mode = MagicMock()
        self.mod.get_measure_mode.return_value = 'ModeA'

        self.mod.measure_running = MagicMock()
        self.mod.measure_running.return_value = False

        self.bus.set.return_value = True

        assert self.mod.start_measure()
        self.mod.get_event_mode.assert_called_once_with()
        self.mod.get_measure_mode.assert_called_once_with()
        self.mod.measure_running.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test_measure_running_YES(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'StartMeasure'

        self.bus.get.return_value = (1,)

        assert self.mod.measure_running()
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_measure_running_Nop(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'StartMeasure'

        self.bus.get.return_value = (0,)

        assert not self.mod.measure_running()
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_measurement(self):
        table = 'MEASURE_PARAMETER_TABLE'
        param = 'Moist'
        moist = 17.77

        self.bus.get.return_value = (moist,)

        assert self.mod.get_measurement(quantity=param) == moist
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test_get_moisture(self):
        moist = 12.35

        self.mod.start_measure = MagicMock()
        self.mod.start_measure.return_value = True

        self.mod.measure_running = MagicMock()
        self.mod.measure_running.side_effect = (True, True, False)

        self.mod.get_measurement = MagicMock()
        self.mod.get_measurement.return_value = moist

        expected = [call(), call(), call()]

        assert self.mod.get_moisture() == moist
        self.mod.start_measure.assert_called_once_with()
        assert self.mod.measure_running.call_args_list == expected
        self.mod.get_measurement.assert_called_once_with(quantity='Moist')

    def test__get_analog_output_mode(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'AnalogOutputMode'
        mode = 0

        self.bus.get.return_value = (mode,)

        assert self.mod._get_analog_output_mode() == mode
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__set_analog_output_mode_WrongMode(self):
        with pytest.raises(ModuleError, message="Wrong AnalogOutputMode!"):
            self.mod._set_analog_output_mode(3)

    def test__set_analog_output_mode(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'AnalogOutputMode'
        value = 0

        self.bus.set.return_value = True

        assert self.mod._set_analog_output_mode(value)
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test__get_moist_max_value(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'MoistMaxValue'
        self.bus.get.return_value = (50,)

        assert self.mod._get_moist_max_value() == 50
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__get_moist_min_value(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'MoistMinValue'
        self.bus.get.return_value = (0,)

        assert self.mod._get_moist_min_value() == 0
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__get_temp_max_value(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'TempMaxValue'
        self.bus.get.return_value = (60,)

        assert self.mod._get_temp_max_value() == 60
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__get_temp_min_value(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'TempMinValue'
        self.bus.get.return_value = (0,)

        assert self.mod._get_temp_min_value() == 0
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__set_analog_moist_ValueToLow(self):
        with pytest.raises(ModuleError, message="Value out of range!"):
            self.mod._set_analog_moist(-1)

    def test__set_analog_moist_ValueToHigh(self):
        with pytest.raises(ModuleError, message="Value out of range!"):
            self.mod._set_analog_moist(1001)

    def test__set_analog_moist_WrongEventMode(self):
        mvolt = 550

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotAnalogOut"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'AnalogOut'!"):
            self.mod._set_analog_moist(mvolt)
        self.mod.get_event_mode.assert_called_once_with()

    def test__set_analog_moist_WrongAnalogOutputMode(self):
        mvolt = 550

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "AnalogOut"

        self.mod._get_analog_output_mode = MagicMock()
        self.mod._get_analog_output_mode.return_value = -1

        with pytest.raises(ModuleError, message="Wrong AnalogOutputMode, need mode 0 here!"):
            self.mod._set_analog_moist(mvolt)
        self.mod.get_event_mode.assert_called_once_with()
        self.mod._get_analog_output_mode.assert_called_once_with()

    def test__set_analog_moist(self):
        table = 'MEASURE_PARAMETER_TABLE'
        param = 'Moist'
        mvolt = 500
        min_value = 0
        max_value = 10
        value = (max_value - min_value) / 1000.0 * mvolt + min_value

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "AnalogOut"

        self.mod._get_analog_output_mode = MagicMock()
        self.mod._get_analog_output_mode.return_value = 0

        self.mod._get_moist_min_value = MagicMock()
        self.mod._get_moist_min_value.return_value = 0

        self.mod._get_moist_max_value = MagicMock()
        self.mod._get_moist_max_value.return_value = 10

        assert self.mod._set_analog_moist(mvolt)
        self.mod.get_event_mode.assert_called_once_with()
        self.mod._get_analog_output_mode.assert_called_once_with()
        self.mod._get_moist_min_value.assert_called_once_with()
        self.mod._get_moist_max_value.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test__get_analog_moist(self):
        table = 'MEASURE_PARAMETER_TABLE'
        param = 'Moist'
        self.bus.get.return_value = (0,)

        assert self.mod._get_analog_moist() == 0
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__set_analog_temp_ValueToLow(self):
        with pytest.raises(ModuleError, message="Value out of range!"):
            self.mod._set_analog_temp(-1)

    def test__set_analog_temp_ValueToHigh(self):
        with pytest.raises(ModuleError, message="Value out of range!"):
            self.mod._set_analog_temp(1001)

    def test__set_analog_temp_WrongEventMode(self):
        mvolt = 550

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotAnalogOut"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'AnalogOut'!"):
            self.mod._set_analog_temp(mvolt)
        self.mod.get_event_mode.assert_called_once_with()

    def test__set_analog_temp_WrongAnalogOutputMode(self):
        mvolt = 550

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "AnalogOut"

        self.mod._get_analog_output_mode = MagicMock()
        self.mod._get_analog_output_mode.return_value = -1

        with pytest.raises(ModuleError, message="Wrong AnalogOutputMode, need mode 0 here"):
            self.mod._set_analog_temp(mvolt)
        self.mod.get_event_mode.assert_called_once_with()
        self.mod._get_analog_output_mode.assert_called_once_with()

    def test__set_analog_temp(self):
        table = 'MEASURE_PARAMETER_TABLE'
        param = 'CompTemp'
        min_value = -20
        max_value = 70
        mvolt = 550
        value = (max_value - min_value) / 1000.0 * mvolt + min_value

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "AnalogOut"

        self.mod._get_analog_output_mode = MagicMock()
        self.mod._get_analog_output_mode.return_value = 0

        self.mod._get_temp_min_value = MagicMock()
        self.mod._get_temp_min_value.return_value = min_value

        self.mod._get_temp_max_value = MagicMock()
        self.mod._get_temp_max_value.return_value = max_value

        assert self.mod._set_analog_temp(mvolt)
        self.mod.get_event_mode.assert_called_once_with()
        self.mod._get_analog_output_mode.assert_called_once_with()
        self.mod._get_temp_min_value.assert_called_once_with()
        self.mod._get_temp_max_value.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test__get_analog_temp(self):
        table = 'MEASURE_PARAMETER_TABLE'
        param = 'CompTemp'
        self.bus.get.return_value = (0,)

        assert self.mod._get_analog_temp() == 0
        self.bus.get.assert_called_once_with(self.serno, table, param)

    def test__turn_asic_on_WrongEventMode(self):
        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotSelfTest"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'SelfTest'!"):
            self.mod._turn_asic_on()

    def test__turn_asic_on(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'SelfTest'
        value = [1, 1, 63, 0]

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "SelfTest"

        assert self.mod._turn_asic_on()
        self.mod.get_event_mode.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, value)

    def test__turn_asic_off_WrongEventMode(self):
        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotSelfTest"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'SelfTest'!"):
            self.mod._turn_asic_off()

    def test__turn_asic_off(self):
        table = 'ACTION_PARAMETER_TABLE'
        param = 'SelfTest'
        value = [1, 0, 255, 0]

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "SelfTest"

        assert self.mod._turn_asic_off()
        self.mod.get_event_mode.assert_called_once_with()
        self.bus.set.assert_called_once_with(self.serno, table, param, value)

    def test__get_transit_time_tdr_WrongEventMode(self):
        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NotNormalMeasure"

        with pytest.raises(ModuleError, message="Wrong event mode, need 'NormalMeasure'!"):
            self.mod._get_transit_time_tdr()

    def test__get_transit_time_tdr(self):
        transit_time = 123
        tdr_value = 321

        set_calls = [
            call(self.serno,
                 'DEVICE_CONFIGURATION_PARAMETER_TABLE', 'MeasMode', [0]),
            call(self.serno,
                 'ACTION_PARAMETER_TABLE', 'StartMeasure', [1]),
            call(self.serno,
                 'DEVICE_CONFIGURATION_PARAMETER_TABLE', 'MeasMode', [2])
        ]

        get_calls = [
            call(self.serno, 'ACTION_PARAMETER_TABLE', 'StartMeasure'),
            call(self.serno, 'ACTION_PARAMETER_TABLE', 'StartMeasure'),
            call(self.serno, 'MEASURE_PARAMETER_TABLE', 'TransitTime'),
            call(self.serno, 'MEASURE_PARAMETER_TABLE', 'TDRValue'),
        ]

        self.mod.get_event_mode = MagicMock()
        self.mod.get_event_mode.return_value = "NormalMeasure"

        self.bus.set.return_value = True
        self.bus.get.side_effect = [(1,), (0,), (transit_time,), (tdr_value,)]

        assert self.mod._get_transit_time_tdr() == (transit_time, tdr_value)
        self.mod.get_event_mode.assert_called_once_with()
        assert self.bus.set.call_args_list == set_calls
        assert self.bus.get.call_args_list == get_calls

    def test__set_sdi12_address_WrongAddress(self):
        with pytest.raises(ModuleError, message='SDI12 address out of range!'):
            self.mod._set_sdi12_address(2000)

    def test__set_sdi12_address(self):
        table = 'SYSTEM_PARAMETER_TABLE'
        param = 'ModuleInfo1'
        value = 0

        self.mod._set_sdi12_address(value)
        self.bus.set.assert_called_once_with(self.serno, table, param, [value])

    def test__set_protocol_WrongProtocol(self):
        value = 'chocolate_jesus'
        with pytest.raises(ModuleError, message="Wrong protocol: {}".format(value)):
            self.mod._set_protocol(value)

    def test__set_protocol(self):
        table = 'DEVICE_CONFIGURATION_PARAMETER_TABLE'
        param = 'Protocol'
        protocols = {'IMPBUS': 0, 'SDI12': 1}

        assert protocols == self.mod.protocols

        expected = []
        for protocol in protocols:
            value = protocols[protocol]
            self.mod._set_protocol(protocol)
            expected.append(call(self.serno, table, param, [value]))

        assert self.bus.set.call_args_list == expected
