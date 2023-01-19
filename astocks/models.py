from django.db import models
from accounts.models import Persons
from boards.models import Board

# Create your models here.

class StockChoose(models.Model):
    pick_date = models.DateField(max_length=10,db_index=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    reasons = models.CharField(max_length=100,null=True)
    boards = models.ManyToManyField(Board, related_name="stockchooses")
    short = models.CharField(max_length=100,null=True)
    ndperformance = models.CharField(max_length=50,null=True)
    tenday_limits = models.PositiveIntegerField(null=True)
    summary = models.TextField(max_length=1000,null=True)
    person = models.ForeignKey(Persons, related_name='stockchooses',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class StockList(models.Model):
    ts_code = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10, unique=True,db_index=True)
    name = models.CharField(max_length=50, unique=True)
    area = models.CharField(max_length=50,null=True)
    industry = models.CharField(max_length=50,null=True)
    list_date = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Stocksz(models.Model):
    code = models.CharField(max_length=10, db_index=True)                        
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    pre_close = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)      # 涨跌额
    p_change = models.DecimalField(max_digits=7, decimal_places=2)          # 涨跌幅
    date = models.DateField(max_length=10,db_index=True)
    volume_ratio = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return self.name
    
class Stockszc(models.Model):
    code = models.CharField(max_length=10, db_index=True)                        
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    pre_close = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)
    p_change = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(max_length=10,db_index=True)
    volume_ratio = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
    
class Stocksh(models.Model):
    code = models.CharField(max_length=10, db_index=True)                        
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    pre_close = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)
    p_change = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(max_length=10,db_index=True)
    volume_ratio = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
    
class Stockshk(models.Model):
    code = models.CharField(max_length=10, db_index=True)                        
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    pre_close = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)
    p_change = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(max_length=10,db_index=True)
    volume_ratio = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
       
class Stockbj(models.Model):
    code = models.CharField(max_length=10, db_index=True)                        
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    pre_close = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)
    p_change = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(max_length=10,db_index=True)
    volume_ratio = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
    
class Stockme(models.Model):
    code = models.CharField(max_length=10, db_index=True)                        
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    pre_close = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)
    p_change = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(max_length=10,db_index=True)
    
    def __str__(self):
        return self.name
          
    