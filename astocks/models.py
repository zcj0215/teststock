from django.db import models
from accounts.models import Persons
from boards.models import Board

# Create your models here.

class LimitupType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

    def to_json(self):
        json_LimitupType = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return json_LimitupType

class StockLimitup(models.Model):
    pick_date = models.DateField(max_length=10,db_index=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    reasons = models.CharField(max_length=100,null=True)
    boards = models.ManyToManyField(Board, related_name="stocklimitups")
    short = models.CharField(max_length=100,null=True)
    ndperformance = models.CharField(max_length=50,null=True)
    tenday_limits = models.PositiveIntegerField(null=True)
    summary = models.TextField(max_length=1000,null=True)
    person = models.ForeignKey(Persons, related_name='stocklimitups',on_delete=models.CASCADE)
    types = models.ManyToManyField(LimitupType, related_name="stocklimitups")
    growth=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
    
class ChooseType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

    def to_json(self):
        json_ChooseType = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return json_ChooseType

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
    types = models.ManyToManyField(ChooseType, related_name="stockchooses")
    growth=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
    
class Stocks(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    boards = models.ManyToManyField(Board, related_name="stockses")
    growth=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    blockname=models.CharField(max_length=50,null=True)
    committee=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    nf = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    market_value = models.CharField(max_length=50,null=True)
    circulation_market_value = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name
    
class StockList(models.Model):
    ts_code = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10, unique=True,db_index=True)
    name = models.CharField(max_length=50, unique=True)
    area = models.CharField(max_length=50,null=True)
    industry = models.CharField(max_length=50,null=True)
    list_date = models.CharField(max_length=50)
    market_value = models.CharField(max_length=50,null=True)
    circulation_market_value = models.CharField(max_length=50,null=True)
    
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
    capital_inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)     # 主力资金净流入
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True) 
    nf = models.DecimalField(max_digits=15, decimal_places=2,null=True)    # 北向资金净流入
    committee = models.DecimalField(max_digits=10, decimal_places=2,null=True) # 委比
    

    def __str__(self):
        return self.code
    
class Stockszc(models.Model):
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
    capital_inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True) 
    nf = models.DecimalField(max_digits=15, decimal_places=2,null=True) 
    committee = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.code
    
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
    capital_inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True)  
    nf = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    committee = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.code
    
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
    capital_inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True) 
    nf = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    committee = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.code
       
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
    capital_inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True) 
    nf = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    committee = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return self.code
    
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
        return self.code
    
class Stocksector(models.Model):
    code = models.CharField(max_length=11, db_index=True)                        
    open = models.DecimalField(max_digits=11, decimal_places=2)
    high = models.DecimalField(max_digits=11, decimal_places=2)
    close = models.DecimalField(max_digits=11, decimal_places=2)
    pre_close = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=11, decimal_places=2)
    volume = models.DecimalField(max_digits=18, decimal_places=2)
    turnover = models.DecimalField(max_digits=10, decimal_places=2,null=True)  
    volume_ratio=models.DecimalField(max_digits=10, decimal_places=2,null=True) 
    limitup_number=models.DecimalField(max_digits=5, decimal_places=0,null=True) 
    growth=models.DecimalField(max_digits=10, decimal_places=2,null=True)  
    growth_pre=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    growth_3=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    growth_fall=models.CharField(max_length=50,db_index=True,null=True)  # 上涨数，下跌数
    Continuerise_30_limitup=models.DecimalField(max_digits=5, decimal_places=0,null=True)  # 连续30天涨停数量
    Continuerise_days=models.DecimalField(max_digits=5, decimal_places=0,null=True) 
    date = models.DateField(max_length=10,db_index=True,null=True)
    name = models.CharField(max_length=50,db_index=True,null=True)
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True) 
    inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)     # 主力资金净流入
    
    def __str__(self):
        return self.name
    
    def thirty_limitup(self):
        
        return 
    
    
class Stockindex(models.Model):
    code = models.CharField(max_length=11, db_index=True) 
    name = models.CharField(max_length=50,db_index=True,null=True)                      
    open = models.DecimalField(max_digits=11, decimal_places=2)
    high = models.DecimalField(max_digits=11, decimal_places=2)
    close = models.DecimalField(max_digits=11, decimal_places=2)
    low = models.DecimalField(max_digits=11, decimal_places=2)
    volume = models.DecimalField(max_digits=18, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    price_change = models.DecimalField(max_digits=7, decimal_places=2)      # 涨跌额
    growth = models.DecimalField(max_digits=10, decimal_places=2,null=True)   # 涨幅
    amplitude = models.DecimalField(max_digits=10, decimal_places=2,null=True)   # 振幅
    date = models.DateField(max_length=10,db_index=True,null=True)
    pe = models.DecimalField(max_digits=7, decimal_places=2,null=True) 
    
    
class Indexinflow(models.Model):
    code = models.CharField(max_length=11, db_index=True) 
    name = models.CharField(max_length=50,db_index=True,null=True) 
    inf =  models.DecimalField(max_digits=15, decimal_places=2,null=True)     # 流入
    outf =  models.DecimalField(max_digits=15, decimal_places=2,null=True)    # 流出
    inflow = models.DecimalField(max_digits=15, decimal_places=2,null=True)   # 主力资金净流入
    date = models.DateField(max_length=10,db_index=True,null=True)
    growth=models.DecimalField(max_digits=10, decimal_places=2,null=True)  
