from django.db import models


class Groupmembers(models.Model):
    groupmemberid = models.AutoField(primary_key=True)
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='roleid')
    adddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'groupmembers'


class Users(models.Model):
    userid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'


class Groups(models.Model):
    groupid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startdate = models.DateTimeField()
    members = models.ManyToManyField(Users, through='Groupmembers', through_fields=('groupid', 'userid'))

    class Meta:
        managed = False
        db_table = 'groups'


class Group(models.Model):
    groupid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'groups'


class Roles(models.Model):
    roleid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'