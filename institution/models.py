from django.db import models
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.
class Institution(models.Model):
    code = models.CharField(max_length=100,blank=True,null=True,verbose_name='Institution Code')
    name = models.CharField(max_length=255,blank=True,null=True,verbose_name='Institution Name')
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    email = models.EmailField(max_length=50,blank=True,null=True,verbose_name='Email Address')
    logo = models.ImageField(upload_to='institution/',blank=True,null=True,verbose_name='Institution Logo')
    short_address = models.TextField(blank=True,null=True,verbose_name='Short Address')
    address = models.TextField(blank=True,null=True,verbose_name='Address')
    site_link = models.URLField(max_length=255, blank=True,null=True,verbose_name='Website')
    map_link = models.URLField(max_length=255,blank=True,null=True,verbose_name='Map Address')
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='institution_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='institution_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inst_institution'
        verbose_name = '1. Institution'

    def __str__(self):
        return self.name

class Branch(models.Model):
    code = models.CharField(max_length=100,blank=True,null=True,verbose_name='Branch Code')
    name = models.CharField(max_length=255,blank=True,null=True,verbose_name='Branch Name')
    mobile_no = models.CharField(max_length=11,blank=True,null=True,verbose_name='Mobile No')
    email = models.EmailField(max_length=50,blank=True,null=True,verbose_name='Email Address')
    short_address = models.TextField(blank=True,null=True,verbose_name='Short Address')
    address = models.TextField(blank=True,null=True,verbose_name='Address')
    map_link = models.URLField(max_length=255,blank=True,null=True,verbose_name='Map Address')
    institution = models.ForeignKey(Institution,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_by = UserForeignKey(auto_user_add=True, on_delete=models.SET_NULL,related_name='branch_creator', editable=False, blank=True, null=True)
    updated_by = UserForeignKey(auto_user=True, on_delete=models.SET_NULL, related_name='branch_update_by', editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inst_branch'
        verbose_name = '2. Branch'

    def __str__(self):
        return self.name