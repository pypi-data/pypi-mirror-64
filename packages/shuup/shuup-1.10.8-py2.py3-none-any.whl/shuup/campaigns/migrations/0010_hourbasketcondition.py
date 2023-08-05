# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-17 17:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0009_hourcondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourBasketCondition',
            fields=[
                ('basketcondition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='campaigns.BasketCondition')),
                ('hour_start', models.TimeField()),
                ('hour_end', models.TimeField()),
                ('days', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
            ],
            options={
                'abstract': False,
            },
            bases=('campaigns.basketcondition',),
        ),
    ]
