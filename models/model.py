__author__ = 'ISP-PC'

from google.appengine.ext import ndb

class EmployeeDB(ndb.Model):
        firstname = ndb.StringProperty(default='empty')
        lastname = ndb.StringProperty(default='empty')
        email = ndb.StringProperty()
        idno = ndb.IntegerProperty(default=0)
        phone = ndb.StringProperty(default='empty')
        hiredate = ndb.StringProperty(default='empty')
        job = ndb.StringProperty(default='empty')
        type = ndb.StringProperty(default='empty')
        privilege = ndb.StringProperty(default='user')



class LeaveDB(ndb.Model):
        year = ndb.IntegerProperty(default=1990)
        days = ndb.IntegerProperty(default=0)
        email = ndb.StringProperty()
        datefrom = ndb.DateProperty(auto_now_add=True)
        dateto = ndb.DateProperty(auto_now_add=True)
        approvedby= ndb.StringProperty(default='waiting...')
        dateapproved = ndb.DateTimeProperty()
        leavetype = ndb.StringProperty(default='null')
        leavestatus = ndb.StringProperty(default='Pending')
        reason = ndb.StringProperty(default='null')
        name = ndb.StringProperty(default='null')

class JobDB(ndb.Model):
        title = ndb.StringProperty(default='empty')
        description = ndb.StringProperty(default='empty')

class LeaveTypeDB(ndb.Model):
        type = ndb.StringProperty(default='empty')
        duration = ndb.IntegerProperty(default=0)
        description = ndb.StringProperty(default='empty')

class HoliDayDB(ndb.Model):
        date = ndb.DateProperty()
        name = ndb.StringProperty(default='Public')
        kind = ndb.StringProperty(default='yearly')