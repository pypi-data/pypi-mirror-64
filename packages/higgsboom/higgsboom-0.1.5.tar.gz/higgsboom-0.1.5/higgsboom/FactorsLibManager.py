import os, sys, time, sqlalchemy
import pandas as pd
from dateutil.parser import parse
from higgsboom.DatabaseManager import *
from higgsboom.Exceptions import *

pd.set_option('mode.chained_assignment', None)

class FactorsLibManager(object):
	def __init__(self, userInfo, factorsLib):
		self.userInfo = userInfo
		self.factorsLib = factorsLib
		try:
			dbConfig = {'dbEngine':'mysql','user':self.userInfo['UserName'], 'passwd':self.userInfo['Password'], 'host':'10.214.0.21', 'dbName': self.factorsLib}
			self.engine = sqlalchemy.create_engine(EngineConfigToCreateStr(dbConfig), echo=False)
			self.conn = self.engine.connect()
		except Exception as e:
			print(e)
			sys.exit(-1)

	def ClearLibraryData(self):
		for table in self.engine.table_names():
			self.conn.execute('DROP TABLE %s' % table)
		print('finished clearing all library data for %s' % self.factorsLib)

#TickFactorsLibManager
def LocalInstTradingDates(rootDir):
	tdList = list()
	for (root, dirs, files) in os.walk(rootDir):
		for directory in dirs:
			tdList.append(directory)
	instTradingDates = dict()
	for td in tdList:
		for (root, dirs, files) in os.walk('%s%s/' % (rootDir, td)):
			for file in files:
				if file.endswith('.csv'):
					instrument = file[:-4]
					if not instrument in instTradingDates.keys():
						instTradingDates[instrument] = [td]
					else:
						instTradingDates[instrument].append(td)
	for key in instTradingDates.keys():
		instTradingDates[key].sort()
	return instTradingDates

def DailyTickFactorsFrame(rootDir, instrument, tradingDate):
	try:
		df = pd.read_csv('%s/%s/%s.csv' % (rootDir, tradingDate, instrument))
		df['TradingDate'] = tradingDate
		cols = df.columns.tolist()
		cols = cols[-1:] + cols[:-1]
		return df[cols]
	except:
		print('error, failed to get factors dataframe for %s on %s' % (instrument, tradingDate))

class TickFactorsLibManager(FactorsLibManager):
	def __init__(self, userInfo, factorsLib):
		print('FactorsLibManager: user %s managing %s' % (userInfo['UserName'], factorsLib))
		FactorsLibManager.__init__(self, userInfo, factorsLib)
		self.instTradingDates = dict()
		for tableName in self.engine.table_names():
			instrument = self.SqlTableNameToInstrument(tableName)
			tdList = [x[0] for x in self.conn.execute("SELECT DISTINCT TradingDate FROM %s" % tableName).fetchall()]
			self.instTradingDates[self.SqlTableNameToInstrument(tableName)] = tdList

	def CompleteFactorsFrame(self, instrument):
		try:
			tableName = self.InstrumentToSqlTableName(instrument)
			#res = self.conn.execute('SELECT * FROM %s' % tableName)
			#columns = [x['name'] for x in sqlalchemy.inspect(self.engine).get_columns(tableName)]
			return pd.DataFrame(self.conn.execute('SELECT * FROM %s' % tableName).fetchall(), columns= [x['name'] for x in sqlalchemy.inspect(self.engine).get_columns(tableName)])
		except:
			print('failed to get complete factors frame for %s' % instrument)

	def LibInstTradingDates(self):
		instTradingDates = dict()
		for tableName in self.engine.table_names():
			instrument = self.SqlTableNameToInstrument(tableName)
			tdList = [x[0] for x in self.conn.execute("SELECT DISTINCT TradingDate FROM %s" % tableName).fetchall()]
			tdList.sort()
			instTradingDates[self.SqlTableNameToInstrument(tableName)] = tdList
		return instTradingDates

	def BuildFactorsLib(self, rootDir):
		opt = input('Ready to build %s, this operation will overwrite all existing library data, continue?(y/n)' % self.factorsLib)
		if opt in ['y', 'Y']:
			self.ClearLibraryData()
		else:
			return
		instTradingDates = LocalInstTradingDates(rootDir)
		for instrument in instTradingDates.keys():
			try:
				completeDf = pd.concat([DailyTickFactorsFrame(rootDir, instrument, td) for td in instTradingDates[instrument]], axis=0)
				tbName = self.InstrumentToSqlTableName(instrument)
				print('writing all factor library data for %s ... ' % instrument, end='')
				t0 = time.time()
				completeDf.to_sql(con=self.conn, name=tbName, if_exists='replace', index=False)
				print('time elapsed %.2fs' % (time.time() - t0))
			except Exception as e:
				print(e)
				print('failed to write all factors data for %s' % instrument)

	def UpdateDailyFactorsData(self, rootDir, instList, tradingDate):
		for instrument in instList:
			df = DailyTickFactorsFrame(rootDir, instrument, tradingDate)
			tbName = self.InstrumentToSqlTableName(instrument)
			try:
				t0 = time.time()
				print('updating factor library data for %s on %s ... ' % (instrument, tradingDate), end='')
				df.to_sql(con=self.conn, name=tbName, if_exists='append', index=False)
				print('time elapsed %.2fs' % (time.time() - t0))
			except Exception as e:
				print(e)
				print('failed to write data for %s on %s to %s' % (instrument, tradingDate, self.factorsLib))

	def InstrumentToSqlTableName(self, instrument):
		return instrument

	def SqlTableNameToInstrument(self, sqlTableName):
		return sqlTableName