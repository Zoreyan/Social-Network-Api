# Generated by Django 3.2.12 on 2022-09-18 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_comment_options_alter_like_options_like_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preview',
            field=models.ImageField(default='no.svg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='main.post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='main.post'),
        ),
    ]
