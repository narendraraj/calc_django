import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tango.settings')


import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [
        {'title': 'Official Python tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': 500},

        {'title': 'How to think like a computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': 450},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': 400},
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'http://docs.djangoproject.com/en/3.0/',
         'views': 350},
        {'title': 'Django Rocks',
         'url': 'https://www.djangorocks.com/',
         'views': 300},
        {'title': 'Tango with Django',
         'url': 'https://www.tangowithdjango.com/',
         'views': 250},
    ]

    other_pages = [
        {'title': 'Bottle',
         'url': 'https://bottlepy.org/docs/dev/',
         'views': 200},
        {'title': 'Flask',
         'url': 'https://flask.palletsprojects.com/en/1.1.x/',
         'views': 150},
        # {'views': 40}
    ]

    cats = {'Python': {'pages': python_pages, 'views': 200, 'likes': 100},
            'Django': {'pages': django_pages, 'views': 100, 'likes': 50},
            'Other Frameworks': {'pages': other_pages, 'views': 50, 'likes': 25}}

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        print(cat, cat_data)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],p['views'] )
        print('#################\n')
        print(p)



    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f' - {c} : {p}')


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title, views=views)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c


if __name__ == '__main__':
    print('starting Rango population script')
    populate()
