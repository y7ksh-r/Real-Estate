from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land'),
    ]
    PROPERTY_STATUS = [
        ('readytomove', 'Ready To Move'),
        ('underconstrution', 'Under Construction'),
    ]
    main_img = models.ImageField(upload_to="media/images", default="")
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    property_status = models.CharField(max_length=50, choices=PROPERTY_STATUS, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_feet = models.IntegerField()
    map_url = models.TextField(null=True)
    video = models.TextField(null=True)
    lot_size = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)
    devloper = models.TextField(max_length=300, null=True)
    price2 = models.CharField(max_length=255, editable=False,default='NONE')  # Field for storing the price in words

    def convert_to_lakh_or_crore(self, value):
        if value >= 1_00_00_000:
            return f"{value / 1_00_00_000:.2f} crore"
        elif value >= 1_00_000:
            return f"{value / 1_00_000:.2f} lakh"
        else:
            return str(value)

    def save(self, *args, **kwargs):
        # Convert the price to lakhs or crores and store it in price2
        self.price2 = self.convert_to_lakh_or_crore(float(self.price))
        super(Property, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Photo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/',default="")

    def __str__(self):
        return f'Photo for {self.property.title}'
class inq(models.Model):
    property=models.CharField(null=True,max_length=100)   
    name=models.CharField(max_length=100)
    contactno=models.PositiveIntegerField()
    email=models.EmailField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} for {self.property}'
