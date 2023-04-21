from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image

def compress_image(image):
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'jpeg', quality=70, optimize=True)
    new_image = File(im_io, name=image.name)
    return new_image

class Turf(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    landmark = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    contact = models.CharField(max_length=10)
    email = models.EmailField()
    length = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to='turf_images')
    total_nets = models.PositiveSmallIntegerField()
    description = models.TextField()
    price = models.IntegerField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' - ' + self.city

    def save(self, force_insert=False, force_update=False, using=None, *args, **kwargs):
        if self.image:
            image = self.image
            if image.size > 0.3 * 1024 * 1024:  # if size greater than 300kb then it will compress image
                self.picture = compress_image(image)
        super(Turf, self).save(*args, **kwargs)


class Rating(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    rating_1_count = models.PositiveSmallIntegerField(default=0)
    rating_2_count = models.PositiveSmallIntegerField(default=0)
    rating_3_count = models.PositiveSmallIntegerField(default=0)
    rating_4_count = models.PositiveSmallIntegerField(default=0)
    rating_5_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.turf.name


class Timings(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.turf.name


class Booking(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.user


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username