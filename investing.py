import requests
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

class CrawlerInvesting:
	def __init__(self):
		self.header = self.getHeaderInvesting()

		nomeCriptoMoeda = str(sys.argv[-1])
		if '.py' in nomeCriptoMoeda:
			self.sendLogToSystem('ERROR', 'Syntax de execução incorreta. Correta : python investing.py "Nome Criptomoeda"')
			quit()

        self.sendLogToSystem('DEBUG', 'Start Crawler')
		self.getCritoMoeda(nomeCriptoMoeda)
        self.sendLogToSystem('DEBUG', 'Finish Crawler')

	def sendLogToSystem(self, type_message, message):
		print (f'[ {type_message} ] {message}')

	def getCritoMoeda(self, nomeCriptoMoeda):
		nomeCriptoMoedaURL = nomeCriptoMoeda.replace(' ','-')

		urlCriptoMoeda = 'https://br.investing.com/crypto/{}'.format(nomeCriptoMoedaURL)

		requisicaoCriptoMoeda = requests.get(urlCriptoMoeda, headers=self.header)
		if requisicaoCriptoMoeda.status_code == 200:
			soupCriptoMoeda = BeautifulSoup(requisicaoCriptoMoeda.content, 'html.parser')

			valorCriptoDolar = self.tratarStringToDouble(soupCriptoMoeda.select_one("span#last_last"))
			valorCriptoReal = valorCriptoDolar * self.getValueDolar()

			dictCriptoMoeda = {
				'nome_criptomoeda' : nomeCriptoMoeda,
				'url_criptoMoeda' : urlCriptoMoeda,
				'valor_dolar' : valorCriptoDolar,
				'valor_real' : valorCriptoReal,
				'valor_variacao' : self.tratarStringToDouble( soupCriptoMoeda.select_one('div.top.bold.inlineblock span:nth-of-type(2)') ),
				'porcentagem_variacao' : str(self.tratarStringToDouble( soupCriptoMoeda.select_one('div.top.bold.inlineblock span:nth-of-type(4)') ) )+'%',
				'data_hora_consulta' : datetime.now().strftime('%Y-%m-%d %H:%M:%S%z')
			}

			self.sendLogToSystem('DEBUG', 'Cotacão Coletada - {} | {}'.format(nomeCriptoMoeda,dictCriptoMoeda['data_hora_consulta']))

			self.setInfoInCSV(dictCriptoMoeda)
		else:
			self.sendLogToSystem('ERROR', 'Criptomoeda invalida')

	def tratarStringToDouble(self, string):
		if string != None:
			return float( str(string.text).replace('.','').replace(',','.').replace('%','').strip() )
		else:
			return None

	def setInfoInCSV(self, dictData):
		titles, data = self.convertDictInCSV(dictData)

		if 'cotacoes.csv' in os.listdir('./'):
			fileCSV = open('cotacoes.csv', 'a+', encoding='utf-8')
			fileCSV.write(data)
		else:
			fileCSV = open('cotacoes.csv', 'a+', encoding='utf-8')
			fileCSV.write(titles + data)

		fileCSV.close()

	def convertDictInCSV(self, dictData):
		arrayTitles = []
		arrayData = []

		for key in dictData:
			arrayTitles.append(str(key))
			arrayData.append(str(dictData[key]))

		stringTitle = str(';'.join(arrayTitles)) + '\n'
		stringData = str(';'.join(arrayData)) + '\n'

		return stringTitle, stringData

	def getValueDolar(self):
		urlDolar = 'https://br.investing.com/currencies/usd-brl'

		requisicaoDolar = requests.get(urlDolar, headers=self.header)
		soupDolar = BeautifulSoup(requisicaoDolar.content, 'html.parser')

		return self.tratarStringToDouble(soupDolar.select_one("span#last_last"))

	def getHeaderInvesting(self):
		return {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Cookie': 'logglytrackingsession=fea7af4c-fb3a-4151-8d03-d25ebb8fe2d2; adBlockerNewUserDomains=1599509579; _ga=GA1.2.1146182430.1599509582; G_ENABLED_IDPS=google; _fbp=fb.1.1599509582299.1979057458; r_p_s_n=1; OptanonAlertBoxClosed=2020-09-07T20:13:05.041Z; eupubconsent-v2=CO5YcsCO5YcsCAcABBENA2CsAP_AAH_AAChQGetf_X_fb2vj-_5999t0eY1f9_63v-wzjgeNs-8NyZ_X_L4Xr2MyvB36pq4KuR4Eu3LBAQdlHOHcTQmQwIkVqTLsbk2Mq7NKJ7LEilMbM2dYGH9vn8XTuZCY70_sf__z_3-_-___67b-IGeEEmGpfAQJCWMBJNmlUKIEIVxIVAOACihGFo0sNCRwU7K4CPUECABAagIwIgQYgoxZBAAAAAElEQAkBwIBEARAIAAQArQEIACJAEFgBIGAQACgGhYARRBKBIQZHBUcogQFSLRQTzRgSQAA.YAAAAAAAAAAA; usprivacy=1YNN; OB-USER-TOKEN=1edbdc51-2a2e-438d-91c6-80c2fe70bf4f; __gads=ID=f487794cef765e22:T=1601035636:S=ALNI_Mb73kE1wvhD7iqJIagkcaMwh4KSPw; SKpbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMOf4y1wGGNgcVrNQMsM5kL278M-lGA3fHc7uoCEA%22%2C%22ID5ID_CREATED_AT%22%3A%222020-08-10T12%3A55%3A31.292Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A3%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A7%3A%221024807%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A23%3A%22Bitcoin+Real+Brasileiro%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fcrypto%2Fbitcoin%2Fbtc-brl%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A6%3A%22945629%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A24%3A%22Bitcoin+D%C3%B3lar+Americano%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A23%3A%22%2Fcrypto%2Fbitcoin%2Fbtc-usd%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%222103%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A32%3A%22D%C3%B3lar+Americano+Real+Brasileiro%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A19%3A%22%2Fcurrencies%2Fusd-brl%22%3B%7D%7D%7D%7D; PHPSESSID=bvspv0u4aadmc73v9moqemqja0; prebid_page=0; prebid_session=1; StickySession=id.58332903543.653.br.investing.com; geoC=BR; gtmFired=OK; _gid=GA1.2.412834279.1601225144; SKpbjs-unifiedid=%7B%22TDID%22%3A%226e9fa0ba-4cfe-4f2c-9472-3c6d2165f765%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222020-08-27T16%3A45%3A48%22%7D; SKpbjs-unifiedid_last=Sun%2C%2027%20Sep%202020%2016%3A45%3A47%20GMT; SKpbjs-id5id_last=Sun%2C%2027%20Sep%202020%2016%3A45%3A48%20GMT; GED_PLAYLIST_ACTIVITY=W3sidSI6InJHRkUiLCJ0c2wiOjE2MDEyMjUxNTAsIm52IjoxLCJ1cHQiOjE2MDEyMjUxNTAsImx0IjoxNjAxMjI1MTUwfV0.; OptanonConsent=isIABGlobal=false&datestamp=Sun+Sep+27+2020+13%3A45%3A50+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.5.0&consentId=f1055393-0138-4b9d-b9da-a9cd98e421e0&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&hosts=H107%3A1%2CH20%3A1%2CH128%3A1%2CH58%3A1%2CH75%3A1%2CH81%3A1%2CH106%3A1%2CH108%3A1%2CH109%3A1%2CH6%3A1%2CH8%3A1%2CH9%3A1%2CH10%3A1%2CH14%3A1%2CH15%3A1%2CH16%3A1%2CH112%3A1%2CH17%3A1%2CH19%3A1%2CH21%3A1%2CH23%3A1%2CH25%3A1%2CH26%3A1%2CH93%3A1%2CH31%3A1%2CH32%3A1%2CH94%3A1%2CH34%3A1%2CH35%3A1%2CH37%3A1%2CH123%3A1%2CH95%3A1%2CH39%3A1%2CH40%3A1%2CH41%3A1%2CH43%3A1%2CH44%3A1%2CH124%3A1%2CH125%3A1%2CH46%3A1%2CH126%3A1%2CH47%3A1%2CH127%3A1%2CH48%3A1%2CH51%3A1%2CH52%3A1%2CH133%3A1%2CH134%3A1%2CH53%3A1%2CH54%3A1%2CH57%3A1%2CH135%3A1%2CH61%3A1%2CH62%3A1%2CH64%3A1%2CH65%3A1%2CH66%3A1%2CH69%3A1%2CH70%3A1%2CH71%3A1%2CH72%3A1%2CH74%3A1%2CH101%3A1%2CH76%3A1%2CH141%3A1%2CH78%3A1%2CH79%3A1%2CH142%3A1%2CH85%3A1%2CH87%3A1%2CH88%3A1%2CH90%3A1&geolocation=BR%3BSP&AwaitingReconsent=false; nyxDorf=Y2cyZmA%2FZiQ0a21nMH05OmIwYzxmfzo7',
			'Host': 'br.investing.com',
			'Referer': 'https://br.investing.com/crypto/bitcoin/btc-brl',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-User': '?1',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
		}

CrawlerInvesting()
