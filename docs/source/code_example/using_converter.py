import asyncio
import json
from xena_rfc_core import controller
from xena_rfc_converter.entry import converter
from xena_rfc_converter.types import TestSuiteType

# source config file to be converted
OLD_CONFIG_FILE = "my_old2544_config.v2544" 
NEW_CONFIG_FILE = "xoa2544.json"
T_SUITE_NAME = "RFC-2544"
PLUGINS_PATH =  "pluginlib"

async def start():

    # create an instance of xena python rfc core controller
    c = await controller.MainController()

    # open and read xena test config my_old2544_config.v2544
    with open(OLD_CONFIG_FILE) as f:
        app_data = f.read()

        # register rfc2544 plugin to core
        c.register_lib(str(PLUGINS_PATH))

        # get rfc2544 test suite information from the core's registration
        info = c.get_test_suite_info(T_SUITE_NAME)
        if not info:
            print("Test suite is not recognized.")
            return None
        
        # convert the old config into new config
        new_data = converter(TestSuiteType.RFC2544, app_data, info["schema"])

        # save the new config file xoa2544.json
        with open(NEW_CONFIG_FILE, "w") as f:
            f.write(new_data)
        
        # you can use the config file below to start the test
        new_config = json.loads(new_data)

        # Test suite name: "RFC-2544" is received from call of c.get_available_test_suites()
        # test_id = c.start_test_suite(T_SUITE_NAME, new_config)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()