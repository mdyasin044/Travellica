# Generated by Django 3.1.4 on 2020-12-17 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0004_auto_20201216_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewimages',
            name='review_location',
            field=models.CharField(default='barisal', max_length=40),
            preserve_default=False,
        ),
    ]
