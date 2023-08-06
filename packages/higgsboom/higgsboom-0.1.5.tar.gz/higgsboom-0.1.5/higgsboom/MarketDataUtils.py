# -*- coding: utf-8 -*-
from dateutil.parser import parse
from .DatabaseManager import *
from .Exceptions import *

def StockIdToTableName(stockId):
	parts = stockId.lower().split(".")
	return parts[1] +  parts[0]

def IsValidDate(strdate):
    try:
        if "-" in strdate:
            datetime.datetime.strptime(strdate, "%Y-%m-%d")
        else:
            datetime.datetime.strptime(strdate, "%Y%m%d")
        return True
    except:
        return False

#将列表拆分成长度尽可能平均的子列表
def Chunks(arr, m):
	n = int(np.ceil(len(arr) / float(m)))
	return [arr[i:i + n] for i in range(0, len(arr), n)]

def MinuteIdToTimeOfDay(minuteId):
	return time.strftime('%H:%M:%S', time.gmtime(60*minuteId))

def TimestampToMinuteId(timestamp):
	return 60*timestamp.hour+timestamp.minute

def TimestampToSecondsCount(timestamp):
	return 3600*timestamp.hour + 60*timestamp.minute + timestamp.second

def TimeOfDayToMinuteId(todStr):
	todParts = todStr.split(":")
	return 60*int(todParts[0]) + int(todParts[1])

def TimeOfDayToSecondsCount(todStr):
	todParts = todStr.split(":")
	return 3600*int(todParts[0]) + 60*int(todParts[1]) + int(todParts[2])

def TickOfSecond(millisec):
	if millisec < 500:
		return 0
	else:
		return 1

#每秒2次的Tick数据时间戳转化为对齐字段TickLabel
def T2TimeStampToTickLabel(todStr, millisec):
	return 2*TimeOfDayToSecondsCount(todStr) + TickOfSecond(millisec)

def TimeStampToT2TickLabel(todStr, millisec):
	return 2*TimeOfDayToSecondsCount(todStr) + TickOfSecond(millisec)

#N秒一次的Tick数据时间戳转化为对齐字段TickLabel
def TimeStampToNSecTickLabel(timestamp, n):
	return n*int((TimestampToSecondsCount(timestamp)+n-1)/n)

#N秒一次的Tick数据时间字符串转化为对齐字段TickLabel
def TimeOfDayToNSecTickLabel(todStr, n):
	return n*int((TimeOfDayToSecondsCount(todStr)+n-1)/n)

def ProductInfo(productId):
	prodInfoMap = {
		#CFFEX中金所合约
		'IF':{'Multiplier':300},
		'IH':{'Multiplier':300},
		'IC':{'Multiplier':200},
		'T':{'Multiplier':10000},
		'TF':{'Multiplier':10000},
		'IO':{'Multiplier':100},
		#SHFE上期所合约
		'cu':{'Multiplier':5},
		'rb':{'Multiplier':10},
		'zn':{'Multiplier':5},
		'al':{'Multiplier':5},
		'au':{'Multiplier':1000},
		'wr':{'Multiplier':10},
		'fu':{'Multiplier':10},
		'ru':{'Multiplier':10},
		'pb':{'Multiplier':5},
		'ag':{'Multiplier':15},
		'bu':{'Multiplier':10},
		'hc':{'Multiplier':10},
		'ni':{'Multiplier':1},
		'sn':{'Multiplier':1},
		#INE
		'sc':{'Multiplier':1000},
		'nr':{'Multiplier':10},
		#DCE
		'p':{'Multiplier':10},
		'l':{'Multiplier':5},
		'v':{'Multiplier':5},
		'b':{'Multiplier':10},
		'a':{'Multiplier':10},
		'm':{'Multiplier':10},
		'y':{'Multiplier':10},
		'c':{'Multiplier':10},
		'j':{'Multiplier':100},
		'jm':{'Multiplier':60},
		'i':{'Multiplier':100},
		'jd':{'Multiplier':10},
		'bb':{'Multiplier':500},
		'fb':{'Multiplier':500},
		'pp':{'Multiplier':5},
		'cs':{'Multiplier':10},
		#CZCE
		'TA':{'Multiplier':5},
		'SR':{'Multiplier':10},
		'CF':{'Multiplier':5},
		'CY':{'Multiplier':5},
		'WH':{'Multiplier':20},
		'OI':{'Multiplier':10},
		'RI':{'Multiplier':20},
		'FG':{'Multiplier':20},
		'RM':{'Multiplier':10},
		'RS':{'Multiplier':10},
		'JR':{'Multiplier':20},
		'LR':{'Multiplier':20},
		'SF':{'Multiplier':5},
		'SM':{'Multiplier':5},
		'MA':{'Multiplier':10},
		'AP':{'Multiplier':10},
		'ZC':{'Multiplier':100}
	}
	return prodInfoMap[productId]

class MarketDataUtils(object):
	dbManager = MarketDatabaseManager()

#期货数据接口
class FuturesDataUtils(MarketDataUtils):
	def __init__(self, dataSource):
		if not dataSource in ['cffex-l1', 'shfe-l1', 'ine-l1', 'dce-l1', 'czce-l1', 'cffex-l2', 'shfe-l2', 'ine-l2', 'dce-l2', 'czce-l2']:
			print('HiggsBoom FuturesDataUtils: error, unknown data source %s' % dataSource)
			sys.exit(-1)
		self.dataSource = dataSource
		self.exchangeId = dataSource.split('-')[0].upper()
		print('HiggsBoom: initializing futures data engine for %s' % self.dataSource)

	def TickDataFrame(self, instrument, tradingDate):
		try:
			tradingDate = str(parse(tradingDate).date()).replace('-', '')
			instrumentId = instrument
			if '_V' in instrument:
				parts = instrument.split('_V')
				summaryDf = self.DailySummaryFrame(parts[0], tradingDate).sort_values(by=['TotalVolume'], ascending=False)
				if summaryDf.shape[0] == 0:
					raise NoDataError('no instrument data for %s on %s' % (parts[0], tradingDate))
				instrumentId = list(summaryDf['InstrumentId'])[int(parts[1])]
			tableName = '%s_%s' % (self.exchangeId, tradingDate)
			selectSql = "SELECT * FROM %s WHERE instrumentId='%s'" % (tableName, instrumentId)
			tickFrame = pd.DataFrame(MarketDataUtils.dbManager.GetQueryResult(self.dataSource, selectSql), columns=[x[0].upper() + x[1:] for x in MarketDataUtils.dbManager.GetTableColumns(self.dataSource, tableName)])
			tickFrame.rename(columns={'Turnover':'Amount'}, inplace=True)
			return tickFrame
		except:
			raise NoDataError("error, failed to get tick data for %s on %s" % (instrument, tradingDate))

	def MinuteDataFrame(self, instrument, tradingDate):
		try:
			tickFrame = self.TickDataFrame(instrument, tradingDate)
			tickFrame['MinuteID'] = tickFrame['UpdateTime'].apply(TimeOfDayToMinuteId)
			minGroup = tickFrame.groupby('MinuteID')
			minFrame = minGroup.agg({'LastPrice':['first', 'max', 'min', 'last'], 'Volume':['last'], 'Turnover':['last']})
			minFrame.reset_index(inplace=True)
			minFrame.columns = [''.join(col).strip() for col in minFrame.columns.values]
			minFrame.rename(columns={'LastPricefirst':'Open', 'LastPricemax':'High', 'LastPricemin':'Low','LastPricelast':'Close', 'Volumelast':'AccVolume','Turnoverlast':'AccAmt'}, inplace=True)
			minFrame['Volume'] = minFrame['AccVolume'] - minFrame['AccVolume'].shift(1)
			minFrame['Amt'] = minFrame['AccAmt'] - minFrame['AccAmt'].shift(1)
			minFrame['Timestamp'] = minFrame['MinuteID'].apply(MinuteIdToTimeOfDay)
			return minFrame[['Timestamp', 'MinuteID', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amt']]
		except NoDataError as e:
			raise NoDataError("error, failed to get minute data for %s on %s" % (instrument, tradingDate))

	def DailySummaryFrame(self, productId, tradingDate):
		tradingDate = str(parse(tradingDate).date()).replace('-', '')
		selectSql = "SELECT * FROM %s_summary WHERE ProductId='%s' AND ProductType='FUT' AND TradingDate='%s'" % (self.exchangeId, productId, tradingDate)
		return pd.DataFrame(MarketDataUtils.dbManager.GetQueryResult(self.dataSource, selectSql), columns=MarketDataUtils.dbManager.GetTableColumns(self.dataSource, '%s_summary' % self.exchangeId))

	def TradingDays(self, productId):
		selectSql = "SELECT DISTINCT TradingDate FROM %s_summary WHERE ProductId='%s' AND ProductType='FUT'" % (self.exchangeId, productId)
		tdList = [x[0] for x in MarketDataUtils.dbManager.GetQueryResult(self.dataSource, selectSql)]
		tdList.sort()
		return tdList

#A股Tick级数据接口
class AStockTickDataUtils(MarketDataUtils):
	def __init__(self):
		self.dataSource = 'astock-tick'
		print('HiggsBoom: initializing tick data engine for A-stocks')

	def InstrumentList(self, instType, tradingDate):
		selectSql = "SELECT InstrumentId FROM tick_summary WHERE InstrumentType='%s' AND TradingDate='%s'" % (instType, str(parse(tradingDate).date()))
		return [x[0] for x in MarketDataUtils.dbManager.GetQueryResult(self.dataSource, selectSql)]

	def TradingDays(self):
		selectSql = "SELECT DISTINCT TradingDate FROM tick_summary"
		tdList = [str(x[0]) for x in MarketDataUtils.dbManager.GetQueryResult(self.dataSource, selectSql)]
		tdList.sort()
		return tdList

	def TickDataFrame(self, instrument, tradingDate):
		tableName = StockIdToTableName(instrument)
		selectSql = "SELECT * FROM %s WHERE DATE(Timestamp)='%s'" % (tableName, str(parse(tradingDate).date()))
		tickFrame = pd.DataFrame(MarketDataUtils.dbManager.GetQueryResult(self.dataSource, selectSql), columns=[x[0].upper() + x[1:] for x in MarketDataUtils.dbManager.GetTableColumns(self.dataSource, tableName)])
		if tickFrame.shape[0] == 0:
			raise NoDataError("error, failed to get tick data for %s on %s" % (instrument, tradingDate))
		return tickFrame

	def MinuteDataFrame(self, instrument, tradingDate):
		try:
			tickFrame = self.TickDataFrame(instrument, tradingDate)
			tickFrame['MinuteID'] = tickFrame['Timestamp'].apply(TimestampToMinuteId)
			minGroup = tickFrame.groupby('MinuteID')
			minFrame = minGroup.agg({'LastPrice':['first', 'max', 'min', 'last'], 'Volume':['last'], 'Amount':['last']})
			minFrame.reset_index(inplace=True)
			minFrame.columns = [''.join(col).strip() for col in minFrame.columns.values]
			minFrame.rename(columns={'LastPricefirst':'Open', 'LastPricemax':'High', 'LastPricemin':'Low','LastPricelast':'Close', 'Volumelast':'AccVolume','Amountlast':'AccAmt'}, inplace=True)
			minFrame['Volume'] = minFrame['AccVolume'] - minFrame['AccVolume'].shift(1)
			minFrame['Amt'] = minFrame['AccAmt'] - minFrame['AccAmt'].shift(1)
			minFrame['Timestamp'] = minFrame['MinuteID'].apply(MinuteIdToTimeOfDay)
			return minFrame[['Timestamp', 'MinuteID', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amt']]
		except NoDataError as e:
			raise NoDataError("error, failed to get minute data for %s on %s" % (instrument, tradingDate))
