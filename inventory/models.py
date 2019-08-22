from django.db import models

class ActivityTracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(ActivityTracking):
    name = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class BooksInventory(ActivityTracking):
    title = models.CharField(null=False, blank=False, verbose_name='Book Title', max_length=128)
    author = models.CharField(null=False, blank=False, verbose_name='Book Author', max_length=128)
    isbn = models.CharField(null=False, blank=False, verbose_name='Book ISBN', max_length=128)
    publisher = models.CharField(null=False, blank=False, verbose_name='Book Publisher', max_length=128)
    publish_date = models.DateField(blank=False, null=False, verbose_name='Book Publish Date')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Book Category')
    no_of_stock = models.IntegerField(null=False, blank=False, default=0, verbose_name='Number Of Books in Stock')
    price = models.FloatField(null=False, blank=False, verbose_name='Book Price', default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Books Inventory'
        verbose_name_plural = 'Books Inventory'

class BookImages(ActivityTracking):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    book = models.ForeignKey(BooksInventory, on_delete=models.CASCADE, verbose_name='Book Inventory')

    def __str__(self):
        return self.book.title
    
    class Meta:
        verbose_name = 'Book Images'
        verbose_name_plural = 'Book Images'




