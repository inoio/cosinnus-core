# Generated by Django 2.1.5 on 2019-05-29 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cosinnus', '0048_auto_20190529_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastvisitedobject',
            name='portal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='cosinnus.CosinnusPortal', verbose_name='Portal'),
        ),
    ]
