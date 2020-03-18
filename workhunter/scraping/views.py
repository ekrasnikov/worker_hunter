from django.shortcuts import render
from .utils import Parser
from .models import Speciality, City, Vacancy, Url, Site


def index(request):
    return render(request, 'base.html')


def home(request):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'accept': '*/*',
    }
    city = City.objects.get(name='Томск')
    speciality = Speciality.objects.get(name='Python')
    url_qs = Url.objects.filter(city=city, speciality=speciality)
    site = Site.objects.all()
    url_hh = url_qs.get(site=site.get(name='hh.ru')).url_address
    parser = Parser(headers)
    parser.get_urls(url_hh)
    jobs = parser.parse()
    vacancy = Vacancy.objects.filter(city=city.id, speciality=speciality.id).values('url')
    url_list = [url['url'] for url in vacancy]
    for job in jobs:
        if job['link'] not in url_list:
            v = Vacancy(city=city, speciality=speciality, url=job['link'], title=job['title'],
                        description=job['context'], company=job['company'])
            v.save()

    return render(request, 'scrapping/list.html', {'jobs': jobs})
