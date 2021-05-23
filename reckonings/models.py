# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Categories(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'categories'


class Exceptions(models.Model):
    exceptionid = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    reckoningpositionid = models.ForeignKey('Reckoningpositions', models.DO_NOTHING, db_column='reckoningpositionid')
    groupmemberid = models.ForeignKey('Groupmembers', models.DO_NOTHING, db_column='groupmemberid')

    class Meta:
        managed = False
        db_table = 'exceptions'


class Groupmembers(models.Model):
    groupmemberid = models.AutoField(primary_key=True)
    groupid = models.ForeignKey('Groups', models.DO_NOTHING, db_column='groupid')
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid')
    adddate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'groupmembers'


class Groups(models.Model):
    groupid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'groups'


class Reckoningpositions(models.Model):
    reckoningpositionid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    categoryid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='categoryid')
    groupmemberid = models.ForeignKey(Groupmembers, models.DO_NOTHING, db_column='groupmemberid',blank=True, null=True)
    reckoningid = models.ForeignKey('Reckonings', models.DO_NOTHING, db_column='reckoningid')
    paymentdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reckoningpositions'


class Reckonings(models.Model):
    reckoningid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startdate = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField()
    groupid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='groupid')
    author = models.ForeignKey(Groupmembers, models.DO_NOTHING, db_column='author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reckonings'


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
