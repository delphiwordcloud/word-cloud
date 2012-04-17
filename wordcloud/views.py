__author__ = 'michael odland'

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from wordcloud.forms import *
from wordcloud.models import *
import linguist


#todo: laura wants to be able to choose the label and group words together graphically
#todo: group words in a box: all the terms in the box would have the ability to label. you see the label
#todo: need jquery handlers to interact more, also html5
#

def tag_page(request, tag_name):
    c = {}
    c.update(csrf(request))
    tag = get_object_or_404(Tag, name = tag_name )
    corpora = tag.corpora.order_by('-id')
    variables = RequestContext( request, {
        'corpora'  : corpora,
        'tag_name' : tag_name,
        'show_tags': True,
        'show_user': True
    })
    return render_to_response('tag_page.html', c, variables)


def profile_settings_page(request):
    c = {}
    c.update(csrf(request))


def profile_page(request):
    c = {}
    c.update(csrf(request))


@login_required
def corpus_save(request):  # todo: successful save page is needed, corpus_list.html must be fixed to display the saved corpora
    c = {}
    c.update(csrf(request))
    ajax = 'ajax' in request.GET
    if request.method == 'POST':
        form = CorpusSaveForm(request.POST, request.FILES)
        if form.is_valid():
            corpus = _corpus_save(form, request)
            if ajax:
                variables = RequestContext(request,{
                    'corpora'  : [corpus],
                    'show_edit': True,
                    'show_tags': True
                })
                return render_to_response('corpus_list.html', c, variables)
            else:
                return HttpResponseRedirect(
                    '/user/%s/' % request.user.username
                )
        else:
            if ajax:
                return HttpResponse("failure")
    elif 'title' in request.GET:
        title = request.GET['title']
        file  = ''
        tags  = ''
        try:
            title  = Corpus.objects.get(title=title)
            corpus = Corpus.objects.get(
                title=title, user=request.user
            )
            file = corpus.file
            tags  = ' '.join(
                tag.name for tag in corpus.tag_set.all()
            )
        except Corpus.DoesNotExist:
            pass
        form = CorpusSaveForm({
            'title': title,
            'file' : file,
            'tags' : tags
        })
    else:
        form  = CorpusSaveForm()
    variables = RequestContext(request, {
        'form': form
    })
    if ajax:
        return render_to_response('corpus_save_form.html', c, variables)
    else:
        return render_to_response('corpus_save.html', c, variables)


def _corpus_save(form, request):
    handle_uploaded_file(request.FILES['file'])
    # get or create a corpus
    corpus, created = Corpus.objects.get_or_create(
        title = form.cleaned_data['title'],
        file  = request.FILES['file'],
        user  = request.user
    )
    if not created:
        corpus.tag_set.clear()
        # create new tag list
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name = tag_name)
        corpus.tag_set.add(tag)
        # save corpus to database and return it
    corpus.save()
    #process_text(corpus)
    return corpus


def handle_uploaded_file(f):
    path = 'uploaded_text/'#linguist.corpusPath()
    destination = open((path + f.name), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return destination


def process_text(corpus):
    path = corpus.file
    wordcount, vocab, important, pairs = linguist.process(corpus, path)
    json_corpus(corpus, wordcount, "wordcount")
    json_corpus(corpus, important, "important")
    json_corpus(corpus, vocab, "vocab")
    # todo: incorporate the next line into visual output
    # #print repr(pairs)
    collocations = linguist.context(corpus, important)
    profile_corpus(corpus, collocations)
    path.close()

def json_corpus(corpus, dic, name):
    data_stream = linguist.jsonEncode(dic)
    json = Json.objects.create(
        name = name,
        data_stream = data_stream,
        corpus = corpus
    )

def profile_corpus(corpus, pairs, collocations):
    profile = Profile.objects.create(
        corpus  = corpus,
        pairs   = pairs,
        context = collocations
    )


#todo debug cloud_page
@login_required
def cloud_page(request):
    c = {}
    c.update(csrf(request))
    json = get_object_or_404(Corpus, json = json)
    variables = RequestContext(request, dict(json_file = json))
    return render_to_response('canvas_cloud.html', c, variables)


def search_page(request):
    c = {}
    c.update(csrf(request))
    form = SearchForm()
    corpora = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query':query})
            corpora = Corpus.objects.filter(
                title__icontains=query
            )[:10]
    variables = RequestContext(request, {
        'form': form,
        'corpora': corpora,
        'show_results': show_results,
        'show_tags': True,
        'show_user': True
    })
    if request.GET.has_key('ajax'):
        return render_to_response('corpus_list.html', c, variables)
    else:
        return render_to_response('search.html', c, variables)


def user_page(request, username):
    c = {}
    c.update(csrf(request))
    user = get_object_or_404(User, username=username)
    variables = RequestContext(request, {
        'username' : username,
        })
    return render_to_response('user_page.html', c, variables)


def register_page(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                email    = form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form  = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('registration/register.html', c, variables)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def main_page(request):
    return render_to_response('main_page.html', RequestContext(request))