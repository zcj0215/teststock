from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Company
from ..add_companies_to_db import add_company

class FuncAddCompany2DB(TestCase):
    def test_add_company(self):
        """
        测试调用该方法，数据库成功添加了股票公司数据
        """
        companies = Company.objects.all()
        self.assertQuerysetEqual(companies,[])
        add_company()
        self.assertEquals(Company.objects.count(),10)
        self.assertEquals(Company.objects.first().stock_code,'600718')
        self.assertEquals(Company.objects.first().name,'东软集团')
        