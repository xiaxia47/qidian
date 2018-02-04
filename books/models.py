# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import timedelta

 
class Book(models.Model):
    book_id = models.CharField(primary_key=True, max_length=12)
    book_type = models.CharField(max_length=2)
    book_sub_type = models.CharField(max_length=4)
    book_name = models.CharField(max_length=30)
    book_url = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    total_words = models.IntegerField(blank=True, null=True)
    click_count = models.IntegerField(blank=True, null=True)
    recommand_count = models.IntegerField(blank=True, null=True)
    book_status = models.CharField(max_length=2)
    rank_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    rank_ppl_involved = models.IntegerField(blank=True, null=True)
    last_upload_date = models.DateTimeField()
    last_update_date = models.DateTimeField(blank=True, null=True,auto_now=True)

    #是否是最近刚更新的
    def was_published_recently(self):
        book_flag = (self.last_upload_date >= (timezone.now() - timedelta(days=1)))
        return self.last_upload_date if book_flag is False else "刚刚更新"

    changed_tag = property(was_published_recently)

    class Meta:
        db_table = 'qidian'

