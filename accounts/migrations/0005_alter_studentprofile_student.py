# Generated by Django 3.2.3 on 2021-05-28 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_studentprofile_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='student',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
            preserve_default=False,
        ),
    ]
