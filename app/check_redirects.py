import threading, os, time, urllib2, json


class RunCheck(object):
	def __init__(self):

		self.interval = int(os.environ.get('CHECK_INTERVAL'))

		print "This check will run every %ds" % self.interval
		self.create_url_status()

		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True  # Daemonize thread
		thread.start()

	def create_url_status(self):
		#copy url list to json format list

		first = True
		with open('url_status.json','w') as out:
			out.write ('{}'.format("{"))
			url_contents = [url_content.rstrip('\n') for url_content in open ('url_list')]

			for current_url in url_contents:
				if not current_url.startswith("#"):
					mylist = current_url.split(',')
					if first:
						out.write ('{}{}{}{}{}'.format("\"", mylist[0], "\":[\"", mylist[1], "\",\"OK\"]"))

						first = False
					else:
						out.write ('{}{}{}{}{}'.format(",\"", mylist[0], "\":[\"", mylist[1], "\",\"OK\"]"))

			out.write ('{}'.format("}"))

	def get_url_nofollow(self, url):
		try:
			response = urllib2.urlopen(url)
			#code = response.getcode()
			response_url = response.geturl()

			return response_url
		except urllib2.HTTPError as e:
			return e.code
		except:
			return 0

	def run(self):
		""" Method that runs forever """
		check_log_url = "https://pingdom-redirect-checker.ukti.io/logs.html"

		while True:
			with open('url_status.json') as json_file:
				d = json.load(json_file)
			xml_out_1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			xml_out_2 = "<pingdom_http_custom_check>"
			xml_out_5 = "</pingdom_http_custom_check>"

			#url_contents = [url_content.rstrip('\n') for url_content in open('url_list')]
			timestr = time.strftime(" ...Actually Returned @ Time Of Failure: %d/%m/%Y-%H:%M:%S")
			redirect_status = True
			t0 = time.time()

			with open('app/templates/logs.html', 'w') as out:
				out.write('{}\n{}\n{}\n{}\n'.format('<html>', '<body>', '<h1>Redirect check - logs</h1>', '<p>'))

			for current_url, status in d.iteritems():

					response_url = str(self.get_url_nofollow(current_url))
					if response_url[-1] == '/':
						response_url = response_url[:-1]
					print "Checking URL: %s\tRespose: %s" % (current_url, response_url)

					# with open('app/templates/logs.html', 'a') as out:
					# 	out.write('{}\t\t{}{}{}\n'.format(current_url, ' -- Response: ', response_url, '<br/>'))

					# if response_code != 200:
					# 	redirect_status = False
					if response_url != status[0]:
						redirect_status = False
						#status[1] = response_url + timestr

						with open('app/templates/logs.html', 'a') as out:
							out.write('{}{}{}{}{}{}{}{}{}\n'.format('Source: ',current_url ,'    Expected result: ',status[0] ,'    Actual result: ',response_url ,' -- Result: ', 'BAD', '<br/>'))

						if (status[1] == 'OK'):
							status[1] = response_url + timestr

					if response_url == status[0]:
						status[1] = "OK"
						with open('app/templates/logs.html', 'a') as out:
							out.write('{}{}{}{}{}{}{}{}{}\n'.format('Source: ',current_url ,'    Expected result: ',status[0] ,'    Actual result: ',response_url ,' -- Result: ', 'GOOD', '<br/>'))

			with open('url_status.json', 'w') as json_file:
				json.dump(d, json_file)

			with open('app/templates/logs.html', 'a') as out:
				if redirect_status == True:
					out.write('{}\n{}\n{}\n{}\n'.format('--  All Sites Checked -- OK --', '</p>', '</body>', '</html>'))
					print "--  All Sites Checked -- OK --"
				else:
					out.write('{}\n{}\n{}\n{}\n'.format('--  All Sites Checked -- Bad Redirects Detected --', '</p>', '</body>', '</html>'))
					print "--  All Sites Checked -- Bad Redirects Detected --"



			t1 = time.time()
			total_time = (t1 - t0) * 1000

			if redirect_status == False:
				with open('app/templates/check.xml', 'w') as out:
					out.write('{}\n{}\n{}\n'.format(xml_out_1, xml_out_2, "<status>"))
					with open('url_status.json') as json_file:
						d = json.load(json_file)
						# for key, value in xml_list.items():
						for key, value in d.iteritems():
							#print (key)
							#print (value)

							if (value[1] != 'OK'):
								out.write('{}\n{}{}{}\n'.format("The following URLs redirect is incorrect", "<", key[7:].replace('/','-'), ">"))
								out.write('{}\n'.format("Expected ..."))
								for x in value:
									out.write('{}\n'.format(x))
								#out.write('{}\n'.format("...Actually Returned"))
								out.write('{}{}{}\n'.format("</", key[7:].replace('/','-'), ">"))

					out.write('{}\n'.format("</status>"))
					# xml_out_3 = "<status XML-LINK=\"LINK\" HREF=\"https://pingdom-redirect-checker.ukti.io/logs.html\">Logs Link</status>"
					xml_out_4 = "<response_time>%.2f</response_time>" % total_time
					out.write('{}\n{}\n'.format(xml_out_4, xml_out_5))

			if redirect_status == True:
				with open('app/templates/check.xml', 'w') as out:
					xml_out_3 = "<status>OK</status>"
					xml_out_4 = "<response_time>%.2f</response_time>" % total_time
					out.write('{}\n{}\n{}\n{}\n{}\n'.format(xml_out_1, xml_out_2, xml_out_3, xml_out_4, xml_out_5))
			time.sleep(self.interval)
