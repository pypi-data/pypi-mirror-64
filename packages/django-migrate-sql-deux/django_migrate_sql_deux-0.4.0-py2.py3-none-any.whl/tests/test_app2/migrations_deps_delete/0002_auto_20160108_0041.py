# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import migrate_sql.operations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_auto_20160108_0048'),
        ('test_app2', '0001_initial'),
    ]

    operations = [
        migrate_sql.operations.ReverseAlterSQL(
            name='sale',
            sql='DROP TYPE sale',
            reverse_sql='CREATE TYPE sale AS (arg1 int); -- 1',
        ),
        migrate_sql.operations.AlterSQL(
            name='sale',
            sql='CREATE TYPE sale AS (arg1 int, arg2 int); -- 2',
            reverse_sql='DROP TYPE sale',
        ),
    ]
