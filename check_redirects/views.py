from django.shortcuts import render

from .models import Urllist, Responsetime

# Create your views here.

def url_search_results(request):
	# broken_links = Brokenlink.objects.all()
	response_time = Responsetime.objects.get(id=1).response_time
	url_list = Urllist.objects.all()
	is_ok = True
	for x in url_list:
		if x.enable and x.broken_redirect:
			is_ok = False

	# context['status'] = not any(x.temp_url.enable for x in Brokenlink.objects.all())
	context = {'url_list': url_list, 'response_time': response_time, 'is_ok': is_ok}

	return render(request, 'check.xml', context)

def logs(request):
	#broken_links = Brokenlink.objects.all()
	url_list = Urllist.objects.all()
	context = {'url_list': url_list}

	return render(request, 'logs.html', context)

# def scan(request):
#     return render(request, 'scan-base.html', {})
