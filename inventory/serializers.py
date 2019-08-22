from rest_framework import serializers
from inventory.models import Category, BooksInventory, BookImages
import uuid

from rest_framework.serializers import(
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.authtoken.models import Token

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
class BookImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImages
        fields = '__all__'

class BooksInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksInventory
        fields = '__all__'

class GetBooksInventorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = BooksInventory
        fields = ['id','title', 'author', 'isbn', 'publisher','price', 'publish_date', 'no_of_stock', 'image', 'image_url', 'category']
    
    def get_image_url(self, book):
        request = self.context.get('request')
        if book.image:
            image_url = book.image.url
            return request.build_absolute_uri(image_url)
   

#login and register
class UserCreateSerializer(ModelSerializer):
    first_name = CharField(allow_blank = False, required = True)
    last_name = CharField(allow_blank = False, required = True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password',]

        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email = email)
        if user_qs.exists():
            raise ValidationError("Email already exixts!!")
        return data
    

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = "{}_{}_{}".format(first_name, last_name, uuid.uuid4())
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
        )
        user_obj.set_password(password)
        user_obj.save()
        token = Token.objects.create(user=user_obj)
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank = True, read_only = True)
    email =EmailField(allow_blank = False, required = True)
    class Meta:
        model = User
        fields = ['email', 'password','token']

        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data['password']
        if not email:
            raise ValidationError("email is required")
        
        user = User.objects.filter(email=email).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() ==1:
            user_obj=user.first()
        else:
            raise ValidationError("email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials")
        token = Token.objects.get_or_create(user=user_obj)
        data["token"] ="Token {}".format(token[0])
        return data