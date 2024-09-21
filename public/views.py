from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db.models import F, ExpressionWrapper, DecimalField

import csv
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
import pandas as pd


from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from django.db import IntegrityError
from django.db.models import Sum, Count

def home(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}

	return render(request, 'public/home.html', context)



def cancer_units(request):
    # Fetch all CancerUnit objects from the database
    cancer_units = CancerUnit.objects.all()

    # Create a dictionary to store units grouped by category
    units_by_category = {}

    for unit in cancer_units:
        if unit.category in units_by_category:
            units_by_category[unit.category].append(unit)
        else:
            units_by_category[unit.category] = [unit]

    if request.method == 'POST':
        form = CancerUnitCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerUnitCreateForm()
    
    context = {
        'form': form,
        'units_by_category': units_by_category,  # Pass the units grouped by category to the template context
        'cancer_units': cancer_units
    }
    return render(request, 'public/cancer_units.html', context)


# def cancer_units(request):
#     # Fetch all CancerUnit objects from the database
#     cancer_units = CancerUnit.objects.all()

#     unique_categories = set()  # Create an empty set to store unique categories
#     unique_units = []  # Create an empty list to store unique units
    
#     for unit in cancer_units:
#         if unit.category not in unique_categories:
#             unique_units.append(unit)  # Append the unique unit to the list
#             unique_categories.add(unit.category)  # Add the category to the set

#     if request.method == 'POST':
#         form = CancerUnitCreateForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('success_url')  # Redirect to a success page or another URL
#     else:
#         form = CancerUnitCreateForm()
    
#     context = {
#         'form': form,
#         'cancer_units': unique_units,  # Pass the unique units to the template context
#     }
#     return render(request, 'public/cancer_units.html', context)






# def cancer_units(request):
#     # Fetch all CancerUnit objects from the database
#     cancer_units = CancerUnit.objects.all()

#     if request.method == 'POST':
#         form = CancerUnitCreateForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('success_url')  # Redirect to a success page or another URL
#     else:
#         form = CancerUnitCreateForm()
    
#     context = {
#         'form': form,
#         'cancer_units': cancer_units,  # Pass the queryset to the template context
#     }
#     return render(request, 'public/cancer_units.html', context)

def cancer_experts(request):
    # Fetch all CancerExpert objects from the database
    cancer_experts = CancerExpert.objects.all()

    if request.method == 'POST':
        form = CancerExpertCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerExpertCreateForm()
    
    context = {
        'form': form,
        'cancer_experts': cancer_experts,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_experts.html', context)



def cancer_networks(request):
    # Get filter values from GET parameters
    location_filter = request.GET.get('location')
    name_filter = request.GET.get('name')

    # Apply location filter if selected
    if location_filter and location_filter != "0":  # "0" for "All" locations
        cancer_networks = CancerNetwork.objects.filter(location=location_filter)
    else:
        cancer_networks = CancerNetwork.objects.all()

    # Apply name filter if selected
    if name_filter and name_filter != "0":  # "0" for "All" names
        cancer_networks = CancerNetwork.objects.filter(name=name_filter)

    if request.method == 'POST':
        form = CancerNetworkCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerNetworkCreateForm()

    # Get distinct locations and names for the filter dropdowns
    locations = CancerNetwork.objects.values_list('location', flat=True).distinct()
    names = CancerNetwork.objects.values_list('name', flat=True).distinct()

    context = {
        'form': form,
        'cancer_networks': cancer_networks,  # Pass the filtered queryset to the template context
        'locations': locations,  # Pass the distinct locations for the dropdown
        'names': names,  # Pass the distinct names for the dropdown
        'selected_location': location_filter,  # Pass the selected location to the template
        'selected_name': name_filter,  # Pass the selected name to the template
    }
    return render(request, 'public/cancer_networks.html', context)

    # Fetch all CancerUnit objects from the database
    # cancer_networks = CancerNetwork.objects.all()

    # if request.method == 'POST':
    #     form = CancerNetworkCreateForm(request.POST)
    #     if form.is_valid():
    #         form.save()  # Save the form data to the database
    #         return redirect('success_url')  # Redirect to a success page or another URL
    # else:
    #     form = CancerNetworkCreateForm()
    
    # context = {
    #     'form': form,
    #     'cancer_networks': cancer_networks,  # Pass the queryset to the template context
    # }
    # return render(request, 'public/cancer_networks.html', context)


def cancer_organizations(request):
     # Get filter values from GET parameters
    location_filter = request.GET.get('location')
    name_filter = request.GET.get('name')

    # Apply location filter if selected
    if location_filter and location_filter != "0":  # "0" for "All" locations
        cancer_organizations = CancerOrganization.objects.filter(location=location_filter)
    else:
        cancer_organizations = CancerOrganization.objects.all()

    # Apply name filter if selected
    if name_filter and name_filter != "0":  # "0" for "All" names
        cancer_organizations = CancerOrganization.objects.filter(name=name_filter)

    if request.method == 'POST':
        form = CancerOrganizationCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerOrganizationCreateForm()

    # Get distinct locations and names for the filter dropdowns
    locations = CancerOrganization.objects.values_list('location', flat=True).distinct()
    names = CancerOrganization.objects.values_list('name', flat=True).distinct()

    context = {
        'form': form,
        'cancer_organizations': cancer_organizations,  # Pass the filtered queryset to the template context
        'locations': locations,  # Pass the distinct locations for the dropdown
        'names': names,  # Pass the distinct names for the dropdown
        'selected_location': location_filter,  # Pass the selected location to the template
        'selected_name': name_filter,  # Pass the selected name to the template
    }
    # Fetch all CancerUnit objects from the database
    # cancer_organizations = CancerOrganization.objects.all()

    # if request.method == 'POST':
    #     form = CancerOrganizationCreateForm(request.POST)
    #     if form.is_valid():
    #         form.save()  # Save the form data to the database
    #         return redirect('success_url')  # Redirect to a success page or another URL
    # else:
    #     form = CancerOrganizationCreateForm()
    
    # context = {
    #     'form': form,
    #     'cancer_organizations': cancer_organizations,  # Pass the queryset to the template context
    # }
    return render(request, 'public/cancer_organizations.html', context)

# def cancer_experts(request):
	
# 	context = {}
	
# 	return render(request, 'public/cancer_experts.html', context)

def video(request):
    # Fetch all Video objects from the database
    video = Video.objects.all()

    if request.method == 'POST':
        form = VideoCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = VideoCreateForm()
    
    context = {
        'form': form,
        'video': video,  # Pass the queryset to the template context
    }
    return render(request, 'public/video.html', context)


def presentation(request):
    # Fetch all Video objects from the database
    # cancer_units = unit.objects.all().order_by('name')
    presentation = Presentation.objects.all()  # Retrieve all presentations
    unique_cancer_types = Presentation.objects.values_list('cancer_type', flat=True).distinct()

    if request.method == 'POST':
        form = PresentationCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = PresentationCreateForm()
    
    context = {
        'form': form,
        'presentation': presentation,  # Adjusted variable name to match the template context
        'unique_cancer_types': unique_cancer_types,
    }
    return render(request, 'public/presentation.html', context)

def infographic(request):
    # Fetch all Infographic objects from the database
    infographic = Infographic.objects.all()

    if request.method == 'POST':
        form = InfographicCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = InfographicCreateForm()
    
    context = {
        'form': form,
        'infographic': infographic,  # Pass the queryset to the template context
    }
    return render(request, 'public/infographics.html', context)


def cancer_experts_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerExpert, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'location': item.location,
        'speciality': item.speciality,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_experts_info.html', context)


# def cancer_experts_info(request):
	
# 	context = {}
	
# 	return render(request, 'public/cancer_experts_info.html', context)


def cancer_units_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerUnit, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'category': item.category,
        'location': item.location,
        'uploaded_image': item.uploaded_image,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_units_info.html', context)


def cancer_types_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerType, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'title': item.title,
        'description': item.description,
        'cancertype': item.cancertype,
        'symptoms': item.symptoms,
        'diagnosed': item.diagnosed,
        'treatment': item.treatment,
        'prevented': item.prevented,
        'causes': item.causes,
        'definition': item.definition,
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_types_info.html', context)


def cancer_organizations_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerOrganization, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'location': item.location,
        'description': item.description       
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_organizations_info.html', context)

def cancer_networks_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(CancerNetwork, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'name': item.name,
        'location': item.location,
        'description': item.description
    }
    
    # Render the details page template with the item details
    return render(request, 'public/cancer_networks_info.html', context)


def cancer_types(request):
    # Fetch all CancerUnit objects from the database
    cancer_types = CancerType.objects.all()

    if request.method == 'POST':
        form = CancerTypeCreateForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CancerTypeCreateForm()
    
    context = {
        'form': form,
        'cancer_types': cancer_types,  # Pass the queryset to the template context
    }
    return render(request, 'public/cancer_types.html', context)

# def infographics(request):
	
# 	context = {}
	
# 	return render(request, 'public/infographics.html', context)

def presentations(request):
	# cancer_units = unit.objects.all().order_by('name')

    context = {}

    return render(request, 'public/presentations.html', context)

def keynotes(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/keynotes.html', context)

def faqs(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/faqs.html', context)

# def crowdfunding(request):

# 	context = {}
	
# 	return render(request, 'public/crowdfunding.html', context)


def crowdfunding(request):
    # Get the Status object with the 'Approved' name
    approved_status = Status.objects.get(name='Approved')
    # Check if the user is authenticated
    is_logged_in = request.user.is_authenticated
    # Filter the Crowdfunding queryset to include only campaigns with the approved status
    crowdfunding = Crowdfunding.objects.filter(status=approved_status).order_by('-id')

    for unit in crowdfunding:
        if unit.goal_amount != 0:
            unit.percentage_achieved = (unit.raised_amount / unit.goal_amount) * 100
        else:
            unit.percentage_achieved = 0

    if request.method == 'POST':
        form = CrowdfundingForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('success_url')  # Redirect to a success page or another URL
    else:
        form = CrowdfundingForm()
    
    context = {
        'form': form,
        'crowdfunding': crowdfunding,  # Pass the queryset to the template context
        'is_logged_in': is_logged_in,
    }
    return render(request, 'public/crowdfunding.html', context)



#create crowdfuning campaign
def create_crowdfunding(request):
    if request.method == 'POST':
        form = CrowdfundingForm(request.POST, request.FILES)
        if form.is_valid():
            crowdfunding_instance = form.save()
            messages.success(request, 'Crowdfunding campaign created successfully!')
            return redirect('create-crowdfunding')  # Redirect to the same page or another relevant page
        else:
            # Print form errors to the console for debugging
            print(form.errors)
            messages.error(request, 'There was an error creating the crowdfunding campaign. Please check the form and try again.')
    else:
        form = CrowdfundingForm()

    return render(request, 'public/create_campaign.html', {'form': form})



# sigle campain detailsview

def crowdfunding_campaign_detail(request, pk):
    # Retrieve the campaign or return a 404 error if not found
    campaign = get_object_or_404(Crowdfunding, pk=pk)
    
    
    # Additional context data
    related_campaigns = Crowdfunding.objects.exclude(pk=pk)[:3]  # Get 3 other campaigns for context
    similar_campaigns = Crowdfunding.objects.filter(category=campaign.category).exclude(pk=pk)[:3]  # Get 3 similar campaigns for context
    
    context = {
        'campaign': campaign,
        'related_campaigns': related_campaigns,
        'similar_campaigns': similar_campaigns,
    }
    
    return render(request, 'crowdfunding_campaign_detail.html', context)




# sigle campaign details view
def campaign_info(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    top_donations = Donation.objects.filter(item=item).order_by('-amount')[:5]
    
    # Calculate percentage achieved
    percentage_achieved = ExpressionWrapper((F('raised_amount') / F('goal_amount')) * 100, output_field=DecimalField(max_digits=5, decimal_places=2))
    
    # Pass the item details to the template along with percentage achieved
    percentage_achieved_value = Crowdfunding.objects.annotate(percentage_achieved=percentage_achieved).filter(pk=item_id).values_list('percentage_achieved', flat=True).first()
    
    context = {
        'campaign_image': item.campaign_image,
        'campaign_video': item.campaign_video,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date,
        'percentage_achieved': percentage_achieved_value,
        'category': item.category,
        'location': item.location,
        'status': item.status,
        'top_donations': top_donations
    }
    
    return render(request, 'public/campaign_info.html', context)





#view filterd campaigns

def filtered_campaigns(request):
    location = request.GET.get('location')
    category = request.GET.get('category')
    amount_required = request.GET.get('amount_required')
    donation_type = request.GET.get('donation_type')
    
    campaigns = Crowdfunding.objects.all()

    if location:
        campaigns = campaigns.filter(location=location)
    if category:
        campaigns = campaigns.filter(category=category)
    if amount_required:
        campaigns = campaigns.filter(goal_amount__gte=amount_required)
    if donation_type:
        campaigns = campaigns.filter(donation_type=donation_type)
    
    response_data = []
    for campaign in campaigns:
        response_data.append({
            'id': campaign.id,
            'title': campaign.title,
            'campaign_image_url': campaign.campaign_image.url,
            'raised_amount': campaign.raised_amount,
            'goal_amount': campaign.goal_amount,
            'percentage_achieved': campaign.percentage_achieved,
            'closing_date': campaign.closing_date.strftime('%Y-%m-%d'),
            'location': campaign.location,  # Add location to response data
            'category': campaign.category   # Add category to response data
        })
    
    return JsonResponse({'campaigns': response_data})



def fundraiser(request):
	# cancer_units = unit.objects.all().order_by('name')
	context = {}
	
	return render(request, 'public/fundraiser.html', context)


def donate(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'name': item.name,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
        
    }
    
    # Render the details page template with the item details
    return render(request, 'public/donate.html', context)


def mobile_money(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
    }
    
    # Render the details page template with the item details
    return render(request, 'public/mobile_money.html', context)



# @login_required
def pay(request, item_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        user = request.user
        item = get_object_or_404(Crowdfunding, pk=item_id)
        
        # Update raised_amount of the selected item
        item.raised_amount += int(amount)  # Convert amount to integer
        item.save()

        # Save the donation details
        donation = Donation(user=user, item=item, amount=amount)
        donation.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # If the request method is not POST, render the pay.html template as before
    item = get_object_or_404(Crowdfunding, pk=item_id)
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,
        'closing_date': item.closing_date
    }

    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        context['authenticated'] = False
    else:
        context['authenticated'] = True

    return render(request, 'public/pay.html', context)


def give_gift(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
    }
    
    # Render the details page template with the item details
    return render(request, 'public/give_gift.html', context)

def pay_via_bank(request, item_id):
    # Retrieve the selected item from the database
    item = get_object_or_404(Crowdfunding, pk=item_id)
    
    # Pass the item details to the template
    context = {
        'campaign_image': item.campaign_image,
        'title': item.title,
        'description': item.description,
        'raised_amount': item.raised_amount,
        'goal_amount': item.goal_amount,
        'open_date': item.open_date,
        'donation_id': item_id,  # Pass the donation_id to the template context
        'closing_date': item.closing_date
    }
    
    # Render the details page template with the item details
    return render(request, 'public/pay_via_bank.html', context)

def settings(request):
	return render(request, 'public/settings.html', {'title': 'Settings'})

def search_google(request):
	return render(request, 'public/search_google.html', {'title': 'Search'})

class SliderTemplate(TemplateView):
	template_name = 'public/slider.html'

class SliderMainTemplate(TemplateView):
	template_name = 'public/slider_main.html'

class CancerNetworkUploadView(FormView):
	template_name = 'public/upload_file.html'
	form_class = UploadCancerNetwork
	success_url = '/upload_file/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = 'Upload Cancer Network'  # Add the heading to the context
		return context

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)
     


class CancerUnitUploadView(FormView):
	template_name = 'public/upload_file.html'
	form_class = UploadCancerUnit
	success_url = '/upload_file/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = 'Upload Cancer Facilities'  # Add the heading to the context
		return context

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)
     

class CancerOrganizationUploadView(FormView):
	template_name = 'public/upload_file.html'
	form_class = UploadCancerOrganization
	success_url = '/upload_file/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = 'Upload Cancer Organization'  # Add the heading to the context
		return context

	def form_valid(self, form):
		form.process_data()
		return super().form_valid(form)     