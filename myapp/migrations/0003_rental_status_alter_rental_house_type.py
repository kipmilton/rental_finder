# Generated by Django 5.1.6 on 2025-03-13 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rental_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='rental',
            name='house_type',
            field=models.CharField(choices=[('Bedsitter', 'Bedsitter'), ('Single Room', 'Single Room'), ('One Bedroom', 'One Bedroom'), ('Two Bedroom', 'Two Bedroom'), ('Three Bedroom', 'Three Bedroom'), ('Four Bedroom', 'Four Bedroom')], max_length=20),
        ),
    ]
