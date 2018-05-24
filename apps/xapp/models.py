from django.db import models
import bcrypt
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

now = str(datetime.now())
# print(type(now))

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class UserManager(models.Manager):

    def regValidator(self, form):

        errors = []
        if not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif User.objects.filter(email=form['email']):
             errors.append("Account already exists.")
        if len(form['name']) < 3:
            errors.append("Name must have at least 3 characters.")
        if len(form['alias']) < 2:
            errors.append("Alias must have at least 3 characters.")
        elif User.objects.filter(alias=form['alias']):
             errors.append("Alias already exists.")
        if not form['bday']:
            errors.append('Date Of Birth is required')
        elif form['bday'] > now:
            errors.append("Date of birth can't be in the future.")
        if len(form['pass']) < 5:
            errors.append("Password must have at least 5 characters.")
        elif form['pass'] != form['confirmpass']:
            errors.append("Password and confirm password must match.")


        if not errors:
            hash1 = bcrypt.hashpw(form['pass'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=form['name'], alias=form['alias'], email=form['email'], bday=form['bday'], password=hash1)
            return (True, user)
        else:
            return (False, errors)


    def loginValidator(self, form):

        errors = []

        if not form['email']:
            errors.append("Email required.")
        elif not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif not User.objects.filter(email=form['email']):
             errors.append("Please register first")
        elif len(form['pass']) < 5:
            errors.append("Password must have at least 5 characters.")
        else:
            user = User.objects.filter(email=form['email'])
            if not bcrypt.checkpw(form['pass'].encode(), user[0].password.encode()):
                errors.append("Sorry, password does not match our records.")

        if not errors:
            return (True, user[0])
        else:
            return (False, errors)

class QuoteValidator(models.Manager):

    def quoteValidator(self, form, user_id):
        errors = []

        if not form['author']:
            errors.append('Author is required')
        if len(form['author']) < 3:
            errors.append('Author name needs to be more than 3 characters')
        if not form['message']:
            errors.append('"Message" is required')
        if len(form['message']) < 3:
            errors.append('The "Message" needs to be more than 10 characters')

        if not errors:
            poster = User.objects.get(id=user_id)
            quote = Quote.objects.create(author=form['author'], message=form['message'], poster=poster)

            return (True, quote)
        else:
            return (False, errors)



class User(models.Model):
    name = models.CharField(max_length=15)
    alias = models.CharField(max_length=15)
    email = models.CharField(max_length=15)
    bday = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # joins (connets our Trip model with out User model through our Join table)
    # trips (connects our Trip model with our User model (Trip table)
    def __repr__(self):
        return "<User {} | {} | {} {}>".format(self.id, self.name, self.alias, self.email)

    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=10)
    message = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    poster = models.ForeignKey(User, related_name="posts")
    booker = models.ManyToManyField(User, related_name="favoritequotes")

   
    def __repr__(self):
        return "<Quote {} | {} | {} {}>".format(self.id, self.author, self.message, self.poster) 
        
    objects = QuoteValidator()
