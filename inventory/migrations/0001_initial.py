# Generated by Django 3.1 on 2021-07-27 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('qty', models.IntegerField(default=0)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.location')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('qty', models.IntegerField(default=0)),
                ('location_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_from', to='inventory.location')),
                ('location_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_to', to='inventory.location')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movement_products', to='inventory.product')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]