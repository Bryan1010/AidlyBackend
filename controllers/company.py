from models.company import Company
from flask import json

def create_Company(comp):
    createdCompany = Company(**comp).save()
    id = createdCompany.id
    return id
    