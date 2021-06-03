from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomContactForm


def contact_page(request):
    print('contact')
    forms = CustomContactForm()
    if request.method == 'POST':
        forms = CustomContactForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.add_message(request, messages.INFO, 'Message sent successfully!')
            return redirect('posts:main-board')
    context = {
        'forms': forms
    }
    return render(request, 'contact/contact.html', context)