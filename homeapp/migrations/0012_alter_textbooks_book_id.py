# Generated by Django 4.2.7 on 2023-11-27 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0011_alter_classname_classname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textbooks',
            name='book_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
