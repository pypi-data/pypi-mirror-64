from .gamedata import getPlayers, getPointLog, getMatches, getUnplayed, getDisqualified
from .pwr import PWRsystems
from .regression import Regression
from .simulate import simulateBracket, simulateMatch, simulateGamelog
from .players import Player, Players
from .tiebreak import getPlayoffSeeding
from .util import playoff_series_ids
from joblib import Parallel, delayed
import pandas as pd
import numpy as np

class Simulate(object):
    def __init__(self, n_sims, pwr_systems=None, rank_adj=0.5, st_dev=1.6, season=2):
        self.n_sims = n_sims
        self.rank_adj = rank_adj
        self.st_dev = st_dev
        self.season = season
        if pwr_systems is None:
            self.pwr_systems = PWRsystems()
        else:
            self.pwr_systems = pwr_systems
        self.players = getPlayers(season)
        self.points = getPointLog(season)
        self.played = getMatches(season)
        self.unplayed = getUnplayed(season)
        self.dq = getDisqualified(season)
        for system in self.pwr_systems.systems:
            system.calculate(gamelog=self.points, season=season)
            self.regress(system)
        self.pwr = self.pwr_systems.combine()
        self.regress(self.pwr)

    def run(self, parallel=True, combine=True):
        simulations = []
        if parallel:
            simulations = Parallel(n_jobs=-1)(delayed(self.simulate)() for i in range(self.n_sims))
        else:
            for i in range(self.n_sims):
                simulations.append(self.simulate())
        self.simulations = Simulations(simulations, combine)
        return self

    def playoffs(self, reindex=False):
        if self.simulations.combined:
            return self.copied(self.simulations.playoffs.copy(), reindex)

    def regularseason(self, reindex=False):
        if self.simulations.combined:
            return self.copied(self.simulations.regularseason.copy(), reindex)
    
    def standings(self, reindex=False):
        if self.simulations.combined:
            return self.copied(self.simulations.standings.copy(), reindex)

    def copied(self, df, reindex):
        if reindex:
            return df.reset_index(level='Simulation')
        else:
            return df
            
    def simulate(self):
        return Simulation(self)

    def regress(self, system):
        if system.regress_to is not None:
            if type(system.regress_to) is not Regression:
                system.regress_to = Regression(to=system.regress_to)
            system.regress(system.values)

class Simulation(object):
    def __init__(self, sim):
        self.rankings = sim.pwr.values.copy()
        pwr_adjustments = np.random.normal(0, sim.rank_adj, self.rankings.shape[0])
        self.rankings['PWR'] = self.rankings['PWR'].values - pwr_adjustments
        if sim.unplayed.empty:
            self.regularseason = sim.played
        else:
            simulated = simulateGamelog(sim.unplayed, self.rankings, sim.st_dev, sim.season)
            self.regularseason = pd.concat([sim.played, simulated], ignore_index=True)
        adjusted = pd.DataFrame([x + [1] for x in self.regularseason[['Winner','Loser','W Pts']].values.tolist()] +
                                [x + [0] for x in self.regularseason[['Loser','Winner','L Pts']].values.tolist()],
                                columns=['Player','Opponent','Pts','Wins'])
        df = pd.merge(pd.merge(adjusted, sim.players, on='Player'), 
                      sim.players.rename({'Player':'Opponent','Division':'OppDivision'}, axis=1), on='Opponent')
        self.standings = pd.merge(df.groupby(['Player','Division']).agg({'Pts':'sum','Wins':'sum'}).reset_index(), 
                                  self.rankings, on='Player')
        df['Wins'] = np.where(np.isin(df['Player'].values, sim.dq), 0, df['Wins'].values)
        self.seeding = getPlayoffSeeding(df)
        self.playoffs = self.simulatePlayoffs(sim)
        self.standings = pd.merge(self.standings, self.seeding, how='left', on='Player', suffixes=('', '_')).drop('Division_', axis=1)
        
    def simulatePlayoffs(self, sim):
        players = Players(pd.merge(self.standings, self.seeding, on='Player', suffixes=('', '_')).drop('Division_', axis=1))
        bracket = simulateBracket(players, st_dev=sim.st_dev)
        results = dict((playoff_series_ids[key], value) for (key, value) in bracket.items())
        df = pd.DataFrame.from_dict(results, orient='index').reset_index()
        df[['Round','Series']] = pd.DataFrame(df[['level_0','level_1']].values.tolist(), index=df.index)
        return df[['Round','Series','Winner','Loser','Games']]

class Simulations(object):
    def __init__(self, values, combine=True):
        self.combined = combine
        if combine:
            indices = list(range(len(values)))
            self.playoffs = pd.concat([x.playoffs for x in values], keys=indices).rename_axis(['Simulation','Row'])
            self.standings = pd.concat([x.standings for x in values], keys=indices).rename_axis(['Simulation','Row'])
            self.regularseason = pd.concat([x.regularseason for x in values], keys=indices).rename_axis(['Simulation','Row'])
        else:
            self.values = values
