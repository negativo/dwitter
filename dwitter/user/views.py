from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from dwitter.models import Dweet
from django.contrib.auth.models import User

def user_feed(request, url_username, page_nr):
  user = get_object_or_404(User, username=url_username) 
  page = int(page_nr)
  dweets_per_page = 5
  first = (page - 1) * dweets_per_page
  last = page * dweets_per_page
  dweet_count = Dweet.objects.count()

  if(first < 0 or first >= dweet_count):
    raise Http404("No such page")
  if(last >= dweet_count ):
    last = dweet_count - 1;
  
  dweet_list = Dweet.objects.filter(author=user).order_by('-posted')[:5]
  context = {'dweet_list': dweet_list
            ,'header_title': url_username + ' feed'
            ,'page_nr': page
            ,'next_url': reverse('user_feed_page', kwargs={
                                        'url_username': url_username,
                                        'page_nr': page + 1})
            ,'prev_url': reverse('user_feed_page', kwargs={
                                        'url_username': url_username,
                                        'page_nr': page - 1})
            }
  return render(request, 'feed/feed.html', context );
