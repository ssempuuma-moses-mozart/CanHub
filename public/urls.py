from django.urls import path
from . import views
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='website-home'),
    # path('cancer_units/<int:pk>/', views.cancer_units, name='website-cancer_units'),
    path('cancer_units/', views.cancer_units, name='website-cancer_units'),
    path('cancer_experts/', views.cancer_experts, name='website-cancer_experts'),
    path('cancer_networks/', views.cancer_networks, name='website-cancer_networks'),
    path('cancer_organizations/', views.cancer_organizations, name='website-cancer_organizations'),
    path('cancer_experts_info/<int:item_id>', views.cancer_experts_info, name='website-cancer_experts_info'),
    path('cancer_organizations_info/<int:item_id>', views.cancer_organizations_info, name='website-cancer_organizations_info'),
    path('cancer_networks_info/<int:item_id>', views.cancer_networks_info, name='website-cancer_networks_info'),
    path('cancer_units_info/<int:item_id>', views.cancer_units_info, name='website-cancer_units_info'),
    path('cancer_types_info/<int:item_id>', views.cancer_types_info, name='website-cancer_types_info'),
    path('donate/<int:item_id>', views.donate, name='website-donate'),
    path('mobile_money/<int:item_id>', views.mobile_money, name='website-mobile_money'),
    path('pay/<int:item_id>', views.pay, name='website-pay'),
    path('give_gift/<int:item_id>', views.give_gift, name='website-give_gift'),
    path('pay_via_bank/<int:item_id>', views.pay_via_bank, name='website-pay_via_bank'),
    path('fundraiser/', views.fundraiser, name='website-fundraiser'),
    # path('crowdfunding_donation/', views.crowdfunding_donation, name='website-crowdfunding_donation'),
    path('video/', views.video, name='website-video'),
    path('cancer_types/', views.cancer_types, name='website-cancer_types'),
    path('infographics/', views.infographic, name='website-infographics'),
    path('presentation/', views.presentation, name='website-presentation'),
    path('keynotes/', views.keynotes, name='website-keynotes'),
    path('faqs/', views.faqs, name='website-faqs'),
    path('crowdfunding/', views.crowdfunding, name='website-crowdfunding'),
    path('campaign_info/<int:item_id>', views.campaign_info, name='campaign-info'),
    path('filtered_campaigns/', views.filtered_campaigns, name='filtered-campaigns'),
    path('crowdfunding_campaign_detail/int:pk', views.crowdfunding_campaign_detail, name='crowdfunding-campaign-detail'),
    path('create_campaign/', views.create_crowdfunding, name='create-crowdfunding'),

    path('settings/', views.settings, name='website-settings'),
    path('slider/', SliderTemplate.as_view(), name='slider'),
    path('slider_main/', SliderMainTemplate.as_view(), name='slider-main'),
    path('search_google/', views.search_google, name='search-google'),


    path('upload_file/', CancerNetworkUploadView.as_view(), name='upload_file'),
    path('upload_file_units/', CancerUnitUploadView.as_view(), name='upload_file_units'),
    path('upload_file_organization/', CancerOrganizationUploadView.as_view(), name='upload_file_organization'),


]
