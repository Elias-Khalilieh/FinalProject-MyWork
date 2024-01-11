from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['fname']) < 3:
            errors["fname"] = "User First Name should be at least 3 characters"
        if len(postData['lname']) < 3:
            errors["lname"] = "User Last Name should be at least 3 characters"
        if len(postData['username'])< 5:
            errors["username"] = "User Name Must be at Least 5 Characters"
        if postData['bdate'] == "":
            errors['bdate'] = "Please Enter a Valid Date!"
        else:
            userbirthdate = datetime.strptime(postData['bdate'],'%Y-%m-%d')
            if datetime.today() < userbirthdate:
                errors["bdate"] = "User's Birthday must be in the past!"
            elif ((datetime.today().year)-userbirthdate.year)<15:
                errors['bdate'] = "You are young to sign up here!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['useremail']):      
            errors['useremail'] = "Invalid email address!"
        if len(User.objects.filter(email_address = postData['useremail'])) > 0:
            errors["useremail"] = "Email address exist!"
            
        if len(postData['userpass']) < 8 :
            errors['userpass'] = "Password is Weak, Choose Another Please!"
        if postData['userpass'] != postData['confirmuserpass']:
            errors['confirmuserpass'] = "Password does not match!"
        return errors
    
    def login_validator(self, postData):
        errors ={}
        logged_user=User.objects.filter(email_address=postData['useremail'])
        if logged_user:
            user=logged_user[0]
        else:
            errors['useremail']='Email Not Found In DataBase. Please register.'
            return errors
        if bcrypt.checkpw(postData['userpass'].encode(), user.password.encode()):
            return errors
        else:
            errors['userpass']='Password does not match Email.Try Again! :).'
            return errors
        
class AnimeManager(models.Manager):
    def anime_basic_validator(self,postData):
        errors = {}
        if len(postData['title']) < 5:
            errors['title']="Please :) Add a Title!."
        if len(postData['desc']) < 10:
            errors['desc']="Description Must Be More Than 10 Characters."
        if postData['year'] > '2023':
            errors['year']="Please Enter a Valid Year"
        if postData['year'] < '0':
            errors['year']="Please Enter a Valid Year"
        if len(postData['ylink']) < 5:
            errors['ylink']="Invalid YouTube Link !"
        if len(postData['ilink']) < 5:
            errors['ilink']="Invalid Image Link !"
        return errors
    
class CUserManager(models.Manager):
    def c_basic_validator(self,postData):
        errors = {}
        if len(postData['cfname']) < 3:
            errors['cfname']="Type Your Name!"
        if len(postData['clname']) < 3:
            errors['clname']="Type Your Last Name!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['cemail']):      
            errors['cemail'] = "Invalid email address!"
        if len(postData['csubject'] ) < 5:
            errors['csubject'] = "Type a Subject"
        # if len(postData['cmessage']) < 10:
        #     errors['cmessage']="Message Must Be More Than 10 Characters."
        

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    dob = models.DateField()
    email_address = models.EmailField()
    password = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    ## Defining the function that will create the user in the database:
    def new_user(first_name,last_name,user_name,dob,email_address,password):
        return User.objects.create(first_name=first_name,last_name=last_name,user_name=user_name,dob=dob,email_address=email_address,password=password)
    def user_in_account(id):
        return User.objects.get(id=id)
    
class Anime(models.Model):
    title = models.CharField(max_length=45)
    desc = models.TextField()
    year = models.IntegerField()
    link = models.TextField()
    img_url = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="uploded_animes",on_delete=models.CASCADE)
    user_that_fav = models.ManyToManyField(User, related_name="fav_animes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AnimeManager()
    
    def new_anime(title,desc,year,link,img_url,uploaded_by):
        return Anime.objects.create(title=title, desc=desc,year=year,link=link,img_url=img_url,uploaded_by=uploaded_by)
    
    def one_anime(id):
        return Anime.objects.get(id=id)
    
    def update_one(id,title,desc,year,link,img_url):
        update1 =Anime.objects.get(id=int(id))
        update1.title=title
        update1.desc=desc
        update1.year=year
        update1.link=link
        update1.img_url=img_url
        update1.save()
        
    def delete_anime(id):
        anime1 = Anime.objects.filter(id=int(id))
        anime1.delete()
        
    def fav_add_one(userid,anid):
        user1 = User.objects.get(id=int(userid))
        anime1 = Anime.objects.get(id=int(anid))
        anime1.user_that_fav.add(user1)
        
    def unfav_rem_one(userid,anid):
        user1 = User.objects.get(id=int(userid))
        anime1 = Anime.objects.get(id=int(anid))
        anime1.user_that_fav.remove(user1)
        
    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating
        
        if reviews_total > 0:
            return reviews_total / self.reviews.count()
        
        return 0
    
class Reviews(models.Model):
    anime = models.ForeignKey(Anime, related_name='reviews', on_delete= models.CASCADE)
    rating = models.IntegerField(default = 3)
    content = models.TextField()
    created_by = models.ForeignKey(User,related_name = 'reviews',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def new_rev(anime,rating,content,created_by):
        Reviews.objects.create(anime=anime,rating=rating,content=content,created_by=created_by)
        
    def delete_rev(id):
        rev1 = Reviews.objects.get(id=int(id))
        rev1.delete()
        
class CUser(models.Model):
    c_fname = models.CharField(max_length=45)
    c_lname = models.CharField(max_length=45)
    c_email = models.EmailField()
    c_subject = models.CharField(max_length=45)
    c_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CUserManager()
    
    def new_con(c_fname,c_lname,c_email,c_subject,c_message):
        CUser.objects.create(c_fname=c_fname,c_lname=c_lname,c_email=c_email,c_subject=c_subject,c_message=c_message)
