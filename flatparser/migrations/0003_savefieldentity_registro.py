# Generated by Django 2.2.2 on 2019-06-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatparser', '0002_distinctentity_savefieldentity_sumfieldentity_uniqueentity'),
    ]

    operations = [
        migrations.AddField(
            model_name='savefieldentity',
            name='registro',
            field=models.CharField(default='', max_length=200),
        ),
    ]