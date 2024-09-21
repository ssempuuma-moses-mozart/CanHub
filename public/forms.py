import csv
import io
from django import forms
from .models import *
import datetime

# class ApplyCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = ServiceProvider
# 		fields =('service','name','capacity','phone','email','address','description')

class CancerUnitCreateForm(forms.ModelForm):
	class Meta:
		model = CancerUnit
		fields =('name','category','location','description','uploaded_image','date_created','date')

class CancerTypeCreateForm(forms.ModelForm):
	class Meta:
		model = CancerType
		fields =('title','description','cancertype','date_created','date')

class CancerExpertCreateForm(forms.ModelForm):
	class Meta:
		model = CancerExpert
		fields =('name','speciality','location','description','date_created','date')

class VideoCreateForm(forms.ModelForm):
	class Meta:
		model = Video
		fields =('video_file','title','description','date_created','date')

class PresentationCreateForm(forms.ModelForm):
	class Meta:
		model = Presentation
		fields =('name','organization','profile_image','topic','powerpoint_file','date_created','date')
		
class InfographicCreateForm(forms.ModelForm):
	class Meta:
		model = Infographic
		fields =('cancertype','infographic_image','date_created')  

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='Allowed file types: .xlsx, .xls, .csv',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx, .xls, .csv',
        })
    )

class CancerNetworkCreateForm(forms.ModelForm):
	class Meta:
		model = CancerNetwork
		fields =('name','location','description','date_created','date')

class CancerOrganizationCreateForm(forms.ModelForm):
	class Meta:
		model = CancerOrganization
		fields =('name','location','description','date_created','date')

# class CrowdfundingCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = Crowdfunding
# 		fields =('campaign_image','title','description','name','raised_amount','goal_amount','open_date','closing_date')

class CrowdfundingForm(forms.ModelForm):
    class Meta:
        model = Crowdfunding
        fields = "__all__"

        widgets = {
            'campaign_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'campaign_video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            #'status': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
			'cancertype': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cancertype'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'raised_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Raised Amount'}),
            'goal_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Goal Amount'}),
            'open_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CrowdfundingForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['name'].required = True
        self.fields['goal_amount'].required = True
        self.fields['open_date'].required = True
        self.fields['closing_date'].required = True
        self.fields['category'].required = True
        self.fields['location'].required = True 

class UploadCancerNetwork(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)
		for record in reader:
			CancerNetwork.objects.update_or_create(id = record['id'], defaults={'name':record['name'],'location':record['location'],'description':record['description']})
			


class UploadCancerUnit(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)
		for record in reader:
			CancerUnit.objects.update_or_create(id = record['id'], defaults={'name':record['name'],'location':record['location'],'category':record['category'],'description':record['description']})


class UploadCancerOrganization(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)
		for record in reader:
			CancerOrganization.objects.update_or_create(id = record['id'], defaults={'name':record['name'],'location':record['location'],'description':record['description']})
