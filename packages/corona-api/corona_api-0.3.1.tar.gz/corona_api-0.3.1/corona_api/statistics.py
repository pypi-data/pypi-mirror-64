class GlobalStatistics:
    def __init__(self, cases, deaths, recoveries, today_cases, today_deaths, total_critical, updated):
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.critical = total_critical
        self.updated = updated


class CountryStatistics:
    def __init__(self, name, cases, deaths, recoveries, today_cases, today_deaths, critical, cases_per_million):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.critical = critical
        self.cases_per_million = cases_per_million


class StateStatistics:
    def __init__(self, name, cases, deaths, recoveries, today_cases, today_deaths, active):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.active = active


class CountryHistory:
    def __init__(self, name, dicts):
        self.name = name
        self.case_history = dicts[0]
        self.death_history = dicts[1]
        self.recovery_history = dicts[2]