# Generated by Django 4.1.1 on 2022-10-02 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('capacity', models.IntegerField()),
                ('projector', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hall', to='conf_app.conferencehall')),
            ],
            options={
                'unique_together': {('date', 'hall')},
            },
        ),
    ]