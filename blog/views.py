#from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from models import Category, Post, Tag
from forms import ContactForm

# Create your views here.

def index(request, selected_page=1):
    # get the blog posts that are published
    posts = Post.objects.filter(published=True).all()
    pages = Paginator(posts, 5)
    plist = Post.objects.filter(published=True).all()

    try:
        returned_page = pages.page(selected_page)
    except EmptyPage:
        returned_page = pages.page(pages.num_pages)
    # return the rendered template
    return render(request, "blog/index.html",
                  {"posts": returned_page.object_list, "page": returned_page, "plist": plist })


class CategoryListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Post.objects.filter(category=category)
        except Category.DoesNotExist:
            return Post.objects.none()


class TagListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Post.objects.none()

#########################
##### SPECIFIC PAGES ####
#########################

@login_required(login_url='/lostroses.html')

def about(request):
    p_about = Post.objects.filter(category__name='About',published=True).all()[:3]
    p_her = Post.objects.filter(tags__name='herstory',published=True).all()[:3]
    p_resume = Post.objects.filter(tags__name='resume',published=True).all()[:3]
    p_sopriv = Post.objects.filter(tags__name='SoPriv',published=True).all()[:3]
    p_read = Post.objects.filter(tags__name='read',published=True).all()[:10]
    p_r_list = Post.objects.filter(tags__name='read',published=True).all()[10:20]
    p_adv = Post.objects.filter(tags__name='adv',published=True).all()[:3]
    p_blog = Post.objects.filter(tags__name='blog',published=True).all()[:3]

    return render(request, '../templates/blog/about/about.html', {'p_about': p_about, 'p_her': p_her, 'p_resume': p_resume,
                                               'p_sopriv': p_sopriv, 'p_read': p_read, 'p_adv': p_adv,
                                               'p_blog': p_blog, 'p_read_list': p_r_list})


def school(request):
    p_mind = Post.objects.filter(category__name='Mind',published=True).all()[:3]
    p_econ = Post.objects.filter(tags__name='econ',published=True).all()[:3]
    p_stat = Post.objects.filter(tags__name='stats',published=True).all()[:3]
    p_comm = Post.objects.filter(tags__name='comm',published=True).all()[:3]
    p_loan = Post.objects.filter(tags__name='loans',published=True).all()[:3]

    return render(request, '../templates/blog/school/mind.html',
                  {'p_mind': p_mind, 'p_econ': p_econ, 'p_stat': p_stat, 'p_comm': p_comm, 'p_loan': p_loan})


def music(request):
    p_soul = Post.objects.filter(category__name='Soul',published=True).all()[:3]
    p_poet = Post.objects.filter(tags__name='poetree',published=True).all()[:3]
    p_music = Post.objects.filter(tags__name='music',published=True).all()[:3]
    p_vid = Post.objects.filter(tags__name='video',published=True).all()[:3]

    return render(request, '../templates/blog/music/soul.html', {'p_soul': p_soul, 'p_poet': p_poet, 'p_music': p_music, 'p_vid': p_vid})


def tech(request):
    p_body = Post.objects.filter(category__name='Body',published=True).all()[:3]
    p_comp = Post.objects.filter(tags__name='CompSci',published=True).all()[:3]
    p_gard = Post.objects.filter(tags__name='garden',published=True).all()[:3]
    p_misc = Post.objects.filter(tags__name='misc',published=True).all()[:3]

    return render(request, '../templates/blog/tech/body.html', {'p_body': p_body, 'p_comp': p_comp, 'p_gard': p_gard, 'p_misc': p_misc})


def contact(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message_1 = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            message = message_1 + '\n' + sender

            recipients = ['canin.apple@gmail.com']

            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)

        return HttpResponseRedirect('http://www.culture-clap.com/thankyou.html')

    else:

        form = ContactForm()

    return render(request, 'contact.html', {'form': form, })


def caninx(request):
    p_blog = Post.objects.filter(category__name='Blog').all()[:3]
    return render(request, '../templates/blog/about/caninx.html', {'p_blog': p_blog,})

def herstory(request):
    p_her = Post.objects.filter(tags__name='herstory').all()[:3]
    return render(request, '../templates/blog/about/herstory.html', {'p_her': p_her,})


def effort(request):
    p_yt = Post.objects.filter(tags__name='ytReads').all()
    return render(request, 'an-effort-to-educate-white-people.html', {'p_yt': p_yt})
