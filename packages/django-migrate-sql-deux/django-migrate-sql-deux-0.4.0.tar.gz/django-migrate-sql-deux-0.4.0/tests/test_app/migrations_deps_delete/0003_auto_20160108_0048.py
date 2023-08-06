# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import migrate_sql.operations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20160106_0947'),
    ]

    operations = [
        migrate_sql.operations.ReverseAlterSQL(
            name='narration',
            sql='DROP TYPE narration',
            reverse_sql='CREATE TYPE narration AS (sale1 sale, book1 book, arg1 int); -- 1',
        ),
        migrate_sql.operations.CreateSQL(
            name='edition',
            sql='CREATE TYPE edition AS (arg1 int); -- 1',
            reverse_sql='DROP TYPE edition',
        ),
        migrate_sql.operations.ReverseAlterSQL(
            name='book',
            sql='DROP TYPE book',
            reverse_sql='CREATE TYPE book AS (arg1 int); -- 1',
        ),
    ]
