# Generated by Django 2.2.1 on 2019-05-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_redirects', '0002_auto_20180910_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urllist',
            name='slack_sent',
        ),
        migrations.RemoveField(
            model_name='urllist',
            name='team',
        ),
        migrations.AddField(
            model_name='urllist',
            name='protocol',
            field=models.CharField(choices=[('both', 'BOTH'), ('https', 'HTTPS'), ('http', 'HTTP')], default='both', max_length=5),
        ),
    ]