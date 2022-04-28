from PyQt5.QtChart import QChart, QChartView, QLineSeries, QPieSeries, QBarSet, \
	QBarSeries, QBarCategoryAxis
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from .analytic import Analytics
import time
import datetime

class AnalyticsView:
	def __init__(self, this):
		this.ui.stackedWidget.setCurrentWidget(this.ui.page_12)
		self.con = Analytics()
		self.barChart(this)
		self.circleChart(this)
		this.ui.label_10.setText(str(self.con.totalEarns()))
		this.ui.label_12.setText(str(self.con.allSoldProductsLength()))
		date = datetime.datetime.today().date()
		this.ui.today_earns.setText(str(self.con.earnPerDay(date)))

	def barChart(self, this):
		#create barseries
		set0 = QBarSet("Parwiz")
	


		#insert data to the barseries
		data = self.con.sevenDaysEarns()
		
		set0 << data[0] << data[1] <<data[2] << data[3] << data[4] << data[5] << data[6]
		
		
		#we want to create percent bar series
		series = QBarSeries()
		series.append(set0)
		

		#create chart and add the series in the chart
		chart = QChart()
		chart.addSeries(series)
		chart.setTitle("ارباح هذا الاسبوع")
		chart.setAnimationOptions(QChart.SeriesAnimations)
		chart.setTheme(QChart.ChartThemeDark)


		#create axis for the chart
		categories = self.con.daysOfTheWeek()

		axis = QBarCategoryAxis()
		axis.append(categories)
		chart.createDefaultAxes()
		chart.setAxisX(axis, series)

		#create chartview and add the chart in the chartview
		chartview = QChartView(chart)
		if this.ui.verticalLayout_4.count() == 0:
			this.ui.verticalLayout_4.addWidget(chartview)

		




	def circleChart(self, this):
		series  = QPieSeries()
		products = self.con.mostSoldProducts()
		table = this.ui.productsName

		table.setRowCount(len(products))

		for row, product in enumerate(products):
			for i, val in product.items():
				#append some data to the series 
				series.append(i, val)
				table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i)))

		#slice
		#my_slice = series.slices()[3]
		"""my_slice.setExploded(True)
		my_slice.setLabelVisible(True)
		my_slice.setPen(QPen(Qt.green, 4))
		my_slice.setBrush(Qt.green)"""



		#create QChart object
		chart = QChart()
		chart.addSeries(series)
		chart.setAnimationOptions(QChart.SeriesAnimations)
		chart.setTitle("السلع الاكثر مبيعا")
		chart.setTheme(QChart.ChartThemeDark)

		# create QChartView object and add chart in thier 
		chartview = QChartView(chart)
		if this.ui.horizontalLayout_13.count() == 1:
			this.ui.horizontalLayout_13.addWidget(chartview)

