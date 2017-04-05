# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 13:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lbattachment', '0002_auto_20170401_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=255, verbose_name='Code')),
                ('step', models.IntegerField(default=0, verbose_name='Step')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('given up', 'Given up'), ('rejected', 'Rejected'), ('in progress', 'In Progress'), ('completed', 'Completed')], default='in progress', max_length=16, verbose_name='Type')),
                ('audit_page_type', models.CharField(choices=[('view', 'view'), ('edit', 'Edit')], default='view', help_text='If this activity can edit, will auto goto edit mode when audit.', max_length=64, verbose_name='Audit page type')),
                ('can_edit', models.BooleanField(default=False, verbose_name='Can edit')),
                ('can_reject', models.BooleanField(default=True, verbose_name='Can reject')),
                ('can_give_up', models.BooleanField(default=True, verbose_name='Can give up')),
                ('operators', models.TextField(blank=True, verbose_name='Audit users')),
                ('notice_users', models.TextField(blank=True, verbose_name='Notice users')),
                ('share_users', models.TextField(blank=True, verbose_name='Share users')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('ext_data', jsonfield.fields.JSONField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(help_text='Name', max_length=100)),
                ('app_type', models.CharField(choices=[('url', 'URL')], default='url', max_length=255, verbose_name='Type')),
                ('action', models.CharField(blank=True, help_text="URL: It can be url or django's url name. If it's blank will use transition's app param", max_length=255)),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_on', models.DateField(verbose_name='Start on')),
                ('end_on', models.DateField(verbose_name='End on')),
                ('agent_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_user_authorizations', to=settings.AUTH_USER_MODEL, verbose_name='Agent user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('ext_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('attachments', models.ManyToManyField(blank=True, to='lbattachment.LBAttachment', verbose_name='Attachment')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_type', models.CharField(choices=[('transition', 'Transition'), ('edit', 'Edit'), ('give up', 'Give up'), ('reject', 'Reject'), ('back to', 'Back to'), ('rollback', 'Rollback'), ('comment', 'Comment'), ('assign', 'Assign'), ('hold', 'Hold'), ('unhold', 'Unhold')], default='transition', max_length=255)),
                ('comment', models.TextField(blank=True, default='')),
                ('ext_data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('attachments', models.ManyToManyField(blank=True, to='lbattachment.LBAttachment', verbose_name='Attachment')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='A unique code to identify process', max_length=100, unique=True, verbose_name='Code')),
                ('prefix', models.CharField(blank=True, default='', help_text='prefix for process NO.', max_length=8, verbose_name='Prefix')),
                ('name', models.CharField(help_text='Name for this process', max_length=255, verbose_name='Name')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('oid', models.IntegerField(default=999, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('ext_data', jsonfield.fields.JSONField(default='{}')),
            ],
            options={
                'verbose_name': 'Process',
                'ordering': ['oid'],
                'permissions': (('sft_mgr_process', 'workflow - Config'),),
            },
        ),
        migrations.CreateModel(
            name='ProcessCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('oid', models.IntegerField(default=999, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
            ],
            options={
                'ordering': ['oid'],
            },
        ),
        migrations.CreateModel(
            name='ProcessInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(blank=True, max_length=100, verbose_name='NO.')),
                ('object_id', models.PositiveIntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('submit_on', models.DateTimeField(blank=True, null=True)),
                ('end_on', models.DateTimeField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, verbose_name='Summary')),
                ('attachments', models.ManyToManyField(blank=True, to='lbattachment.LBAttachment')),
                ('can_view_users', models.ManyToManyField(blank=True, related_name='can_view_pinstances', to=settings.AUTH_USER_MODEL, verbose_name='Can view users')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instances', to=settings.AUTH_USER_MODEL)),
                ('cur_activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbworkflow.Activity')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.Process')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessReportLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('open_in_new_window', models.BooleanField(default=False, verbose_name='Open in new window')),
                ('perm', models.CharField(blank=True, help_text='Permission to view this report', max_length=255, verbose_name='Permission')),
                ('oid', models.IntegerField(default=999, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbworkflow.ProcessCategory', verbose_name='Category')),
            ],
            options={
                'ordering': ['oid'],
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(default='Agree', help_text="It also the action's name, like: Agree/Submit", max_length=100, verbose_name='Name')),
                ('code', models.CharField(blank=True, max_length=100, verbose_name='Code')),
                ('is_agree', models.BooleanField(default=True, help_text='User only need agree one time in one workflow', verbose_name='Is agree')),
                ('can_auto_agree', models.BooleanField(default=True, help_text='If user agreed in previous steps will auto agree', verbose_name='If can auto agree')),
                ('routing_rule', models.CharField(choices=[('split', 'split'), ('joint', 'Joint')], default='split', help_text='joint: do transition after all work item finished. joint: do transition immediately', max_length=16, verbose_name='Routing rule')),
                ('app_param', models.CharField(blank=True, help_text='Depend on App config', max_length=100, null=True, verbose_name='Param for application')),
                ('condition', models.TextField(blank=True, help_text='Uses the Python syntax.ex: `o.leave_days>3`', verbose_name='Condition')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('oid', models.IntegerField(default=999, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('ext_data', jsonfield.fields.JSONField(default='{}')),
                ('app', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbworkflow.App', verbose_name='Application to perform')),
                ('input_activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='input_transitions', to='lbworkflow.Activity', verbose_name='Input activity')),
                ('output_activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='output_transitions', to='lbworkflow.Activity', verbose_name='Output activity')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.Process', verbose_name='Process')),
            ],
        ),
        migrations.CreateModel(
            name='WorkItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed')], default='in progress', max_length=255)),
                ('receive_on', models.DateTimeField(blank=True, null=True, verbose_name='Receive on')),
                ('is_hold', models.BooleanField(default=False, verbose_name='Is hold')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.Activity')),
                ('agent_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_user_workitems', to=settings.AUTH_USER_MODEL, verbose_name='Agent user')),
                ('authorization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbworkflow.Authorization', verbose_name='Authorization')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.ProcessInstance')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbworkflow.ProcessCategory', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='event',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.ProcessInstance'),
        ),
        migrations.AddField(
            model_name='event',
            name='new_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_events', to='lbworkflow.Activity'),
        ),
        migrations.AddField(
            model_name='event',
            name='next_operators',
            field=models.ManyToManyField(blank=True, related_name='audit_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='notice_users',
            field=models.ManyToManyField(blank=True, related_name='notice_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='old_activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='out_events', to='lbworkflow.Activity'),
        ),
        migrations.AddField(
            model_name='event',
            name='transition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbworkflow.Transition'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='workitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='lbworkflow.WorkItem'),
        ),
        migrations.AddField(
            model_name='comment',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.ProcessInstance'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='processes',
            field=models.ManyToManyField(to='lbworkflow.Process', verbose_name='Processes'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authorized_user_authorizations', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='activity',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbworkflow.Process', verbose_name='Process'),
        ),
    ]
