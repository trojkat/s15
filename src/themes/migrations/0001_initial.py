# Generated by Django 3.0.5 on 2020-04-30 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('domain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(choices=[('hyde', 'hyde'), ('poole', 'poole'), ('massively', 'massively')], max_length=50)),
                ('values', models.TextField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme_settings', to='domain.Site')),
            ],
            options={
                'unique_together': {('site', 'theme')},
            },
        ),
    ]
