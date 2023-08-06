# the main function gets as input a txt file which contains 10 lines (see below)

# 1st = path to csv file with the IDs of point locations (see Appendix)
# 2nd = path to folder where observations will be stored
# 3rd = path to forecasts where observations will be stored
# 4th = path to EVS template (see Appendix)
# 5th = path to folder where the EVS project will be stored
# 6th = path to EVS jar file
# 7th = path to csv file of monthly BSS values (see Appendix)
# 8th = path to folder where results will be stored
# 9th = username for Plotly's API (see Appendix)
# 10th = api_key for Plotly's API (see Appendix)

import plotly.graph_objs as go
import chart_studio.plotly as py
import chart_studio
from more_itertools import unique_everseen
import xml.etree.ElementTree as ET
import requests
import pandas as pd
import copy
import subprocess
import numpy as np
from xml.etree.ElementTree import fromstring, ElementTree
from xml.etree.ElementTree import ParseError
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
plt.style.use("ggplot")
pd.options.mode.chained_assignment = None


def main(txt):
    with open(txt) as f:
        content = f.read().splitlines()
    locations_csv = content[0]
    obs_path = content[1]
    fcst_path = content[2]
    template_path = content[3]
    project_path = content[4]
    EVS_path = content[5]
    score_csv = content[6]
    results_path = content[7]
    username = content[8]
    api_key = content[9]

    def getdata(locations_csv, obs_path, fcst_path):
        global locations
        global current_date
        locations = pd.read_csv(
            locations_csv, sep=";", header=None, names=["Location", "ID"])
        locations = list(locations.loc[:, "ID"])
        locations = sorted(locations)
        url = 'http://tw-151.xtr.deltares.nl:8081/FewsWebServices/rest/fewspiservice/v1/timeseries'
        request_parameters_obs = {'locationIds': '',
                                  'parameterIds': '', 'startTime': '', 'endTime': ''}
        current_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
        endperiod = current_date + "T00:00:00Z"
        startperiod = datetime.datetime.now() - relativedelta(years=1) + \
            relativedelta(days=1)
        startperiod = startperiod.date().strftime('%Y-%m-%d') + "T00:00:00Z"
        request_parameters_obs['parameterIds'] = "Q.obs"
        request_parameters_obs['startTime'] = startperiod
        request_parameters_obs['endTime'] = endperiod
        obs_not_found = []

        for i in locations:
            try:
                request_parameters_obs['locationIds'] = i
                response = requests.get(url, params=request_parameters_obs)
                response = response.content.decode('utf-8')
                tree = ElementTree(fromstring(response))
                path = obs_path + "/obs_" + i + ".xml"
                tree.write(path)
            except ParseError:
                obs_not_found.append(i)

        request_parameters_fcst = {'locationIds': '',
                                   'parameterIds': '', 'moduleInstanceIds': '', 'startTime': '', 'endTime': '', 'showEnsembleMemberIds': '', 'forecastCount': ''}
        request_parameters_fcst['parameterIds'] = "Q.simulated"
        request_parameters_fcst['moduleInstanceIds'] = 'SampleMeasLoc_Forecast_ECMWF-EPS'
        request_parameters_fcst['startTime'] = startperiod
        request_parameters_fcst['endTime'] = endperiod
        request_parameters_fcst['showEnsembleMemberIds'] = 'true'
        request_parameters_fcst['forecastCount'] = '1000000'
        fcst_not_found = []

        for i in locations:
            try:
                request_parameters_fcst['locationIds'] = i
                response = requests.get(url, params=request_parameters_fcst)
                response = response.content.decode('utf-8')
                tree = ElementTree(fromstring(response))
                path = fcst_path + "/fcst_" + i + ".xml"
                tree.write(path)
            except ParseError:
                fcst_not_found.append(i)

        not_found = set(obs_not_found + fcst_not_found)

        for i in not_found:
            locations.remove(i)
        return(locations)

    def createEVSproject(template_path, project_path, obs_path, fcst_path):
        tree = ET.parse(template_path)
        root = tree.getroot()
        verification_unit = tree.find('verification_unit')
        verification_unit_copy = copy.deepcopy(verification_unit)

        for i in range(len(locations) - 1):
            root.append(verification_unit_copy)

        tree.write(
            project_path + "/dummy_VUs.evs")
        tree = ET.parse(project_path + "/dummy_VUs.evs")
        count = 0

        for node in tree.iter('location_id'):
            node.text = locations[count]
            count += 1

        count = 0

        for node in tree.iter('forecast_data_source'):
            path = fcst_path + "/fcst_" + \
                locations[count] + ".xml"
            node[0].text = path
            count += 1

        count = 0

        for node in tree.iter('observed_data_source'):
            path = obs_path + "/obs_" + \
                locations[count] + ".xml"
            node[0].text = path
            count += 1

        root = tree.getroot()
        aggregation_unit = root.find("aggregation_unit")

        for i in locations:
            unit_id = ET.SubElement(aggregation_unit, "unit_id")
            unit_id.text = i + ".Streamflow"

        tree.write(project_path + "/myverification.evs")
        return()

    def runEVSproject(EVS_path, project_path):
        subprocess.call(
            ['java', '-jar', EVS_path, project_path + "/myverification.evs"])
        return()

    def readEVSskillscores(score_path, results_path):
        i = score_path.find("GROUPED.") + 8
        j = score_path.find(".xml", i)
        score_name = score_path[i:j]
        lead_hour = []
        values = []
        tree = ET.parse(score_path)
        for node in tree.iter("lead_hour"):
            lead_hour.append(node.text)
        for node in tree.iter("values"):
            values.append(node.text)
        lead_hour = np.array(lead_hour)
        lead_hour = lead_hour.astype(np.float)
        values = np.array(values)
        values = values.astype(np.float)
        plt.plot(lead_hour, values, linewidth=3)
        plt.ylim(0, 1)
        plt.xticks(lead_hour)
        plt.ylabel(score_name)
        plt.xlabel("Lead_time (hours)")
        plt.savefig(
            results_path + "/" + score_name + ".png", bbox_inches='tight')
        return(lead_hour, values)

    def interactiveBSS(score_csv, results_path, username, api_key):
        chart_studio.tools.set_credentials_file(
            username=username, api_key=api_key)
        dataframe = pd.read_csv(score_csv, sep=";")
        months_dict = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
                       "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
        months = list(unique_everseen(dataframe["Month"]))
        score_path = results_path + "/GROUPED.Brier_skill_score.xml"
        values = readEVSskillscores(score_path, results_path)[1]
        month = current_date[5:7]

        for n in months_dict.items():
            if n[1] == month:
                month = n[0]

        dataframe.loc[dataframe['Month'] == month, 'Value'] = values
        dataframe.to_csv(
            index=False, path_or_buf=score_csv, sep=";")
        fig = go.Figure()

        for m in months:
            x = np.array(
                [dataframe["Lead Time (hours)"].where(dataframe["Month"] == m)])
            x = x[~np.isnan(x)]
            y = np.array([dataframe["Value"].where(dataframe["Month"] == m)])
            y = y[~np.isnan(y)]
            fig.add_trace(go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=6),
                name=m,
                x=x,
                y=y))

        steps = []

        for i in range(len(fig.data)):
            step = dict(
                method="restyle",
                args=["visible", [False] * len(fig.data)],
                label=months[i])
            step["args"][1][i] = True
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Month: "},
            pad={"t": 50},
            steps=steps
        )]
        fig.update_layout(
            title=go.layout.Title(
                text="",
                xref="paper",
                x=0.5
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text="Lead Time (hours)",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                    )
                ),
                tickmode="linear",
                tick0=0,
                dtick=24
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text="Brier Skill Score",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                    )
                )
            ),
            sliders=sliders
        )
        fig.update_yaxes(range=[0, 1])
        py.plot(fig, validate=False, filename='BSS', auto_open=False)
        return()
    getdata(locations_csv, obs_path, fcst_path)
    createEVSproject(template_path, project_path, obs_path, fcst_path)
    runEVSproject(EVS_path, project_path)
    interactiveBSS(score_csv, results_path, username, api_key)
    return()
