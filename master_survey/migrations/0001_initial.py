# Generated by Django 4.2.2 on 2023-08-03 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=128, verbose_name='Nama Survei')),
                ('deskripsi', models.TextField(verbose_name='Deskripsi Survei')),
                ('tgl_mulai', models.DateField(verbose_name='Tanggal Mulai')),
                ('tgl_selesai', models.DateField(verbose_name='Tanggal Berakhir')),
                ('status', models.CharField(choices=[('0', 'Aktif'), ('1', 'Non Aktif')], default=0, max_length=1, verbose_name='Status Survei')),
            ],
        ),
    ]
