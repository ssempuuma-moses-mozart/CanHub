from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.core.validators import MinLengthValidator


class CancerUnit(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	category = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800,blank=True, null=True,)
	uploaded_image = models.ImageField(upload_to='uploaded_image/', blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'
	
class CancerExpert(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	speciality = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=250,blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'	
	

class CancerNetwork(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800,blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'
	
class CancerOrganization(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True,)
	location = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800,blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'	


class Video(models.Model):
	video_file = models.FileField(upload_to='videos/', blank=True, null=True,) 
	title = models.CharField(max_length=250, blank=True, null=True,)
	cancertype = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=800, blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.title} {self.title}'
	
class Presentation(models.Model):
	name = models.CharField(max_length=250)
	organization = models.CharField(max_length=250, blank=True, null=True,)
	cancer_type = models.CharField(max_length=250, blank=True, null=True,)
	profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,)
	topic = models.CharField(max_length=250, blank=True, null=True,)
	powerpoint_file = models.FileField(upload_to='powerpoint_files/', blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.name} {self.name}'
	
class Infographic(models.Model):
	cancertype = models.CharField(max_length=250)
	infographic_image = models.ImageField(upload_to='infographic_images/', blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.cancertype} {self.cancertype}'    



class CancerType(models.Model):
	title = models.CharField(max_length=250, blank=True, null=True,)
	definition = models.CharField(max_length=250, blank=True, null=True,)
	description = models.CharField(max_length=250, blank=True, null=True,)
	cancertype = models.CharField(max_length=250, blank=True, null=True,)
	causes = models.CharField(max_length=250, blank=True, null=True,)
	symptoms = models.CharField(max_length=250, blank=True, null=True,)
	diagnosed = models.CharField(max_length=250, blank=True, null=True,)
	treatment = models.CharField(max_length=250, blank=True, null=True,)
	prevented = models.CharField(max_length=250, blank=True, null=True,)
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.title} {self.cancertype}'
	

# class Crowdfunding(models.Model):
#     campaign_image = models.ImageField(upload_to='campaign_images/', blank=True, null=True,)
#     title = models.CharField(max_length=250, blank=True, null=True)
#     description = models.CharField(max_length=250, blank=True, null=True)
#     name = models.CharField(max_length=20, blank=True, null=True)
#     raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     open_date = models.DateField(default=timezone.now)
#     closing_date = models.DateField(blank=True, null=True)
#     def __str__(self):
# 	    return f'{self.title} {self.title}'


#Add status to the campaign
class Status(models.Model):
    APPROVED = 'Approved'
    NOT_APPROVED = 'Not Approved'
    REVOKED = 'Revoked'
    COMPLETED = 'Completed'
    PENDING = 'Pending'

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (NOT_APPROVED, 'Not Approved'),
        (REVOKED, 'Revoked'),
        (COMPLETED, 'Completed'),
        (PENDING, 'Pending'),
    ]

    name = models.CharField(max_length=20, choices=STATUS_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Crowdfunding(models.Model):
    # Define category choices
    MEDICAL_COSTS = 'Medical Costs'
    SUPPORT_SERVICES = 'Support Services'
    LOGISTICS_ASSISTANCE = 'Logistics Assistance'
    MEDICAL_DEVICES_AND_AIDS = 'Medical Devices and Aids'
    HEALTH_MANAGEMENT = 'Health Management'
    PERSONAL_NEEDS = 'Personal Needs'
    
    CATEGORY_CHOICES = [
        (MEDICAL_COSTS, 'Medical Costs'),
        (SUPPORT_SERVICES, 'Support Services'),
        (LOGISTICS_ASSISTANCE, 'Logistics Assistance'),
        (MEDICAL_DEVICES_AND_AIDS, 'Medical Devices and Aids'),
        (HEALTH_MANAGEMENT, 'Health Management'),
        (PERSONAL_NEEDS, 'Personal Needs'),
    ]

    # List of districts in Uganda
    DISTRICTS = [
        ('Abim', 'Abim'),
        ('Adjumani', 'Adjumani'),
        ('Agago', 'Agago'),
        ('Alebtong', 'Alebtong'),
        ('Amolatar', 'Amolatar'),
        ('Amudat', 'Amudat'),
        ('Amuria', 'Amuria'),
        ('Amuru', 'Amuru'),
        ('Apac', 'Apac'),
        ('Arua', 'Arua'),
        ('Budaka', 'Budaka'),
        ('Bududa', 'Bududa'),
        ('Bugiri', 'Bugiri'),
        ('Bugweri', 'Bugweri'),
        ('Buhweju', 'Buhweju'),
        ('Buikwe', 'Buikwe'),
        ('Bukedea', 'Bukedea'),
        ('Bukomansimbi', 'Bukomansimbi'),
        ('Bukwo', 'Bukwo'),
        ('Bulambuli', 'Bulambuli'),
        ('Buliisa', 'Buliisa'),
        ('Bundibugyo', 'Bundibugyo'),
        ('Bunyangabu', 'Bunyangabu'),
        ('Bushenyi', 'Bushenyi'),
        ('Busia', 'Busia'),
        ('Butaleja', 'Butaleja'),
        ('Butambala', 'Butambala'),
        ('Butebo', 'Butebo'),
        ('Buvuma', 'Buvuma'),
        ('Buyende', 'Buyende'),
        ('Dokolo', 'Dokolo'),
        ('Gomba', 'Gomba'),
        ('Gulu', 'Gulu'),
        ('Hoima', 'Hoima'),
        ('Ibanda', 'Ibanda'),
        ('Iganga', 'Iganga'),
        ('Isingiro', 'Isingiro'),
        ('Jinja', 'Jinja'),
        ('Kaabong', 'Kaabong'),
        ('Kabale', 'Kabale'),
        ('Kabarole', 'Kabarole'),
        ('Kaberamaido', 'Kaberamaido'),
        ('Kagadi', 'Kagadi'),
        ('Kakumiro', 'Kakumiro'),
        ('Kalangala', 'Kalangala'),
        ('Kaliro', 'Kaliro'),
        ('Kalungu', 'Kalungu'),
        ('Kampala', 'Kampala'),
        ('Kamuli', 'Kamuli'),
        ('Kamwenge', 'Kamwenge'),
        ('Kanungu', 'Kanungu'),
        ('Kapchorwa', 'Kapchorwa'),
        ('Kapelebyong', 'Kapelebyong'),
        ('Karenga', 'Karenga'),
        ('Kasanda', 'Kasanda'),
        ('Kasese', 'Kasese'),
        ('Katakwi', 'Katakwi'),
        ('Kayunga', 'Kayunga'),
        ('Kazo', 'Kazo'),
        ('Kibaale', 'Kibaale'),
        ('Kiboga', 'Kiboga'),
        ('Kibuku', 'Kibuku'),
        ('Kigezi', 'Kigezi'),
        ('Kikuube', 'Kikuube'),
        ('Kiruhura', 'Kiruhura'),
        ('Kiryandongo', 'Kiryandongo'),
        ('Kisoro', 'Kisoro'),
        ('Kitagwenda', 'Kitagwenda'),
        ('Kitgum', 'Kitgum'),
        ('Koboko', 'Koboko'),
        ('Kole', 'Kole'),
        ('Kotido', 'Kotido'),
        ('Kumi', 'Kumi'),
        ('Kwania', 'Kwania'),
        ('Kween', 'Kween'),
        ('Kyankwanzi', 'Kyankwanzi'),
        ('Kyegegwa', 'Kyegegwa'),
        ('Kyenjojo', 'Kyenjojo'),
        ('Lamwo', 'Lamwo'),
        ('Lira', 'Lira'),
        ('Luuka', 'Luuka'),
        ('Luwero', 'Luwero'),
        ('Lwengo', 'Lwengo'),
        ('Lyantonde', 'Lyantonde'),
        ('Manafwa', 'Manafwa'),
        ('Maracha', 'Maracha'),
        ('Masaka', 'Masaka'),
        ('Masindi', 'Masindi'),
        ('Mayuge', 'Mayuge'),
        ('Mbale', 'Mbale'),
        ('Mbarara', 'Mbarara'),
        ('Mitooma', 'Mitooma'),
        ('Mityana', 'Mityana'),
        ('Moroto', 'Moroto'),
        ('Moyo', 'Moyo'),
        ('Mpigi', 'Mpigi'),
        ('Mubende', 'Mubende'),
        ('Mukono', 'Mukono'),
        ('Nabilatuk', 'Nabilatuk'),
        ('Nakapiripirit', 'Nakapiripirit'),
        ('Nakaseke', 'Nakaseke'),
        ('Nakasongola', 'Nakasongola'),
        ('Namayingo', 'Namayingo'),
        ('Namisindwa', 'Namisindwa'),
        ('Namutumba', 'Namutumba'),
        ('Napak', 'Napak'),
        ('Nebbi', 'Nebbi'),
        ('Ngora', 'Ngora'),
        ('Ntoroko', 'Ntoroko'),
        ('Ntungamo', 'Ntungamo'),
        ('Nwoya', 'Nwoya'),
        ('Obongi', 'Obongi'),
        ('Omoro', 'Omoro'),
        ('Otuke', 'Otuke'),
        ('Oyam', 'Oyam'),
        ('Pader', 'Pader'),
        ('Pakwach', 'Pakwach'),
        ('Pallisa', 'Pallisa'),
        ('Rakai', 'Rakai'),
        ('Rubanda', 'Rubanda'),
        ('Rubirizi', 'Rubirizi'),
        ('Rukiga', 'Rukiga'),
        ('Rukungiri', 'Rukungiri'),
        ('Rwampara', 'Rwampara'),
        ('Sembabule', 'Sembabule'),
        ('Serere', 'Serere'),
        ('Sheema', 'Sheema'),
        ('Sironko', 'Sironko'),
        ('Soroti', 'Soroti'),
        ('Tororo', 'Tororo'),
        ('Wakiso', 'Wakiso'),
        ('Yumbe', 'Yumbe'),
        ('Zombo', 'Zombo'),
    ]

    campaign_image = models.ImageField(upload_to='campaign_images/', blank=True, null=True)
    campaign_video = models.FileField(upload_to='campaign_videos/', blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    open_date = models.DateField(default=timezone.now)
    closing_date = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=MEDICAL_COSTS)
    location = models.CharField(max_length=50, choices=DISTRICTS, default='Kampala')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.title} - {self.name}'

class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Crowdfunding, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Donation by {self.user} for {self.item} on {self.date}"
