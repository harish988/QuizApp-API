from django.db import models

#Department Model
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Department"

#Year Model
class Year(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Year"

#Section Model
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Section"

#User Model
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=100)
    department = models.ForeignKey(Department, verbose_name="department", on_delete=models.CASCADE)
    year = models.ForeignKey(Year, verbose_name="year", on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name="section", on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "User"