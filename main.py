#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2,jinja2,os,re,datetime
from google.appengine.api import mail,users
from models.model import EmployeeDB,HoliDayDB,LeaveDB,JobDB,LeaveTypeDB




template_path = os.path.join(os.path.dirname(__file__))

jinja2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

global activity
errors = []
edit = []
class MainHandler(webapp2.RequestHandler):
    def get(self):
        global activity
        #Activity
        activity = self.request.get('activity')

        user = users.get_current_user()
        if user:
            usermail =user.email()
            employees = EmployeeDB.query()
            emp = employees.count()
            leavetype = LeaveTypeDB.query()
            job = JobDB.query()
            if emp > 0:
                thisuser = EmployeeDB.query(EmployeeDB.email==usermail)
                if thisuser:
                    self.redirect('/leave')
                else:
                    self.redirect('/register')
            else:
                #Activity
                activity = self.request.get('activity','leave')
                if activity == 'job':
                    activity = 'job'
                if activity == 'employee':
                    activity = 'employee'
                if activity == 'leave':
                    activity == 'leave'

                template_values = {
                    'job':job,
                    'employees':employees,
                    'activity':activity,
                    'leavetype':leavetype
                }

                notification = self.request.get('notification')
                if notification:
                    template_values['notification'] = notification
                self.response.set_status(200)
                template = jinja2_env.get_template('templates/home.html')
                self.response.out.write(template.render(template_values))

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        #New employee
        newemployee = self.request.get('newemployee')
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        idno = self.request.get('idno')
        phone = self.request.get('phone')
        hiredate = self.request.get('hiredate')
        #email = self.request.get('email')
        job = self.request.get('job')
        type = self.request.get('type')

        #New job title
        newjob = self.request.get('newjob')
        title = self.request.get('title')
        description = self.request.get('description')

        #New leave type
        newleavetype = self.request.get('newleavetype')
        leavetype = self.request.get('leavetype')
        leaveduration = self.request.get('leaveduration')
        leavedescription = self.request.get('leavedescription')

        if newemployee == 'true':
            employee = EmployeeDB(

                    firstname = str(firstname),
                    lastname = str(lastname),
                    idno = int(idno),
                    phone = str(phone),
                    hiredate = str(hiredate),
                    email = str(users.get_current_user().email()),
                    job = str(job),
                    type = str(type),
                    privilege = 'admin'
            )

            employee.put()

            self.redirect('/hr')

        if newjob == 'true':
            job = JobDB(
                title = str(title),
                description = str(description)
            )
            job.put()

            self.redirect('/?activity=job')

        if newleavetype == 'true':
            type = LeaveTypeDB(
                type = str(leavetype),
                duration = int(leaveduration),
                description = str(leavedescription)
            )
            type.put()

            self.redirect('/?activity=leave')



class HrHandler(webapp2.RequestHandler):
    def get(self):
        global edit

        dfhractivity = 'pending'
        hractivity = self.request.get('hractivity',dfhractivity)

        if hractivity == 'pending':
            hractivity = 'pending'
        elif hractivity == 'employee':
            hractivity = 'employee'
        elif hractivity == 'job':
            hractivity = 'job'
        elif hractivity == 'holiday':
            hractivity = 'holiday'
        elif hractivity == 'leave':
            hractivity = 'leave'
        else:
            hractivity = 'pending'

        if users.get_current_user():
            user = str(users.get_current_user().email())
            if user :
                thisyear = datetime.datetime.now()
                dfyr = thisyear.year #get default year from current year
                year = int(self.request.get('yearpicker',dfyr))
                leave = LeaveDB.query(LeaveDB.year==year).order(-LeaveDB.datefrom)
                employee = EmployeeDB.query().order(-EmployeeDB.hiredate)
                thisuser =EmployeeDB.query(EmployeeDB.email==user,EmployeeDB.privilege=='admin').get()
                if thisuser:
                    leavetype = LeaveTypeDB.query()
                    job = JobDB.query()
                    holiday = HoliDayDB.query()

                    template_values = {
                        'year':year,
                        'holiday':holiday,
                        'employee':employee,
                        'job':job,
                        'thisuser':thisuser,
                        'leave':leave,
                        'leavetype':leavetype,
                        'hractivity':hractivity
                    }

                    notification = self.request.get('notification')
                    if notification:
                        template_values['notification'] = notification
                    self.response.set_status(200)
                    template = jinja2_env.get_template('templates/index.html')
                    self.response.out.write(template.render(template_values))
                else:
                    self.redirect('/leave')

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):

        user = str(users.get_current_user().email())
        thisuser =EmployeeDB.query(EmployeeDB.email==user,EmployeeDB.privilege=='admin').get()

        #Approve
        approve = (self.request.get('approve'))
        decline = (self.request.get('decline'))

        #New employee
        newemployee = self.request.get('newemployee')
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        idno = self.request.get('idno')
        phone = self.request.get('phone')
        hiredate = self.request.get('hiredate')
        email = self.request.get('email')
        job = self.request.get('job')
        type = self.request.get('type')
        privilege = self.request.get('privilege')

        #New job title
        newjob = self.request.get('newjob')
        title = self.request.get('title')
        description = self.request.get('description')

        #New holiday
        newholiday = self.request.get('newholiday')
        dth = self.request.get('holidate')
        kind = self.request.get('kind')
        name = self.request.get('name')

        #New leave type
        newleavetype = self.request.get('newleavetype')
        leavetype = self.request.get('leavetype')
        leaveduration = self.request.get('leaveduration')
        leavedescription = self.request.get('leavedescription')

        if newholiday == 'true':
            dateholi = datetime.datetime.strptime(dth,'%Y-%m-%d')
            holiday = HoliDayDB(
                date = dateholi,
                name = str(name),
                kind = str(kind)
            )
            holiday.put()
            self.redirect('/hr?hractivity=holiday')

        if newemployee == 'true':
            employee = EmployeeDB(

                    firstname = str(firstname),
                    lastname = str(lastname),
                    idno = int(idno),
                    phone = str(phone),
                    hiredate = str(hiredate),
                    email = str(email),
                    job = str(job),
                    type = str(type),
                    privilege = str(privilege)
            )

            employee.put()
            self.redirect('/hr?hractivity=employee')

        if newjob == 'true':
            job = JobDB(
                title = str(title),
                description = str(description)
            )
            job.put()
            self.redirect('/hr?hractivity=job')

        if newleavetype == 'true':
            type = LeaveTypeDB(
                type = str(leavetype),
                duration = int(leaveduration),
                description = str(leavedescription)
            )
            type.put()
            self.redirect('/hr?hractivity=leave')

        if approve or decline !=''  :
            st = 'error!'

            if approve !='':
                st = 'Approved'
            if decline !='':
                st = 'Declined'
            if st == 'Approved':
                x = LeaveDB.get_by_id(int(approve))
            elif st == 'Declined':
                x = LeaveDB.get_by_id(int(decline))
            x.leavestatus= st
            x.approvedby = thisuser.firstname
            x.dateapproved = datetime.datetime.now().replace(tzinfo=None)
            x.put()

            aplicantmail = x.email
            user = users.get_current_user().email()
            message = mail.EmailMessage(sender="ISP leave request approval <leave@ispleave.appspotmail.com>",
                                        subject="LEAVE REQUEST APPROVAL - STATUS")

            message.to = aplicantmail
            message.body = """
                    ISPEER,

                    Your request approval status.

                    Approved by: %s
                    leavetype: %s
                    Days.: %s
                    From : %s
                    To : %s
                    Reason: %s

                    Request %s %s

                    http://leave.intellisoftplus.com/history

                    """ % (thisuser.firstname,x.leavetype,x.days,x.datefrom.strftime('%d-%B-%Y'),x.dateto.strftime('%d-%B-%Y'),x.reason,st,x.dateapproved)

            message.send()
            self.redirect('/hr')

class LeaveHandler(webapp2.RequestHandler):
    def get(self):
        global errors
        leavestaken = []
        year = datetime.datetime.now()
        dfyr = year.year #get default year from current year
        year = self.request.get('year',dfyr)
        if users.get_current_user():
            user = str(users.get_current_user().email())
            if user :
                thisuser = EmployeeDB.query(EmployeeDB.email==user).get()
                if thisuser:
                    leavetype = LeaveTypeDB.query()

                    for x in leavetype:
                        select = LeaveDB.query(LeaveDB.leavetype == x.type,LeaveDB.email == thisuser.email,LeaveDB.year == year,LeaveDB.leavestatus == 'Approved')
                        i=0
                        l=x.type
                        d=x.duration
                        for y in select:
                            i += y.days
                        leavestaken.append(x)
                        x.type = l
                        x.days = i
                        x.duration = d


                    template_values = {
                        'errors':errors,
                        'year':year,
                        'thisuser':thisuser,
                        'leavestaken':leavestaken,
                        'leavetype':leavetype,
                    }

                    notification = self.request.get('notification')
                    if notification:
                        template_values['notification'] = notification
                    self.response.set_status(200)
                    template = jinja2_env.get_template('templates/leave.html')
                    self.response.out.write(template.render(template_values))
                else:
                    self.redirect('/')

            else:
                self.redirect(users.create_login_url(self.request.uri))

        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):

        global errors
        errors = []

        if users.get_current_user():
            user = str(users.get_current_user().email())
            if user :
                thisuser = EmployeeDB.query(EmployeeDB.email==user).get()
                if thisuser:
                    requestleave = self.request.get('requestleave')
                    year = self.request.get('year')
                    df = self.request.get('datefrom')
                    dt= self.request.get('dateto')
                    reason = self.request.get('reason')
                    email = thisuser.email
                    leavetype = self.request.get('leavetype')

                    if requestleave == 'true':
                        datefrom = datetime.datetime.strptime(df, '%Y-%m-%d')
                        dateto = datetime.datetime.strptime(dt, '%Y-%m-%d')
                        match = re.search('\d{4}', str(datefrom))
                        match2 = re.search('\d{4}', str(dateto))
                        year = match.group(0) if match else '2000'
                        year2 = match2.group(0) if match else '2001'

                        from_weekday = datefrom.weekday()
                        to_weekday = dateto.weekday()
                        # If start date is after Friday, modify it to Monday
                        if from_weekday > 5:
                            from_weekday = 0
                        day_diff = to_weekday - from_weekday
                        whole_weeks = ((dateto - datefrom).days - day_diff) / 7
                        workdays_in_whole_weeks = whole_weeks * 5
                        beginning_end_correction = min(day_diff, 5) - (max(dateto.weekday() - 4, 0) % 5)
                        wds = workdays_in_whole_weeks + beginning_end_correction

                        h = HoliDayDB.query()
                        if h.count() > 0:
                            holidays=0
                            for d in h:
                                hd = d.date
                                hdc = datetime.datetime.combine(hd, datetime.time(0, 0))
                                if (datefrom <= hdc <= dateto) and (hdc.weekday() != 6):
                                    holidays += 1
                        else:
                            holidays=0

                        working_days = wds-holidays

                        l = LeaveTypeDB.query(LeaveTypeDB.type == leavetype).get()
                        ld = l.duration
                        taken=0
                        gettaken = LeaveDB.query(LeaveDB.leavetype == leavetype,LeaveDB.email == thisuser.email,LeaveDB.year == int(year),LeaveDB.leavestatus == 'Approved')
                        for y in gettaken:
                            taken += y.days
                        rem = ld-taken

                        if datefrom>=dateto:
                            e = 'Date error! there should be atleast a 1 day difference in your selection'
                            errors.append(e)
                        if year != year2:
                            e = 'Year error! a single leave only affects a single calender year, you have selected 2'
                            errors.append(e)
                        if working_days>rem:
                            e = 'Days left error! You only have rem days left for leavetype, you just selected days.days days'
                            errors.append(e)

                        if (dateto>datefrom) and (year == year2) and (working_days<=rem) and (working_days>0):
                            request = LeaveDB(
                                year = int(year),
                                days = working_days,
                                datefrom = datefrom,
                                dateto = dateto,
                                reason = reason,
                                email = email,
                                name = thisuser.firstname,
                                leavetype = leavetype
                            )
                            request.put()

                            id = request.key.id()

                            Admin = EmployeeDB.query(EmployeeDB.privilege == 'admin')
                            for a in Admin:
                                adminmail = a.email
                                message = mail.EmailMessage(sender="ISP leave request <leave@ispleave.appspotmail.com>",
                                                            subject="NEW LEAVE REQUEST - REQUIRES ADMIN APPROVAL")

                                message.to = adminmail

                                message.body = """
                                """

                                message.html = """
                                <!DOCTYPE html>
                                <html lang="en">
                                <title>Leave mail</title>

                                <head>
                                      <meta charset="utf-8">
                                      <meta name="viewport" content="width=device-width, initial-scale=1">
                                      <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
                                      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
                                      <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
                                </head>

                                <body>

                                <div class="container">
                                  <div class="panel panel-primary">

                                       <div class="panel-heading">
                                         Hr/Admin, The below employee has requested for a leave.
                                        </div>

                                        <div class="panel-body">

                                                Name: %s %s <br/>
                                                leavetype: %s<br/>
                                                Days.: %s<br/>
                                                From : %s<br/>
                                                To : %s<br/>
                                                Reason: %s<br/>

                                        <form action="http://leave.intellisoftplus.com/hr" method="post">
                                            <button type="submit" name="approve" value="%s">Approve</button><br/>
                                            <button type="submit" name="decline" value="%s">Decline</button><br/>
                                        </form>

                                        Please reply.<br/>

                                        <br/>
                                        http://leave.intellisoftplus.com/hr
                                        </div>
                                  </div>
                                </div>
                                </body></html>
                                """ % (thisuser.firstname,thisuser.lastname,leavetype,working_days,datefrom.strftime('%d-%B-%Y'),dateto.strftime('%d-%B-%Y'),reason,id,id)

                                message.send()

                            self.redirect('/history')
                        else:
                            self.redirect('/leave')

                else:
                    self.redirect('/')
            else:
                self.redirect(users.create_login_url(self.request.uri))

        else:
            self.redirect(users.create_login_url(self.request.uri))



class HistoryHandler(webapp2.RequestHandler):
    def get(self):
        thisyear = datetime.datetime.now()
        dfyr = thisyear.year #get default year from current year
        year = int(self.request.get('yearpicker',dfyr))
        if users.get_current_user():
            user = str(users.get_current_user().email())
            if user :
                thisuser = EmployeeDB.query(EmployeeDB.email==user).get()
                if thisuser:
                    leave = LeaveDB.query(LeaveDB.email == thisuser.email, LeaveDB.year == year)

                    template_values = {
                        'thisuser':thisuser,
                        'leave':leave,
                        'year':year
                    }

                    notification = self.request.get('notification')
                    if notification:
                        template_values['notification'] = notification
                    self.response.set_status(200)
                    template = jinja2_env.get_template('templates/history.html')
                    self.response.out.write(template.render(template_values))
                else:
                    self.redirect('/')

            else:
                self.redirect('/')

        else:
            self.redirect(users.create_login_url(self.request.uri))

class Register(webapp2.RequestHandler):
    def get(self):

        template_values = {

            }

        notification = self.request.get('notification')
        if notification:
            template_values['notification'] = notification
        self.response.set_status(200)
        template = jinja2_env.get_template('templates/register.html')
        self.response.out.write(template.render(template_values))

class Edit(webapp2.RequestHandler):
    def post(self):
        global edit
        id = self.request.get('edit')
        edit = EmployeeDB.get_by_id(int(id))

        self.redirect('/hr?hractivity=employee')


class TryCode(webapp2.RequestHandler):
    def get(self):

        template_values = {

            }

        notification = self.request.get('notification')
        if notification:
            template_values['notification'] = notification
        self.response.set_status(200)
        template = jinja2_env.get_template('templates/try.html')
        self.response.out.write(template.render(template_values))



class LogOut(webapp2.RequestHandler):
    def get(self):

            user = users.get_current_user()
            if user:
                sign = ('Click to sign out, %s! (<a href="%s">sign out</a>)' %
                            (user.nickname(), users.create_logout_url('/')))
            else:
                sign = ('<a href="%s">Sign in </a>.' %
                            users.create_login_url('/'))

            self.response.out.write("<html><body>%s</body></html>" % sign)

class LogIn(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            usermail = user.email()
            thisuser = EmployeeDB.query(EmployeeDB.email==usermail)
            if thisuser:
                self.redirect('/leave')
            else:
                self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class autolog(webapp2.RequestHandler):
    def get(selfself):
        users.create_logout_url('/register')




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/leave', LeaveHandler),
    ('/hr',HrHandler),
    ('/login',LogIn),
    ('/logout',LogOut),
    ('/history',HistoryHandler),
    ('/register',Register),
    ('/auto',autolog),
    ('/try',TryCode),
    ('/edit',Edit),
], debug=True)
