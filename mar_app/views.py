from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from mar_app.models import *
from django.db.models import Count

def view_home(request):
    return render(request,'hpage.html')

# Displaying Home Page after login or register and authenticating user existance:
def display_home(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context={
            'user_in':User.objects.get(id=request.session['id']),
            'allanimes':Anime.objects.all(),
            'top_animes' : Anime.objects.all().annotate(num_revs=Count('reviews')).order_by('-num_revs')[:3],
        }
        return render(request,'mpage.html',context)
    
## Registering a New Account:
def new_sign_up(request):
    ## Checking if there is any validation errors
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect('/')
    else:
        ## Taking the password and hashing it directly:
        password = request.POST['userpass']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user1 = User.new_user(first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        user_name = request.POST['username'],
        dob = request.POST['bdate'],
        email_address = request.POST['useremail'],
        password = pw_hash)
        
        request.session['id'] = user1.id
        request.session['username'] = user1.first_name
        
        return redirect('/success')
    
def new_sign_in(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            user=User.objects.filter(email_address=request.POST['useremail'])
            logged_user=user[0]
            request.session['id']=logged_user.id
            request.session['username'] = logged_user.first_name
        
            return redirect('/success')
    else:
        redirect('/')

def destroy_session(request):
    request.session.flush()
    return redirect('/')

def display_contact(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request,'contact.html')
    
def display_add(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        return render(request,'add.html')
    
def create_anime(request):
    if request.method =='POST':
        errors = Anime.objects.anime_basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_new_anime')
        else: 
            user_id=request.session['id']
            anime1=Anime.new_anime(title=request.POST['title'],
            desc=request.POST['desc'],
            year = request.POST['year'],
            link = request.POST['ylink'],
            img_url = request.POST['ilink'],
            uploaded_by=User.objects.get(id=user_id))
            
            this_user=User.objects.get(id=user_id)
            animeid=anime1.id
            anime1.user_that_fav.add(this_user)
            return redirect ('/success')
        
def show_anime(request,anid):
    if 'id' not in request.session:
        return redirect('/')
    else:
        uploader = Anime.objects.get(id=anid)
        context = {
            'oneanime':Anime.one_anime(anid),
            'oneuser':User.user_in_account(request.session['id']),
            'reviews':Reviews.objects.all()
            }
        return render(request,'apage.html',context)
    
def postrev(request,anid):
    if 'id' not in request.session:
        return redirect('/')
    else:
        
        logged_user = User.objects.get(id=request.session['id'])
        showed_anime = Anime.objects.get(id = int(anid))
        review1 = Reviews.new_rev(anime=showed_anime,rating=request.POST['rating'],content=request.POST['content'],created_by=logged_user)
        # messages.success = 'Review Posted'
        
        context = {
            'oneanime':Anime.one_anime(anid),
            # 'revs': showed_anime.reviews.all(),
        }
        
        return render(request,'partial.html',context)
    
def deleteonerev(request,reviewid,oneanimeid):
    Reviews.delete_rev(reviewid)
    return redirect('/animes/'+str(oneanimeid))

def delthisan(request,anid):
    Anime.delete_anime(anid)
    return redirect("/success")

def show_edit(request,anid):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
                'oneanime':Anime.one_anime(anid),
                'oneuser':User.user_in_account(request.session['id'])
            }
        return render(request,'epage.html',context)
    
def edit_anime(request,oneanimeid):
    if 'id' not in request.session:
        return redirect('/')
    else:
        errors = Anime.objects.anime_basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect ('/event/'+str(oneanimeid)+'/edit')
    Anime.update_one(oneanimeid,request.POST['title'],request.POST['desc'],request.POST['year'],request.POST['ylink'],request.POST['ilink'])
    return redirect ('/success')


def favorite_this(request,anid):
    Anime.fav_add_one(request.session['id'],anid)
    return redirect("/success")

def unfavorite_this(request,anid):
    Anime.unfav_rem_one(request.session['id'],anid)
    return redirect("/success")


def display_shop(request):
    return render(request,'shop.html')