# Generated by Django 4.2.16 on 2024-12-04 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_alter_card_description_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='description',
            field=models.CharField(max_length=800),
        ),
    ]
