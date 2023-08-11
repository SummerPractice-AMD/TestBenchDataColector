import unittest
from unittest.mock import mock_open, patch
from generatejson import (get_errors, get_simtimefile, get_realtimefile, get_testname, get_testsstatus, get_testssimtime, get_testsrealtime, get_logline)


content = """     -.--ns INFO     cocotb.gpi                                  gpi_embed.c:111  in embed_init_python               Did not detect Python virtual environment. Using system-wide Python interpreter.
     -.--ns INFO     cocotb.gpi                                GpiCommon.cpp:91   in gpi_print_registered_impl       VPI registered
     0.00ns INFO     cocotb                                      __init__.py:128  in _initialise_testbench           Unable to determine Cocotb version from Unknown
     0.00ns INFO     cocotb                                      __init__.py:148  in _initialise_testbench           Seeding Python random module with 1691669788
     0.00ns INFO     cocotb.regression                         regression.py:187  in initialise                      Found test testbench.run_test_021
     0.00ns INFO     cocotb.regression                         regression.py:187  in initialise                      Found test testbench.run_test_022
15500020000000000.00ns INFO     cocotb.regression                         regression.py:321  in execute                         Running test 21/32: run_test_021
15500020000000000.00ns INFO     cocotb.test._my_test.0x2867a90            decorators.py:253  in _advance                        Starting test: "run_test_021"
                                                                                                                                Description: Automatically generated test
                                                                                                                                
                                                                                                                                	backpressure_inserter: intermittent_single_cycles (Generator to intermittently insert a single cycle pulse)
                                                                                                                                	config_coroutine: randomly_switch_config (Twiddle the byteswapping config register)
                                                                                                                                	data_in: random_packet_sizes (random string data of a random length)
                                                                                                                                	idle_inserter: None
                                                                                                                                
15500020000000000.00ns INFO     cocotb.scoreboard.endian_swapper          scoreboard.py:216  in add_interface                   Created with reorder_depth 0
15545020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 48 bytes
15590020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 53 bytes
15680020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 114 bytes
15735020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 72 bytes
15790020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 71 bytes
15885020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 137 bytes
15990020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 139 bytes
16100020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 144 bytes
16145020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 58 bytes
16245020000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 135 bytes
16275020000000000.00ns INFO     cocotb.endian_swapper                      testbench.py:111  in run_test                        DUT correctly counted 10 packets
16275020000000000.00ns INFO     cocotb.test._my_test.0x2867a90            decorators.py:264  in _advance                        
16275021000000000.00ns INFO     cocotb.regression                         regression.py:266  in handle_result                   Test Passed: run_test_021
16275021000000000.00ns INFO     cocotb.regression                         regression.py:321  in execute                         Running test 22/32: run_test_022
16275021000000000.00ns INFO     cocotb.test._my_test.0x2874710            decorators.py:253  in _advance                        Starting test: "run_test_022"
                                                                                                                                Description: Automatically generated test
                                                                                                                                
                                                                                                                                	backpressure_inserter: intermittent_single_cycles (Generator to intermittently insert a single cycle pulse)
                                                                                                                                	config_coroutine: randomly_switch_config (Twiddle the byteswapping config register)
                                                                                                                                	data_in: random_packet_sizes (random string data of a random length)
                                                                                                                                	idle_inserter: wave ()
                                                                                                                                
16275021000000000.00ns INFO     cocotb.scoreboard.endian_swapper          scoreboard.py:216  in add_interface                   Created with reorder_depth 0
16310021000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 22 bytes
16365021000000000.00ns INFO     cocotb.endian_swapper.stream_out              avalon.py:210  in _monitor_recv                   Received a packet of 49 bytes
16365021000000000.00ns ERROR    ..reboard.endian_swapper.stream_out       scoreboard.py:141  in compare                         Received transaction differed from expected output
16365021000000000.00ns INFO     ..reboard.endian_swapper.stream_out       scoreboard.py:145  in compare                         Expected:
                                                                                                                                '\xfd\xa5\x1eJ\xea]q-\x1dp[p1"\x88\xa3\xc17;[\x84\xc9\x0c1\xec\xe1H\xf9\xb1\x1b4\xb9w\x18\xf3-\xa9\xaa\xb3-\xd0\xb6\xf4F\xf5\xb6\xf6\xbc\xff'
16365021000000000.00ns INFO     ..reboard.endian_swapper.stream_out       scoreboard.py:155  in compare                         Received:
                                                                                                                                '\xfd\xa5\x1e\x95\xd4]q-\x1dp[\xe0b"\x88\xa3\xc17;\xb7\x08\xc9\x0c1\xec\xe1H\xf3c\x1b4\xb9w\x18\xf3[R\xaa\xb3-\xd0\xb6\xf4\x8d\xea\xb6\xf6\xbc\xff'
16365021000000000.00ns WARNING  ..reboard.endian_swapper.stream_out       scoreboard.py:162  in compare                         Difference:
                                                                                                                                0000      FDA51E4AEA5D712D 1D705B70312288A3 ...J.]q-.p[p1"..
                                                                                                                                     0000 FDA51E95D45D712D 1D705BE0622288A3 .....]q-.p[.b"..
                                                                                                                                0010      C1373B5B84C90C31 ECE148F9B11B34B9 .7;[...1..H...4.
                                                                                                                                     0010 C1373BB708C90C31 ECE148F3631B34B9 .7;....1..H.c.4.
                                                                                                                                0020      7718F32DA9AAB32D D0B6F446F5B6F6BC w..-...-...F....
                                                                                                                                     0020 7718F35B52AAB32D D0B6F48DEAB6F6BC w..[R..-........
                                                                                                                                0030 0030 FF                                               .
                                                                                                                                
16365022000000000.00ns ERROR    cocotb.regression                         regression.py:300  in handle_result                   Test Failed: run_test_022 (result was TestFailure)
29225032000000000.00ns ERROR    cocotb.regression                         regression.py:207  in tear_down                       Failed 1 out of 2 tests (0 skipped)
29225032000000000.00ns INFO     cocotb.regression                         regression.py:375  in _log_test_summary               ********************************************************************************
                                                                                                                                ** TEST                    PASS/FAIL  SIM TIME(NS)  REAL TIME(S)  RATIO(NS/S) **
                                                                                                                                ********************************************************************************
                                                                                                                                ** testbench.run_test_021    PASS     775001000000000.00          0.12   6732285484727734.00  **
                                                                                                                                ** testbench.run_test_022    FAIL     90001000000000.00          0.02   4378084203797130.50  **
                                                                                                                                ********************************************************************************
                                                                                                                                
29225032000000000.00ns INFO     cocotb.regression                         regression.py:392  in _log_sim_summary                *************************************************************************************
                                                                                                                                **                                 ERRORS : 1                                      **
                                                                                                                                *************************************************************************************
                                                                                                                                **                               SIM TIME : 29225032000000000.00 NS                **
                                                                                                                                **                              REAL TIME : 3.97 S                                 **
                                                                                                                                **                        SIM / REAL TIME : 7364444571542619.00 NS/S               **
                                                                                                                                *************************************************************************************
                                                                                                                                
29225032000000000.00ns INFO     cocotb.regression                         regression.py:219  in tear_down                       Shutting down..."""


class TestFileParsing(unittest.TestCase):
    def test_get_errors(self):
        result = get_errors(content)
        self.assertEqual(result, "1")

    def test_get_simtimefile(self):
        result = get_simtimefile(content)
        self.assertEqual(result, "29225032000000000.00")

    def test_get_realtimefile(self):
        result = get_realtimefile(content)
        self.assertEqual(result, "3.97")

    def test_get_testname(self):
        result = []
        justneededpart = content.split("tests")
        testparts = justneededpart[0].split("Running")
        for eachtestpart in testparts:
            if get_testname(eachtestpart) is not None :
                result.append(get_testname(eachtestpart))
        self.assertEqual(result, ["run_test_021", "run_test_022"])

    def test_get_testsstatus(self):
        result = get_testsstatus(content)
        self.assertEqual(result, ["PASS", "FAIL"])

    def test_get_testssimtime(self):
        result = get_testssimtime(content)
        self.assertEqual(result, ["775001000000000.00", "90001000000000.00"])

    def test_get_testsrealtime(self):
        result = get_testsrealtime(content)
        self.assertEqual(result, ["0.12", "0.02"])
#     def test_get_logline(self):
#         result = get_logline(content)
#         self.assertEqual(result, ["""regression.py:321  in execute                         Running test 21/32: run_test_021
# decorators.py:253  in _advance                        Starting test: "run_test_021"
#                                                       Description: Automatically generated test
                                                                                                                                
#                                                   	backpressure_inserter: intermittent_single_cycles (Generator to intermittently insert a single cycle pulse)
#                                                   	config_coroutine: randomly_switch_config (Twiddle the byteswapping config register)
#                                                   	data_in: random_packet_sizes (random string data of a random length)
#                                                   	idle_inserter: None
                                                                                                                                
# scoreboard.py:216  in add_interface                   Created with reorder_depth 0
# avalon.py:210  in _monitor_recv                   Received a packet of 48 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 53 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 114 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 72 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 71 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 137 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 139 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 144 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 58 bytes
# avalon.py:210  in _monitor_recv                   Received a packet of 135 bytes
# testbench.py:111  in run_test                        DUT correctly counted 10 packets""", 
# ""])

if __name__ == '__main__':
    unittest.main()

