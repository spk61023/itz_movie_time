from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

CITY_CHOICES    =   (
                        ('', 'City'),('Mumbai', 'Mumbai'), ('Delhi', 'Delhi'), ('Banglore', 'Banglore'), ('Chennai', 'Chennai')
                    )
STATE_CHOICES   =   (
                        ('','State'),
                        ('MH','Maharashtra'),
                        ('DL','Delhi'),
                        ('KA','Karnataka'),
                        ('TN','Tamil Nadu')
                    )
SEATING_PREFERENCES =   (
                            ('','Seating'),
                            ('classic','Classic'),
                            ('premium','Premium')
                        )
LANGUAGE_CHOICES =  (
                        ('','Language'),
                        ('English','English'),
                        ('Hindi','Hindi'),
                        ('KANNADA','KANNADA')
                    )
GENRE_CHOICES =     (
                        ('','Genre'),
                        ('Drama','Drama'),
                        ('Horror','Horror'),
                        ('Comedy','Comedy'),
                        ('Action','Action'),
                        ('Romance','Romance'),
                        ('Sci-Fi','Sci-Fi'),
                        ('Fiction','Fiction'),
                        ('Crime','Crime')
                    )
RATING_CHOICES =    (
                        ('','Rating'),
                        ('A','A'),
                        ('UA','UA')
                    )
SEAT_STATUS =   (
                    ('','Status'),
                    ('available','available'),
                    ('booked','booked')
                )
BOOKING_STATUS =    (
                        ('','Status'),
                        ('confirmed','confirmed'),
                        ('processing','processing'),
                        ('cancelled','cancelled')
                    )

PAYMENT_PREFERENCES =   (
                            ('','Payment mode'),
                            ('upi','UPI'),
                            ('credit_card','Credit Card'),
                            ('debit_card','Debit Card')
                        )
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone = None, password = None, *args, **kwargs):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            email = self.normalize_email(email),
            name  = name,
            phone = phone
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, name, phone=None, password=None):
        user = self.create_user(
            email,
            name,
            phone    = phone,
            password = password
            )
        user.is_superuser   = True
        user.is_staff       = True
        user.save(using=self._db)
        return user

class Users(AbstractUser):
    name                = models.CharField(max_length = 20)
    email               = models.EmailField(unique = True)
    phone               = models.CharField(max_length = 15, unique = True, null = True, blank = True)
    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['name', 'phone']
    objects = UserManager()

    def save(self, *args, **kwargs):
        return super(Users, self).save()

    def __str__(self):
        name    = self.name
        return name

class City(models.Model):
    ''' name, state, zip_code'''
    #user    = models.ForeignKey(Users,on_delete=models.CASCADE)
    state       =   models.CharField(choices = STATE_CHOICES, max_length = 100, null=True)
    name        =   models.CharField(choices = CITY_CHOICES, max_length = 100, null=True)
    zip_code    =   models.DecimalField(max_digits=10,decimal_places=0, default= 0)

    def __str__(self):
        return str(self.state) + " , " + str(self.name) + " zip_code " + str(self.zip_code)

class Theatre(models.Model):
    ''' name, no_of_screens, city_id'''
    name            = models.CharField(max_length = 50)
    no_of_screens   = models.DecimalField(max_digits=100,decimal_places=0, default= 0)
    city_id         = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Screen(models.Model):
    '''name, capacity, theatre_id'''
    name = models.CharField(max_length = 50)
    capacity = models.DecimalField(max_digits=100,decimal_places=0, default= 0)
    theatre_id = models.ForeignKey(Theatre,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class ScreenSeat(models.Model):
    ''' seat_no, type, screen_id'''
    seat_no = models.CharField(max_length = 50)
    type = models.CharField(choices = SEATING_PREFERENCES, max_length = 50, null=True)
    screen_id = models.ForeignKey(Screen,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.seat_no) + " type " + str(self.type) + " screen_id "+ str(self.screen_id)

class Movie(models.Model):
    def user_directory_path(instance, filename):
        '''file will be uploaded to MEDIA_ROOT /name/ <filename>'''
        ext         = filename.split('.')[-1]
        filename1   = "%s.%s" % (instance.name, ext)
        return '{0}/photos/{1}'.format(instance.name, filename1)

    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 950)
    duration = models.IntegerField(null = True, blank = True)
    language = models.CharField(choices = LANGUAGE_CHOICES, max_length = 100, null=True)
    image = models.ImageField(upload_to = user_directory_path, height_field = None, width_field = None, max_length = 100, null = True,
                              blank = True)
    trailer_url = models.URLField(max_length = 150, null=True, blank=True )
    genre = models.CharField(choices = GENRE_CHOICES, max_length = 100, null=True)
    rating = models.CharField(choices = RATING_CHOICES, max_length = 100, null=True)
    def __str__(self):
        return str(self.name)

class MovieCast(models.Model):
    def user_directory_path(instance, filename):
        '''file will be uploaded to MEDIA_ROOT /name/ <filename>'''
        ext         = filename.split('.')[-1]
        filename1   = "%s.%s" % (instance.name, ext)
        return '{0}/photos/{1}'.format(instance.name, filename1)

    name = models.CharField(max_length = 150)
    image = models.ImageField(upload_to = user_directory_path, height_field = None, width_field = None, max_length = 100, null = True,
                              blank = True)
    character_name = models.CharField(max_length = 150) #character_name which actor plays
    movie_id = models.ForeignKey(Movie,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Screening(models.Model):
    date        = models.DateField(null = True, blank = True )
    start_time  = models.DateTimeField(auto_now = False, null = True, blank = True)
    end_time    = models.DateTimeField(auto_now = False, null = True, blank = True)
    movie_id = models.ForeignKey(Movie,on_delete=models.CASCADE)
    screen_id   = models.ForeignKey(Screen,on_delete=models.CASCADE)
    theatre_id = models.ForeignKey(Theatre,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.screen_id) + "  " + str(self.movie_id)

class Booking(models.Model):
    timestamp = models.DateTimeField(auto_now = True)
    total_no_of_seats = models.IntegerField(null = True, blank = True )
    status = models.CharField(choices = BOOKING_STATUS, max_length = 50, null=True)
    screening_id = models.ForeignKey(Screening,on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class ShowSeat(models.Model):
    status = models.CharField(choices = SEAT_STATUS, max_length = 100, null=True)
    price       = models.DecimalField(max_digits=9,decimal_places=2, default= 0)
    type = models.CharField(choices = SEATING_PREFERENCES, max_length = 50, null=True)
    screen_seat_id = models.ForeignKey(ScreenSeat,on_delete=models.CASCADE)
    screening_id = models.ForeignKey(Screening,on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.status) + " type " + str(self.type) + " screening_id "+ str(self.screening_id)


class Payment(models.Model):
    ''' seat_no, type, screen_id'''
    account_no = models.IntegerField(null = True, blank = True )
    timestamp = models.DateTimeField(auto_now = True)
    payment_method = models.CharField(choices = PAYMENT_PREFERENCES, max_length = 50, null=True)
    type = models.CharField(choices = SEATING_PREFERENCES, max_length = 50, null=True)
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.account_no)


# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'pages/signup.html'
