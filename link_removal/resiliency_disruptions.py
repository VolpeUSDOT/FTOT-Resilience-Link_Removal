
def make_disruption_scenarios(disrupt_type, disrupt_steps, scen_path):
    """
    Method to set up network disruption scenarios in FTOT.

    This will create a set of scenarios based off of a *completed* FTOT run,
    using the sum of betweenness centrality of the to-from nodes or the volume of the edges
    as the values to sort by. 'Disruption' in this case will be setting the route_cost to a very high number
    in the networkx_edge_costs table. This method just sets up the scenarios first.

    disrupt_type: string, BC for betweenness centrality or V for volume
    disrupt_steps: integer, number of edges to disrupt in sequence
    scen_path: location of completed FTOT run to start from
    """
    import os
    import shutil

    disrupt_root = os.path.join(os.path.split(scen_path)[0],
                                '_'.join([os.path.split(scen_path)[1], disrupt_type, 'disrupt']))

    if not os.path.exists(disrupt_root):
        os.mkdir(disrupt_root)

    # Loop over the steps and make a complete copy of the base scenario in each
    for step in range(disrupt_steps):
        disrupt_name = 'disrupt' + "{:02d}".format(step + 1)  # start at 1
        disrupt_scen_path = os.path.join(disrupt_root, disrupt_name)

        # Copy the content of source to destination. Remove if already exists
        if os.path.exists(disrupt_scen_path):
            shutil.rmtree(disrupt_scen_path)
        shutil.copytree(scen_path, disrupt_scen_path)

        # Remove maps and reports folders if exist
        if os.path.exists(os.path.join(disrupt_scen_path, 'Reports')):
            shutil.rmtree(os.path.join(disrupt_scen_path, 'Reports'))
        if os.path.exists(os.path.join(disrupt_scen_path, 'Maps')):
            shutil.rmtree(os.path.join(disrupt_scen_path, 'Maps'))

    print('Prepared ' + str(disrupt_steps) + ' scenarios based on ' + os.path.split(scen_path)[1])


def disrupt_network(disrupt_type, disrupt_steps, scen_path, edges_remove, disrupt_order_ascending=False):
    """
    Direct modification of networkx_edges table using sqlite3

    Depends on the above steps to generate the edges_remove table,
    which provides the sum of betweenness centrality and volume of each edge used in the optimal solution
    from a completed FTOT run

    edges_remove: pandas.DataFrame with at a minimum the columns edge_id, sum_BC, and volume
    """

    import sqlite3
    import os
    from lxml import etree

    disrupt_root = os.path.join(os.path.split(scen_path)[0],
                                '_'.join([os.path.split(scen_path)[1], disrupt_type, 'disrupt']))

    for step in range(disrupt_steps):
        disrupt_name = 'disrupt' + "{:02d}".format(step + 1)  # start at 1
        disrupt_scen_path = os.path.join(disrupt_root, disrupt_name)

        db_name = 'main.db'

        db_path = os.path.join(disrupt_scen_path, db_name)

        # Get list of edges to remove
        if disrupt_type == 'BC':
            edge_col = 'sum_BC'
        if disrupt_type == 'V':
            edge_col = 'volume'

        # Sort by the selected column, BC or V
        edges_remove = edges_remove.sort_values(by = edge_col, ascending = disrupt_order_ascending)

        remove_edges_list = edges_remove['edge_id'].iloc[:step + 1].to_list()
        remove_edges_list = str(remove_edges_list).replace('[', '(').replace(']', ')')

        # Set the cost in the networkx_edge_costs table for this list of edges to a high value
        with sqlite3.connect(db_path) as db_con:
            sql = """update networkx_edge_costs
                     set route_cost = 99999
                     where edge_id in """ + remove_edges_list + ";"
            db_con.execute(sql)
        db_con.close()

        # Also edit the name in the scenario.xml
        fullPathToXmlConfigFile = os.path.join(disrupt_scen_path, 'scenario.xml')

        parser = etree.XMLParser(remove_blank_text = True)

        xml_etree = etree.parse(fullPathToXmlConfigFile, parser)

        # Identify specific element path
        # Only runs until a valid path is found for one file
        element_path = "{Schema_v7.0.0}Scenario_Name"

        target_elem = xml_etree.find(element_path)
        target_elem.text = disrupt_name
        with open(fullPathToXmlConfigFile, 'wb') as wf:
            xml_etree.write(wf, pretty_print = True)

    print('Disrupted ' + str(disrupt_steps) + ' scenarios')


def run_o_steps(disrupt_type, disrupt_steps, scen_path, PYTHON, FTOT, MAKE_MAPS):
    """
    Run the FTOT model from the 'O' optimization steps on

    Runs o1, o2, p, d, and (if MAKE_MAPS is True) m steps. This uses the output of an existing FTOT run, in particular the
    main.db, and re-runs the optimization, post-processing, reporting, and mapping steps. Not run are
    the setup, facilities, connectivity, and graph steps.
    This method also extracts key outputs from the log of the o2 step, namely unmet demand and
    total scenario cost.
    """
    import re
    import os
    import pandas as pd

    results_df = []

    disrupt_root = os.path.join(os.path.split(scen_path)[0],
                                '_'.join([os.path.split(scen_path)[1], disrupt_type, 'disrupt']))

    for step in range(disrupt_steps):
        disrupt_name = 'disrupt' + "{:02d}".format(step + 1)  # start at 1
        disrupt_scen_path = os.path.join(disrupt_root, disrupt_name)

        XMLSCENARIO = os.path.join(disrupt_scen_path, 'scenario.xml')

        # STEP OPTIMIZATION: SET UP THE OPTIMIZATION PROBLEM
        print('Running o1 for ' + disrupt_name)

        cmd = PYTHON + ' ' + FTOT + ' ' + XMLSCENARIO + ' o1'
        os.system(cmd)

        # STEP OPTIMIZATION: BUILD THE OPTIMIZATION PROBLEM AND SOLVE
        print('Running o2 for ' + disrupt_name)

        cmd = PYTHON + ' ' + FTOT + ' ' + XMLSCENARIO + ' o2'
        os.system(cmd)

        # STEP POST-PROCESSING
        print('Running p for ' + disrupt_name)

        cmd = PYTHON + ' ' + FTOT + ' ' + XMLSCENARIO + ' p'
        os.system(cmd)

        # STEP REPORTING
        print('Running d for ' + disrupt_name)

        cmd = PYTHON + ' ' + FTOT + ' ' + XMLSCENARIO + ' d'
        os.system(cmd)

        # STEP MAPPING
        if MAKE_MAPS:
            print('Running m for ' + disrupt_name)

            cmd = PYTHON + ' ' + FTOT + ' ' + XMLSCENARIO + ' m'
            os.system(cmd)
        
        # Get values out of the o2 step log
        # TODO: consider extracting other relevant metrics to bring into the R Markdown report
        log_path = os.path.join(disrupt_scen_path, 'logs')

        # Find most recent o2 step log
        log_list = []

        for log in os.listdir(log_path):
            if re.match('o2_', log):
                log_list.append(log)
        latest_log = log_list[len(log_list)-1]

        print('Preparing to search over ' + latest_log)

        # unmet_pattern = '(?:INFO\s+Total Unmet Demand : )(\d*.?\d*)'
        unmet_cost_pattern = '(?:RESULT\s+Total Unmet Demand Penalty:\s+)(\d+(?:,\d+)?)'
        nedge_pattern = '(?:INFO\s+number of optimal edges:\s+)(\d+)'
        total_cost_pattern = '(?:RESULT\s+Optimal Objective Value:\s+)(\d+(?:,\d+)?)'

        # \s any white space
        # \D non-digit
        # Cost values are comma-separated, so need to include comma as a non-capturing group as well
        # Use https://www.garrickadenbuie.com/project/regexplain/ to test
        # Use noncapturing groups to find the line, then capture the numerical output

        unmet_cost = []
        nedge = []
        total_cost = []

        with open(os.path.join(log_path, latest_log), 'r') as textfile:
            for line in textfile:
                unmet_cost += re.findall(unmet_cost_pattern, line)
                nedge += re.findall(nedge_pattern, line)
                total_cost += re.findall(total_cost_pattern, line)

        z1 = zip(["{:02d}".format(step + 1)], unmet_cost, nedge, total_cost)

        results_df_step = pd.DataFrame(z1, columns = ['disrupt_step',
                                                      'unmet_cost',
                                                      'nedge',
                                                      'total_cost'])

        print(results_df_step)

        results_df.append(results_df_step)

    results_df = pd.concat(results_df).reset_index()

    results_df.to_csv(os.path.join(disrupt_root, 'Results.csv'), index = False)

    return results_df


def evenness_metrics(dbname, use_mode = 'road'):
    """Function to calculate evenness of network using three different measures of link importance.

    dbname: full path to the FTOT database, main.db
    use_mode: layer of the transportation network to use (currently just one string, can flex to a list)
    For example: dbname= C:\FTOT\scenarios\reference_scenarios\rs7_capacity\main.db
    It will read from the `edges` table of that database.
    """
    import os
    import sqlalchemy
    import pandas as pd
    import numpy as np

    db_path = 'sqlite:///' + os.path.join(dbname)
    engine = sqlalchemy.create_engine(db_path)
    table_name = 'edges'
    edges = pd.read_sql_table(table_name, engine)
    # Subset to just the target transportation modes
    # and keep only unique edges
    edges = edges[edges['mode'] == use_mode]
    edges = edges.drop_duplicates(subset=['mode_oid'])

    S = edges.shape[0]
    Hmax = np.log(S)

    metric_list = []

    weighted_metric_list = []

    # Available Capacity

    sum_weight = edges['capac_minus_volume_zero_floor'].sum()
    props = edges['capac_minus_volume_zero_floor'] / sum_weight
    # np.nansum(props) == 1 # Must equal 1, can add this as a stopping criterion

    Hprime = -1 * np.nansum(np.log(props).multiply(props))
    Evenness_capac = Hprime / Hmax

    metric_list.append(Evenness_capac)

    weighted_metric_list.append(sum_weight * Evenness_capac)

    # Volume

    sum_weight = edges['volume'].sum()
    props = edges['volume'] / sum_weight
    Hprime = -1 * np.nansum(np.log(props).multiply(props))
    Evenness_vol = Hprime / Hmax

    metric_list.append(Evenness_vol)

    weighted_metric_list.append(sum_weight * Evenness_vol)

    # Length

    sum_weight = edges['length'].sum()
    props = edges['length'] / sum_weight
    Hprime = -1 * np.nansum(np.log(props).multiply(props))
    Evenness_dist = Hprime / Hmax

    metric_list.append(Evenness_dist)

    weighted_metric_list.append(sum_weight * Evenness_dist)


    metric_df = pd.DataFrame(zip(metric_list, weighted_metric_list),
                             columns = ['Evenness', 'Weighted_Evenness'],
                             index = ['Evenness_AvailCapac', 'Evenness_Vol', 'Evenness_Len'])


    return metric_df


def edges_from_line(geom, attrs):
    """
    Generate edges for each line in geom
    Written as a helper for read_gdb
    """
    from osgeo import ogr
    if geom.GetGeometryType() == ogr.wkbLineString:
        edge_attrs = attrs.copy()
        last = geom.GetPointCount() - 1
        edge_attrs["Wkb"] = geom.ExportToWkb()
        edge_attrs["Wkt"] = geom.ExportToWkt()
        edge_attrs["Json"] = geom.ExportToJson()
        yield (geom.GetPoint_2D(0), geom.GetPoint_2D(last), edge_attrs)

    elif geom.GetGeometryType() == ogr.wkbMultiLineString:
        for i in range(geom.GetGeometryCount()):
            geom_i = geom.GetGeometryRef(i)
            for edge in edges_from_line(geom_i, attrs):
                yield edge


def read_gdb(path, fc):
    
    import networkx as nx
    from osgeo import ogr
    
    net = nx.MultiDiGraph()
    gdb = ogr.Open(path)
    if gdb is None:
        raise RuntimeError("Unable to open {}".format(path))
    for lyr in gdb:
        if lyr.GetName() == fc:
            count = lyr.GetFeatureCount()
            fields = [x.GetName() for x in lyr.schema]
            for f in lyr:
                g = f.geometry()
                fld_data = [f.GetField(f.GetFieldIndex(x)) for x in fields]
                attributes = dict(list(zip(fields, fld_data)))
                attributes["ShpName"] = lyr.GetName()
                if g.GetGeometryType() == ogr.wkbPoint:
                    net.add_node(g.GetPoint_2D(0), **attributes)
                elif g.GetGeometryType() in (ogr.wkbLineString,
                                            ogr.wkbMultiLineString):
                    for edge in edges_from_line(g, attributes):
                        e1, e2, attr = edge
                        net.add_edge(e1, e2)
                        key = len(list(net[e1][e2].keys())) - 1
                        net[e1][e2][key].update(attr)
                else:
                    raise nx.NetworkXError("GeometryType {} not supported".
                                        format(g.GetGeometryType()))

    return net