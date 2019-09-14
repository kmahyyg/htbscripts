#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

# Get Data From ldaptools/ldaptools.git@GitHub

r = requests.get('https://github.com/ldaptools/ldaptools/blob/master/docs/en/reference/Default-Schema-Attributes.md')
soup = BeautifulSoup(r.text, features="lxml")
tables = soup.find_all('table')
all_attrs = []

dictf = open('common_ldap_attr.dic', 'w')

for each_table in tables:
    all_rows_have_contents = each_table.find('tbody').find_all('tr')
    for each_row in all_rows_have_contents:
        row_contents = each_row.find_all('td')[:2]
        for data in row_contents:
            data_inside = data.text.strip() + "\n"
            all_attrs.append(data_inside)


# Grabbed from Some Script from Web

web1_attrs = ["buildingname", "c", "cn", "co", "comment", "commonname", "company", "description", "distinguishedname",
              "dn", "department", "displayname", "facsimiletelephonenumber", "fax", "friendlycountryname", "givenname",
              "homephone", "homepostaladdress", "info", "initials", "ipphone", "l", "mail", "mailnickname",
              "rfc822mailbox", "mobile", "mobiletelephonenumber", "name", "othertelephone", "ou", "pager",
              "pagertelephonenumber", "physicaldeliveryofficename", "postaladdress", "postalcode", "postofficebox",
              "samaccountname", "serialnumber", "sn", "surname", "st", "stateorprovincename", "street", "streetaddress",
              "telephonenumber", "title", "uid", "url", "userprincipalname", "wwwhomepage"]
for data in web1_attrs:
    all_attrs.append(data)


# Get Data from BMC

r2 = requests.get('https://docs.bmc.com/docs/fpsc121/ldap-attributes-and-associated-fields-495323340.html')
soup2 = BeautifulSoup(r2.text, features='lxml')
tables2 = soup2.select('#main-content > div > div > div:nth-child(9) > table')[0]
all_rows_have_contents = tables2.find('tbody').find_all('tr')[1:]
try:
    for each_row in all_rows_have_contents:
        row_contents = each_row.find_all('td')[0]
        data_inside = row_contents.text.strip() + "\n"
        all_attrs.append(data_inside)
except:
    pass


all_attrs = set(all_attrs)
dictf.writelines(all_attrs)
dictf.flush()
dictf.close()
