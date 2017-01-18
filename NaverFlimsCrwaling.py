#-*- coding:utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import time
import codecs
import requests

# quote GyuHyun's
class Movie:
	def __init__(self, title, makeYear, nation, openYD, genre, form, grade):
		self.title = title.encode('utf-8')
		self.makeYear = makeYear.encode('utf-8')
		self.nation = nation.encode('utf-8')
		self.openYD = openYD.encode('utf-8')
		self.genre = genre.encode('utf-8')
		self.form = form.encode('utf-8')
		self.grade = grade.encode('utf-8')

	def __setitem__(self, key, value):
		self.data[key] = value

	def getMembers(self):
		return '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t'.format(self.title.encode('utf-8'), self.makeYear.encode('utf-8'), self.nation.encode('utf-8'), self.openYD.encode('utf-8'), self.genre.encode('utf-8'), self.form.encode('utf-8'), self.grade.encode('utf-8'))
		return [self.title, self.makeYear, self.nation, self.openYD, self.genre, self.form, self.grade]

	def __unicode__(self):
		return u'title: {0}\nmakeYear: {1}\nnation: {2}\nopenYD: {3}\ngenre: {4}\nform: {5}\ngrade: {6}\n'.format(self.title, self.makeYear, self.nation, self.openYD, self.genre, self.grade)

	def __str__(self):
		return unicode(self).encode('utf-8')

def get_html(url, page):
	if page==1:
		html = urllib.urlopen(url)
	else:
		html = urllib.urlopen(url + "&page=" + str(page))
	return html

def get_film_list():
	soup = BeautifulSoup(html, 'lxml')
	content = soup.find('ul', {'class':'directory_list'}).find_all("a")
	content.append("PageEnd")
	return content

def check_type(s):
	if s.find("code") != -1:
		return 'title'
	elif s.find("nation") != -1:
		return 'nation'
	elif s.find("openYD") != -1:
		return 'openYD'
	elif s.find("genre") != -1:
		return 'genre'
	elif s.find('form') != -1:
		return 'form'
	elif s.find('grade') != -1:
		return 'grade'
	elif s.find("year") != -1:
		return 'makeYear'
	else:
		print 'Type Check Error\n'
		return 'error'

def input_data(tmp, type, data):
	data = data.replace(" ", "")
	if type == 'title':
		tmp.title = data
	elif type =="nation":
		tmp.nation = data
	elif type == "openYD":
		tmp.openYD = data
	elif type == "genre":
		tmp.genre = data
	elif type == "form":
		tmp.form = data
	elif type == 'grade':
		tmp.grade = data
	elif type == "makeYear":
		tmp.makeYear = data
	else:
		print 'Data Setting Error\n'
	return tmp

tlist = ["1940", "1950", "1960", "1970" ,"1980", "1990", "1991", "1992", "1993" ,"1994", "1995", "1996", "1997", "1998", "1999",
		 "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
		 "2014", "2015", "2016", "2017", "2018", "2019"]

for year in tlist:

	MovieList = []
	TitleList = []
	MakeYearList = []
	NationList = []
	OpenYDList = []
	GenreList = []
	FormList = []
	GradeList = []

	time.sleep(1)

	print 'Year {0}'.format(year)
	page = 1

	BasicUrl = 'http://movie.naver.com/movie/sdb/browsing/bmovie.nhn?year=' + year
	html = get_html(BasicUrl, page)

	prevList = []
	while True:
		#time.sleep(1)
		List = get_film_list()

		if(List == prevList):
			break

		cnt = 1
		tmp = Movie("NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL")
		print 'Page {0} \n'.format(page)
		for data in List:
			#print 'Data {0}--------------------------------------\n'.format(cnt)
			if(data == "PageEnd"):
				page+=1
				html = get_html(BasicUrl, page)
				break

			if(check_type(data['href'].encode('utf-8')) == 'title'):
				if(tmp.title != data['href'].encode('utf-8')):
					MovieList.append(tmp)
					TitleList.append(tmp.title)
					MakeYearList.append(tmp.makeYear)
					NationList.append(tmp.nation)
					OpenYDList.append(tmp.openYD)
					GenreList.append(tmp.genre)
					FormList.append(tmp.form)
					GradeList.append(tmp.grade)
					tmp = Movie("NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL")

			tmp = input_data(tmp, check_type(data['href'].encode('utf-8')), data.text)
			#print tmp.title
			#print data['href'].encode('utf-8')
			#print '------------------------------------------\n'
			cnt += 1
		#print '------------------------------------------\n'
		prevList = List

	fileName = "Films_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in MovieList:
			fp.write(data.getMembers())

	fileName = "Titles_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in TitleList:
			if(data == "NULL"):
				continue
			fp.write('{0}\t'.format(data.encode('utf-8')))

	fileName = "MakeYears_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in MakeYearList:
			if(data == "NULL"):
				continue
			fp.write('{0}\t'.format(data.encode('utf-8')))

	fileName = "Nations_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in NationList:
			if(data == "NULL"):
				continue
			fp.write('{0}\t'.format(data.encode('utf-8')))

	fileName = "Genres_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in GenreList:
			if(data == "NULL"):
				continue
			fp.write('{0}\t'.format(data.encode('utf-8')))

	fileName = "Forms_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in FormList:
			if(data == "NULL"):
				continue
			fp.write('{0}\t'.format(data.encode('utf-8')))

	fileName = "Grades_" + str(year) + ".txt"
	with open(fileName, "a") as fp:
		for data in GradeList:
			if(data == "NULL"):
				continue
			fp.write('{0}\t'.format(data.encode('utf-8')))
