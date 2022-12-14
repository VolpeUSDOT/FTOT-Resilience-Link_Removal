import os
import lxml_upgrade_tool
import run_upgrade_tool
import input_csv_templates_tool
import scenario_compare_tool
import gridded_data_tool
import xml_text_replacement_tool
import network_disruption_tool
from six.moves import input

header = "\n\
 _______  _______  _______  _______    _______  _______  _______  ___      _______\n\
|       ||       ||       ||       |  |       ||       ||       ||   |    |       |\n\
|    ___||_     _||   _   ||_     _|  |_     _||   _   ||   _   ||   |    |  _____|\n\
|   |___   |   |  |  | |  |  |   |      |   |  |  | |  ||  | |  ||   |    | |_____ \n\
|    ___|  |   |  |  |_|  |  |   |      |   |  |  |_|  ||  |_|  ||   |___ |_____  |\n\
|   |      |   |  |       |  |   |      |   |  |       ||       ||       | _____| |\n\
|___|      |___|  |_______|  |___|      |___|  |_______||_______||_______||_______|\n"


def xml_tool():
    print("You called xml_tool()")
    xml_file_location = lxml_upgrade_tool.repl()


def bat_tool():
    print("You called bat_tool()")
    run_upgrade_tool.run_bat_upgrade_tool()
    input("Press [Enter] to continue...")


def compare_tool():
    print("You called compare_tool()")
    scenario_compare_tool.run_scenario_compare_prep_tool()
    input("Press [Enter] to continue...")


def raster_tool():
    print("You called aggregate_raster_data()")
    gridded_data_tool.run()
    input("Press [Enter] to continue...")


def csv_tool():
    print("You called csv_tool()")
    input_csv_templates_tool.run_input_csv_templates_tool()
    input("Press [Enter] to continue...")


def pdb():
    print("You called pdb()")
    import pdb; pdb.set_trace()
    input("Press [Enter] to continue...")


def replace_xml_text_tool():
    print("You called replace_xml_text()")
    xml_text_replacement_tool.run()
    input("Press [Enter] to continue...")


def disrupt_tool():
    print("You called network_disruption_tool()")
    network_disruption_tool.run_network_disruption_tool()
    input("Press [Enter] to continue...")


menuItems = [
    {"xml_tool": xml_tool},
    {"bat_tool": bat_tool},
    {"scenario_compare_tool": compare_tool},
    {"aggregate_raster_data": raster_tool},
    {"generate_template_csv_files": csv_tool},
    {"replace_xml_text": replace_xml_text_tool},
    {"network_disruption_tool": disrupt_tool},
    {"breakpoint": pdb},
    {"exit": exit}
]


def main():
    while True:
        os.system('cls')
        print(header)
        print('version 0.1\n')
        print('select an option below to activate a tool')
        print('-----------------------------------------')
        for item in menuItems:
            print("[" + str(menuItems.index(item)) + "] " + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0:
                raise ValueError
            # Call the matching function
            list(menuItems[int(choice)].values())[0]()
        except (ValueError, IndexError):
            pass


if __name__ == "__main__":
    main()
