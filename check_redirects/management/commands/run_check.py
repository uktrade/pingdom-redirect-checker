from django.core.management.base import BaseCommand, CommandError

import subprocess
import time, os, urllib.request

from check_redirects.models import Urllist, Responsetime

class Command(BaseCommand):
    def handle(self, *args, **options):

        #import pdb; pdb.set_trace()
        t0 = time.time()
        print('Link check now running ...')
        #current_item_pos = 0
        for current_url in Urllist.objects.filter(enable=True):
            print("checking: ", current_url.site_url, " target url: ", current_url.target_url, " - Supported by: ", current_url.team)
            #current_item_pos += 1
            response_url = str(self.get_url_nofollow(current_url.site_url))
            if response_url == current_url.target_url:
                Urllist.objects.filter(id=current_url.id).update(broken_redirect=False, actual_target=None)
            else:
                # import pdb; pdb.set_trace()
                print ("Actual url: ", response_url)
                print ("Error redirect broken")
                Urllist.objects.filter(id=current_url.id).update(broken_redirect=True, actual_target=response_url)
        t1 = time.time()
        total_time = (t1 - t0) * 1000
        Responsetime.objects.update_or_create(id=1, defaults={'response_time': total_time})

    def get_url_nofollow(self, url):

        response = urllib.request.urlopen(url)
        if response.url[-1] == '/':
            response.url = response.url[:-1]


        return response.url
