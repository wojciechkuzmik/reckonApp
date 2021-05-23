from django.db import models


class Categories(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'categories'
    
    def __str__(self):
        return str(self.categoryid)


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

    def __str__(self):
        return str(self.groupmemberid)


class Groups(models.Model):
    groupid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startdate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'groups'
    
    def __str__(self):
        return str(self.groupid)


class Reckoningpositions(models.Model):
    reckoningpositionid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    categoryid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='categoryid')
    groupmemberid = models.ForeignKey('Groupmembers', models.DO_NOTHING, db_column='groupmemberid')
    reckoningid = models.ForeignKey('Reckonings', models.DO_NOTHING, db_column='reckoningid')

    class Meta:
        managed = False
        db_table = 'reckoningpositions'


class Reckonings(models.Model):
    reckoningid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startdate = models.DateTimeField(blank=True)
    deadline = models.DateTimeField(blank=True)
    groupid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='groupid')

    class Meta:
        managed = False
        db_table = 'reckonings'

    def __str__(self):
        return str(self.reckoningid)


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
