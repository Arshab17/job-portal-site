# Generated by Django 4.1.7 on 2023-05-04 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_account', '0003_rename_edit_image_profile_details_profile_img'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_account.employee')),
                ('job_vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.job_vacancy')),
            ],
        ),
    ]
