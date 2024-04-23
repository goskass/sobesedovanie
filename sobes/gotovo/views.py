from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
import string

def count_words(text, word):
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
    cleaned_text = cleaned_text.replace('\n', ' ')
    cleaned_text = cleaned_text.lower()
    words = cleaned_text.split()
    words = [word for word in words if word]
    return words.count(word.lower())

def word_counter(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            try:
                file_content = uploaded_file.read().decode('utf-8')
            except UnicodeDecodeError:
                return HttpResponse("Error: Unable to decode file content", status=400)

            word = request.POST.get('word', '')
            count = count_words(file_content, word)
            request.session['word_count'] = count
            request.session['searched_word'] = word
            return redirect('word_counter')
        elif 'action' in request.POST and request.POST['action'] == 'clear':
            request.session.pop('word_count', None)
            request.session.pop('searched_word', None)
    else:
        form = UploadFileForm()

    count = request.session.get('word_count', 0)
    searched_word = request.session.get('searched_word', '')
    return render(request, 'word_counter.html', {'form': form, 'count': count, 'searched_word': searched_word})

