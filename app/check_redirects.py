import threading, subprocess, os, time, sys, urllib2
from subprocess import call

class run_check(object):

	def __init__(self):

		self.interval = int(os.environ.get('CHECK_INTERVAL'))
		
		print "This check will run every %ds"  % self.interval
		
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start()                  

	def get_url_nofollow(self, url):
	    try:
	        response = urllib2.urlopen(url)
	        code = response.getcode()
	        return code
	    except urllib2.HTTPError as e:
	        return e.code
	    except:
	        return 0

	def run(self):
		""" Method that runs forever """
		check_log_url = "https://pingdom-link-checker.ukti.io/redirectlogs.html"

		while True:
		
			xml_out_1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
			xml_out_2 = "<pingdom_http_custom_check>"
			xml_out_5 = "</pingdom_http_custom_check>"


			url_contents = [url_content.rstrip('\n') for url_content in open ('url_list')]
			
			redirect_status = True
			t0 = time.time()

			with open('app/templates/redirectlogs.html','w') as out:
				out.write ('{}\n{}\n{}\n{}\n'.format('<html>','<body>','<h1>Redirect check - logs</h1>','<p>'))


			for current_url in url_contents:
		
				response_code = self.get_url_nofollow(current_url)		
				print "checking URL: %s\trespose: %d" % (current_url, response_code)

					#print "%s" % current_url
				with open('app/templates/redirectlogs.html','a') as out:
					out.write ('{}\t\t{}{}{}\n'.format(current_url,' -- Response: ',response_code,'<br/>'))
					
				
				if (response_code != 200 ):
					redirect_status = False


			with open('app/templates/redirectlogs.html','a') as out:
				out.write ('{}\n{}\n{}\n{}\n'.format('--  All Sites Checked --','</p>','</body>','</html>'))


			t1 = time.time()
			total_time = (t1-t0)*1000

			if ( redirect_status == False ):
				with open('app/templates/check.xml','w') as out:
					xml_out_3 = "<status>Redirect Falied check logs - " + check_log_url + "</status>"
					xml_out_4 = "<response_time>%.2f</response_time>" % total_time
					out.write('{}\n{}\n{}\n{}\n{}\n'.format(xml_out_1,xml_out_2,xml_out_3,xml_out_4,xml_out_5))

			if ( redirect_status == True ):
				with open('app/templates/check.xml','w') as out:
					xml_out_3 = "<status>OK</status>"
					xml_out_4 = "<response_time>%.2f</response_time>" % total_time
					out.write('{}\n{}\n{}\n{}\n{}\n'.format(xml_out_1,xml_out_2,xml_out_3,xml_out_4,xml_out_5))
			time.sleep(self.interval)

