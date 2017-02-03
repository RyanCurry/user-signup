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
import webapp2
import cgi
import re

Header="""
<!DOCTYPE html>
<html>

<head>
    <title>Signup</title>
    <style type="text/css">
        .error{
            color: red;
            display:inline;
            }


            label
            {
            display:inline-block;
            width:150px;
            margin-right:10px;
            text-align:right;
            }


        </style>
</head>
<body>
<h1>Signup</h1>
"""


Footer="""
</body>
</html>
"""


SignUpForm="""
        <form method="post">
            <label>Username
                <input type="text" name="Username" value="{0}"/>
            </label> <h3 class="error">{1}</h3>
            <br> <br>
            <label>Password
                <input type="Password" name="Paswrd"/>
            </label> <h3 class="error">{2}</h3>
            <br> <br>
            <label>Confirm Password
                <input type="Password" name="Conpass"/>
            </label> <h3 class="error">{3}</h3>
            <br> <br>
            <label>Email (Optional)
                <input type="text" name="Email" value="{4}"/>
            </label> <h3 class="error">{5}</h3>
            <br> <br>
            <input type="submit" name="Continue" value="Continue">
        </form>
        """



def num_check(s):
    return any(i.isdigit() for i in s)


good_email=re.compile(r"[\S]+@+[\S]+.+[\S]$")
def email_check(email_to_check):
    return good_email.match(email_to_check)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("Username")
        email=self.request.get("Email")
        form1=SignUpForm.format(username,"","","",email,"")
        self.response.write(Header + form1 + Footer)

    def post(self):
        error1=""
        error2=""
        error3=""
        error4=""
        username=self.request.get("Username")
        email=self.request.get("Email")
        pass1=self.request.get("Paswrd")
        passcon=self.request.get("Conpass")

        if not username or username == "":
            error1="Enter a Username"
        elif " " in username:
            error1="Invalid Username: must not contain spaces"
        elif len(username)<=3:
            error1="Invalid Username: must be at least 4 characters long"


        if not pass1 or pass1.strip =="":
            error2="Enter a Password"
        elif " " in pass1:
            error2="Invalid Password"
        elif len(pass1)<8:
            error2="Invalid Password: must be least 8 characters long"
        elif not num_check(pass1):
            error2="Invalid Password: must contain a number"
        elif pass1 != passcon:
            error3 = "Passwords didn't match"

        #if email and not("@" in email or "."in email):
        if email and not email_check(email):
            error4="Enter a valid email address"


        if error1 or error2 or error3 or error4:
            form1=SignUpForm.format(username,error1,error2,error3,email,error4)
            self.response.out.write(Header + form1 + Footer)
        else:
            self.redirect("/Welcome?Username="+username)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        name=self.request.get("Username")

        escaped_name=cgi.escape(name)
        self.response.write("<h1>Welcome, {0}!</h1>".format(escaped_name))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome',WelcomeHandler)
], debug=True)
