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

import itertools
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sigrid_api_client import SigridApiClient


OBJECTIVE_TYPES = {
    "MAINTAINABILITY" : "Maintainability",
    "TEST_CODE_RATIO" : "Test code",
    "ARCHITECTURE_QUALITY" : "Architecture",
    "OSH_MAX_SEVERITY" : "Open Source vulnerabilities",
    "OSH_MAX_FRESHNESS_RISK" : "Open Source freshness",
    "OSH_MAX_LICENSE_RISK" : "Open Source licenses",
    "SECURITY_MAX_SEVERITY" : "Security",
    "RELIABILITY_MAX_SEVERITY" : "Reliability",
    "CLOUD_READINESS_MAX_SEVERITY" : "Cloud readiness"
}


class Status(Enum):
    COMPLETE = 1
    INCOMPLETE = 2
    NA = 3
    
    
class Group(Enum):
    DIVISION = 1
    TEAM = 2    


@dataclass
class Period:
    start: datetime
    end: datetime
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __hash__(self):
        return hash(str(self))
        
        
class SystemFilter:
    def __init__(self, *, division=None, team=None):
        self.division = division
        self.team = team
        
    def check(self, systemEvaluation, metadata):
        systemMetadata = metadata[systemEvaluation["systemName"]]
        active = systemMetadata["active"] and not systemMetadata["isDevelopmentOnly"]
        divisionMatch = self.division == None or self.division == (systemMetadata["divisionName"] or "Unknown")
        teamMatch = self.team == None or self.team in (systemMetadata["teamNames"] or "Unknown")
        return active and divisionMatch and teamMatch
        
    def apply(self, systemEvaluations, metadata):
        return [system for system in systemEvaluations if self.check(system, metadata)]


class ObjectivesCalculator:
    def __init__(self, sigrid, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.periods = self.getMonthlyPeriods()
        
        self.metadata = sigrid.fetchMetadata()
        self.rawPortfolioObjectives = sorted(sigrid.fetchPortfolioObjectives(), key=lambda o: o["objective"]["type"])
        self.status = sigrid.fetchObjectivesEvaluation(startDate, endDate)
        self.trend = {period: sigrid.fetchObjectivesEvaluation(period.start, period.end) for period in self.periods}
        
    # Returns a map from the specified groups to all systems in that group. Note that
    # systems can appear multiple times. For example, if a system is maintained by two
    # teams, it will appear for both teams in the grouping.
    def groupSystems(self, systemEvaluations, group):
        groups = defaultdict(list)
        for systemEvaluation in systemEvaluations:
            systemMetadata = self.metadata[systemEvaluation["systemName"]]
            for systemGroup in self.getSystemGroups(systemMetadata, group):
                groups[systemGroup].append(systemEvaluation)
        return {group: groups[group] for group in reversed(sorted(groups.keys()))}
        
    def getSystemGroups(self, systemMetadata, group):
        if group == Group.DIVISION:
            division = systemMetadata["divisionName"]
            return [division] if division else ["Unknown"]
        elif group == Group.TEAM:
            return systemMetadata["teamNames"] or ["Unknown"]
        else:
            raise Exception(f"Unknown group: {group}")
            
    def isMetadataComplete(self, systemEvaluation):
        systemMetadata = self.metadata[systemEvaluation["systemName"]]
        fields = ["divisionName", "teamNames", "businessCriticality", "lifecyclePhase"]
        return all(systemMetadata[field] for field in fields)
        
    def getMonthlyPeriods(self):
        months = []
        current = self.startDate
        while current < self.endDate:
            next = current + relativedelta(months=1)
            months.append(Period(current, next))
            current = next
        return months
        
    def getAvailableObjectiveTypes(self, systemEvaluations):
        found = set(soe["type"] for system in systemEvaluations for soe in system["objectives"])
        return [type for type in OBJECTIVE_TYPES if type in found]
        
    def calculateStatus(self, systemEvaluations, type="*", *, filter=None):
        statusCount = {status: 0 for status in Status}
        
        for system in systemEvaluations:
            if filter == None or filter(system):
                for systemObjectiveEvaluation in system["objectives"]:
                    if type in (systemObjectiveEvaluation["type"], None, "*"):
                        status = self.determineStatus(systemObjectiveEvaluation)
                        statusCount[status] += 1
                        
                if len(system["objectives"]) == 0:
                    statusCount[Status.NA] += 1
        
        total = sum(statusCount.values())    
        return {status: (count * 100.0 / total if total > 0 else 0) for status, count in statusCount.items()}
        
    def determineStatus(self, systemObjectiveEvaluation):
        if systemObjectiveEvaluation == None:
            return Status.NA
        elif systemObjectiveEvaluation["targetMetAtEnd"] == "MET":
            return Status.COMPLETE
        elif systemObjectiveEvaluation["targetMetAtEnd"] == "NOT_MET":
            return Status.INCOMPLETE
        else:
            return Status.NA
        
    def toPercentage(self, value, total):
        if total == 0:
            return 0.0
        return value * 100.0 / total
