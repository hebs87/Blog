# Generated by Django 3.2.7 on 2021-09-11 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AddField(
            model_name='comment',
            name='categories',
            field=models.ManyToManyField(to='main.Category'),
        ),
    ]
