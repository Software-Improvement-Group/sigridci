#!/usr/bin/env python3

# Copyright Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict
from colors import color
from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pygal import Bar, HorizontalStackedBar, Line, Radar, StackedBar
from pygal.style import Style
from objectives import Group, ObjectivesCalculator, Period, Status, SystemFilter, OBJECTIVE_TYPES
from sigrid_api_client import SigridApiClient


TODAY = datetime.now()
LAST_YEAR = TODAY + relativedelta(years=-1)
SUCCESS_COLORS = ("#57C968", "#EF981A")
TEAM_COLORS = ("#8269A4", "#DFC101", "#04ABC8", "#233347", "#C5CD58", "#D45200", "#E6E1ED", "#A3912E", "#92d7e3", "#687483") 
STATUS_COLORS = ("#04ABC8", "#C3F5FE", "#F0F3F8")
METADATA_COLORS = ("#8269A4", "#E6E1ED")
FILENAME = re.compile("/")

CONDITION_DISPLAY_NAMES = {
    "businessCriticality" : "Business criticality",
    "lifecyclePhase" : "Lifecycle phase",
    "deploymentType" : "Deployment type"
}
    
    
def generateGroupedObjectivesStatusChart(calculator, outputFile):
    systems = calculator.status
    types = list(reversed(calculator.getAvailableObjectiveTypes(systems)))
    statusPercentages = {type: calculator.calculateStatus(systems, type) for type in types}

    chart = HorizontalStackedBar(width=600, height=400, range=(0, 100), style=getChartStyle(STATUS_COLORS), legend_at_bottom=True)
    chart.title = f"Sigrid objectives status"
    chart.x_labels = [OBJECTIVE_TYPES[type] for type in types]
    chart.value_formatter = lambda value: f"{round(value)}%"
    chart.add("Complete", [statusPercentages[type][Status.COMPLETE] for type in types])
    chart.add("Incomplete", [statusPercentages[type][Status.INCOMPLETE] for type in types])
    chart.add("Not covered", [statusPercentages[type][Status.NA] for type in types])
    chart.render_to_file(outputFile)
    
    
def generateTeamObjectivesStatusChart(calculator, outputFile):
    teamSystems = calculator.groupSystems(calculator.status, Group.TEAM)
    statusPercentages = {team: calculator.calculateStatus(systems) for team, systems in teamSystems.items()}
    
    chart = HorizontalStackedBar(width=600, height=400, range=(0, 100), style=getChartStyle(STATUS_COLORS), legend_at_bottom=True)
    chart.title = "Sigrid objectives status per team"
    chart.x_labels = teamSystems.keys()
    chart.value_formatter = lambda value: f"{round(value)}%"
    chart.add("Complete", [statusPercentages[team][Status.COMPLETE] for team in teamSystems])
    chart.add("Incomplete", [statusPercentages[team][Status.INCOMPLETE] for team in teamSystems])
    chart.add("Not covered", [statusPercentages[team][Status.NA] for team in teamSystems])
    chart.render_to_file(outputFile)
    
    
def generateGroupedObjectivesTrendChart(calculator, type, systemFilter, outputFile):
    periods = calculator.periods
    metadata = calculator.metadata
    trend = {period: calculator.calculateStatus(systemFilter.apply(calculator.trend[period], metadata), type) for period in periods}
    
    chart = StackedBar(width=600, height=400, range=(0, 100), style=getChartStyle(STATUS_COLORS), legend_at_bottom=True)
    chart.title = f"{OBJECTIVE_TYPES[type]} objective trend"
    chart.x_labels = [period.start.strftime("%m/%Y") for period in periods]        
    chart.value_formatter = lambda value: f"{round(value)}%"
    chart.add("Complete", [trend[period][Status.COMPLETE] for period in periods])
    chart.add("Incomplete", [trend[period][Status.INCOMPLETE] for period in periods])
    chart.add("Not covered", [trend[period][Status.NA] for period in periods])
    chart.render_to_file(outputFile)
    
    
def generateMetadataCompletionChart(calculator, group, outputFile):
    groups = calculator.groupSystems(calculator.status, group)
    countMetadataComplete = lambda systems: sum(1 for system in systems if calculator.isMetadataComplete(system))
    withMetadata = [countMetadataComplete(systems) for group, systems in groups.items()]
    withoutMetadata = [len(systems) - countMetadataComplete(systems) for group, systems in groups.items()]

    chart = HorizontalStackedBar(width=600, height=400, style=getChartStyle(METADATA_COLORS), legend_at_bottom=True)
    chart.title = f"Sigrid metadata status per {group}"
    chart.x_labels = groups.keys()
    chart.add("With metadata", withMetadata)
    chart.add("Without metadata", withoutMetadata)
    chart.render_to_file(outputFile)
    
    
def generateRadarChart(name, systems, outputFile):
    types = calculator.getAvailableObjectiveTypes(systems)
    status = [calculator.calculateStatus(systems, type)[Status.COMPLETE] for type in types]

    chart = Radar(width=400, height=400, style=getChartStyle(STATUS_COLORS), range=(0, 100), legend_at_bottom=True)
    chart.title = f"Sigrid objectives status for {name}"
    chart.x_labels = [OBJECTIVE_TYPES[type] for type in types]
    chart.value_formatter = lambda value: f"{round(value)}%"
    chart.add("Complete", status)
    chart.render_to_file(outputFile)
    
    
def generateObjectivesBreakdownChart(calculator, type, groupedSystems, outputFile):
    periods = calculator.periods

    chart = Line(width=600, height=400, range=(0, 100), style=getChartStyle(TEAM_COLORS), legend_at_bottom=True)
    chart.title = f"{OBJECTIVE_TYPES[type]} objective trend"
    chart.x_labels = [period.start.strftime("%m/%Y") for period in periods]        
    chart.value_formatter = lambda value: f"{round(value)}%"
    for name in sorted(groupedSystems.keys()):
        systemNames = [system["systemName"] for system in groupedSystems[name]]
        systemFilter = lambda system: system["systemName"] in systemNames
        status = [calculator.calculateStatus(calculator.trend[period], type, filter=systemFilter)[Status.COMPLETE] for period in periods]
        chart.add(name, status)
    chart.render_to_file(outputFile)
    
    
def getChartStyle(colors):
    return Style(
        background="#FFFFFF",
        font_family="Calibri",
        opacity=1.0,
        colors=colors,
        stroke_width=4
    )
    
    
def formatTitle(objective):
    type = objective["objective"]["type"]
    title = OBJECTIVE_TYPES.get(type, type)
    
    if objective["conditions"].get("unconditional", False):
        return title
        
    formatField = lambda field: CONDITION_DISPLAY_NAMES.get(field, field)
    formatValues = lambda values: ", ".join(values).lower().replace("_", " ")
    conditions = [f"{formatField(field)}: {formatValues(values)}" for field, values in objective["conditions"].items()]
    return f"{title} ({', '.join(conditions)})"
    
    
def formatDateRange(start, end):
    return f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"
    
    
def createOutputDir(parentDir, name):
    dir = parentDir + "/" + FILENAME.sub("", name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir
    
    
if __name__ == "__main__":
    parser = ArgumentParser(description="Generates a progress report based on a your Sigrid portfolio objectives.")
    parser.add_argument("customer", type=str, help="Sigrid customer name.")
    parser.add_argument("--start", type=str, default=LAST_YEAR.strftime("%Y-%m-%d"), help="Start date (yyyy-mm-dd).")
    parser.add_argument("--end", type=str, default=TODAY.strftime("%Y-%m-%d"), help="End date (yyyy-mm-dd).")
    parser.add_argument("--out", type=str, help="Output directory path.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com")
    args = parser.parse_args()
    
    if None in [args.customer, args.out]:
        parser.print_help()
        sys.exit(1)
        
    if not os.environ.get("SIGRID_CI_TOKEN"):
        print("Missing Sigrid API token in environment variable SIGRID_CI_TOKEN")
        sys.exit(1)
        
    sigrid = SigridApiClient(args.sigridurl, args.customer, os.environ["SIGRID_CI_TOKEN"])
    startDate = datetime.strptime(args.start, "%Y-%m-%d")
    endDate = datetime.strptime(args.end, "%Y-%m-%d")
    calculator = ObjectivesCalculator(sigrid, startDate, endDate)
    divisions = calculator.groupSystems(calculator.status, Group.DIVISION)
    teams = calculator.groupSystems(calculator.status, Group.TEAM)    
    outputDir = createOutputDir(os.path.expanduser(args.out), args.customer)
        
    for type in calculator.getAvailableObjectiveTypes(calculator.status):
        generateGroupedObjectivesTrendChart(calculator, type, SystemFilter(), f"{outputDir}/trend-{type.lower()}.svg")
        generateObjectivesBreakdownChart(calculator, type, divisions, f"{outputDir}/breakdown-divisions-{type}.svg")
        generateObjectivesBreakdownChart(calculator, type, teams, f"{outputDir}/breakdown-teams-{type}.svg")

    for division, systems in divisions.items():
        divisionDir = createOutputDir(outputDir, "Division " + division)
        generateRadarChart(division, systems, f"{divisionDir}/radar.svg")
        for type in calculator.getAvailableObjectiveTypes(systems):
            systemFilter = SystemFilter(division=division)
            generateGroupedObjectivesTrendChart(calculator, type, systemFilter, f"{divisionDir}/trend-{type.lower()}.svg")
    
    for team, systems in teams.items():
        teamDir = createOutputDir(outputDir, "Team " + team)
        generateRadarChart(team, systems, f"{teamDir}/radar.svg")
        for type in calculator.getAvailableObjectiveTypes(systems):
            systemFilter = SystemFilter(team=team)
            generateGroupedObjectivesTrendChart(calculator, type, systemFilter, f"{teamDir}/trend-{type.lower()}.svg")
