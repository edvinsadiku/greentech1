from django.shortcuts import render, get_object_or_404
from .models import Home, Service, AboutUs, Contact
from .forms import ContactForm
from django.http import HttpResponseRedirect


def home_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            return HttpResponseRedirect('/#contact-section')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'home.html', context)

from django.shortcuts import render, redirect
from .models import Service
from .forms import ServiceForm  # Import the form for creating new services



def services_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create a new service object
            return redirect('services')  # Redirect to the same page to display the updated list of services
    else:
        form = ServiceForm()

    services = Service.objects.all()
    return render(request, 'services.html', {'services': services, 'form': form})

def about_us_view(request):
    about_us = AboutUs.objects.first()
    return render(request, 'about_us.html', {'about_us': about_us})

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save()  # Save the form data into the Contact model
            
            # Prepare email context
            email_context = {
                'name': contact_instance.name,
                'email': contact_instance.email,
                'message': contact_instance.message,
            }

            # Render HTML email template
            html_content = render_to_string('index.html', email_context)
            text_content = strip_tags(html_content)  # Fallback to plain text content

            subject = 'New Contact Form Submission'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            # Create the email
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")

            # Send the email
            email.send()
            
            messages.success(request, 'Your message has been sent successfully!')  # Add success message
            return redirect('/#contact')  # Redirect after successful submission
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

