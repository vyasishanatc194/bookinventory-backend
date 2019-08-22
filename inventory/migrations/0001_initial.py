# Generated by Django 2.2.4 on 2019-08-19 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='BooksInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='Book Title')),
                ('author', models.CharField(max_length=128, verbose_name='Book Author')),
                ('isbn', models.CharField(max_length=128, verbose_name='Book ISBN')),
                ('publisher', models.CharField(max_length=128, verbose_name='Book Publisher')),
                ('publish_date', models.DateField(verbose_name='Book Publish Date')),
                ('no_of_stock', models.IntegerField(default=0, verbose_name='Number Of Books in Stock')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Category', verbose_name='Book Category')),
            ],
            options={
                'verbose_name': 'Books Inventory',
                'verbose_name_plural': 'Books Inventory',
            },
        ),
        migrations.CreateModel(
            name='BookImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.BooksInventory', verbose_name='Book Inventory')),
            ],
            options={
                'verbose_name': 'Book Images',
                'verbose_name_plural': 'Book Images',
            },
        ),
    ]