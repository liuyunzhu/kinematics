#!/usr/bin/env python
import webapp2	# web application framework
import jinja2	# template engine
import os		# access file system
import datetime
import urllib
import cgi
import random
import math
from google.appengine.api import users	# Google account authentication
from google.appengine.ext import db		# datastore
from google.appengine.ext.webapp.util import run_wsgi_app
import cgitb
cgitb.enable()

i = 0
done = []
question = ['''A car is travelling with uniform acceleration along a straight road. The road has marker posts every 100m. </br>When the car passes one post, it has a speed of 10ms<sup>-1</sup> and, when it passes the second one, its speed is 20ms<sup>-1</sup>.</br> What is the car's acceleration?''',
'''A car is travelling at 10ms<sup>-1</sup>, it can come to a rest in a distance of 10m. </br> If it is travelling at 30ms<sup>-1</sup>, in what distance could it stop using the same braking force?''',
'''A ball is thrown vertically upwards and falls back to original position. </br>What is the acceleration of the ball at the maximum height?</br> Take upwards as positive and neglect air resistance.''',
'''Acceleration is the gradient of the __________ - time graph.''',
'''A ball is projected with a velocity of 40ms<sup>-1</sup> at an angle of 45 degrees to the horizontal. </br>What is its speed after 5.0s? Neglect air resistance.''',
'''A ball is dropped from rest over a bed of sand. It hits the sand bed one second later, and makes an impression of 8.0mm in the sand. </br> What is the average deceleration upon hitting the sand bed?</br> Neglect air resistance.''',
'''A rescue plane is flying horizontally with a speed of 30ms<sup>-1</sup> and at an altitude of 125m above the sea when it drops a warning flare. </br>Assuming that the plane does not change its course, speed or altitude, how far from the plane is the flare when it hits the water? </br>Neglect air resistance.''',
'''A tennis ball is projected with an initial speed of 10.0ms<sup>-1</sup> at an angle of 30 degrees towards a vertical wall located 10m away from the ball horizontally. </br> What is the final speed of the ball when it hits the wall?''',
'''A ball suspended from a string is set into oscillation. The string is cut when the ball passes through the lowest point of motion. </br> If the ball is then moving at a velocity of 0.8ms<sup>-1</sup> at a height of 5m above the ground, what is the horizontal distance traveled by the ball?''',
'''A car of mass 500kg, including driver but not the fuel, decelerates from 50ms<sup>-1</sup> to 30ms<sup>-1</sup>. </br>The retarding force exerted by the brakes is 70000N. </br> Take time for car to decelerate when it is almost out of fuel as t1, and the time for car to decelerate when it has full load of 130kg of fuel as t2.</br>Calculate (t2 - t1).''',
'''A trolley runs freely down a slope with constant acceleration a. </br> The mass of the trolley is now doubled and allowed to run down the same slope. </br>What is the acceleration in the second experiment?</br> Neglect air resistance and friction''',
'''A stone is thrown vertically downwards from the edge of a cliff with an initial speed of 18ms<sup>-1</sup>. It travels at 42ms<sup>-1</sup> just before hitting the ground. </br> If the stone is now thrown horizontally outwards from the top of the cliff with the same initial speed, what is its final speed immediately before hitting the ground?''']
shortsol = ['1.5','90','-9.81','displacement','35.1','6000','125','10.7','0.8','0.37','a','42']
solution = ['''using v<sup>2</sup> = u<sup>2</sup> + 2as</br>a=1.5ms<sup>-1</sup>''',
'''using v<sup>2</sup> = u<sup>2</sup> + 2as</br>a = -5ms<sup>-2</sup></br>In second case, using v<sup>2</sup> = u<sup>2</sup> + 2as</br>s = 90m''',
'''Accleration is constant at -9.81ms<sup>-2</sup>''',
'''displacement''',
'''using v<sub>y</sub> = u<sub>y</sub> + at</br> v<sub>y</sub>= -20.8ms<sup>-1</sup></br>v<sub>x</sub> = 28.3ms<sup>-1</sup></br>v=(v<sub>y</sub><sup>2</sup>+v<sub>x</sub><sup>2</sup>)<sup>0.5</sup>=35.1ms<sup>-1</sup>''',
'''Take downwards as positive</br>using v = u + at</br>v = 9.81ms<sup>-1</sup></br>using v<sup>2</sup> = u<sup>2</sup> + 2as</br>a = 6000ms<sup>-2</sup>''',
'''The flare travels at same horizontal speed as the plane throughout the journey. When the flare hits water, it is vertically under the plane and hence distance is 125m.''',
'''s<sub>x</sub> = u<sub>x</sub>t </br> t = 1.15s</br>v<sub>y</sub> = u<sub>y</sub> + at = -6.33ms<sup>-1</sup></br>v=(v<sub>y</sub><sup>2</sup>+v<sub>x</sub><sup>2</sup>)<sup>0.5</sup>=10.7ms<sup>-1</sup>''',
'''considering vertical direction, s = ut + <font class=num>1</font>&#x2044;<font class=denom>2</font>at<sup>2</sup></br>t = 1.0s</br>s<sub>x</sub> = 0.8m''',
'''using v = u + at and a = F/m</br>t<sub>1</sub> = 1.43s</br>t<sub>2</sub> = 1.80s</br> t<sub>2</sub> - t<sub>1</sub> = 0.37s''',
'''a''',
'''Take downwards as positive</br>using v<sup>2</sup> = u<sup>2</sup> + 2as</br> s = 72m</br> When dropped from 72m, using v<sup>2</sup> = u<sup>2</sup> + 2as</br> v = (0 + 2x10x72)<sup>0.5</sup> = 42ms<sup>-1</sup>''']
#solution is full solution, shortsol is for checking of ans
ques_index = [0,1,2,3,4,5,6,7,8,9,10,11]
correct = 0

linear = [ '''<h4>Step 1</h4> <p><b>When approaching a kinematics calculation question, first define the positive direction and write down all the values given in the question. </br></br> </b>A ball is thrown vertically upwards at 15.0ms<sup>-1</sup>. Find the time taken to reach its maximum height. </br>Take g = 9.81ms<sup>-1</sup></br></br>Take upwards as positive</br> u = 15.0ms<sup>-1</sup> </br> v = 15.0ms<sup>-1</sup></br>a = -9.81ms<sup>-2</sup></p>''', 
'''<h4>Step 2</h4> <p><b>From the values given, choose a suitable formula to use.</br>For linear motion questions, you can get the answer by using just one formula most of the time. </br></br> </b>
A ball is thrown vertically upwards at 15.0ms<sup>-1</sup>. Find the time taken to reach its maximum height. </br>Take g = 9.81ms<sup>-1</sup></br></br>
Take upwards as positive</br> u = 15.0ms<sup>-1</sup> </br> v = 15.0ms<sup>-1</sup></br>a = -9.81ms<sup>-2</sup></br> </br>using v = u + at,</br>
t = (v-u)/a </br>   = (0-15)/(-9.81)</br>   = 1.53s (3sf)</br></p>''']

projectile = ['''<h4>Step 1</h4>  <p><b>Define the positive direction and write down all the values given in the question.</b></br></br>
A ball is thrown with an initial velocity of 15ms<sup>-1</sup> at an angle of 60 degrees to the horizontal.</br></br>
Take upwards as positive</br> u = 15ms<sup>-1</sup></br></p> ''', 
'''<h4>Step 2</h4> <p><b>Resolve the horizontal and vertical components of initial velocity. </b></br></br>
A ball is thrown with an initial velocity of 15ms<sup>-1</sup> at an angle of 60 degrees to the horizontal.</br></br>
Take upwards as positive</br> u = 15ms<sup>-1</sup></br> u<sub>x</sub> = 15cos60</br>u<sub>y</sub> = 15sin60</p>
</p> ''',
'''<h4>Step 3</h4> <p><b>Apply suitable formula with the <b>vertical component</b> of initial velocity to find maximum height reached by object and time taken to reach the maximum height.</br>At the maximum height, v<sub>y</sub> equals zero. </b></br></br>
A ball is thrown with an initial velocity of 15ms<sup>-1</sup> at an angle of 60 degrees to the horizontal.</br></br>
Take upwards as positive</br> u = 15ms<sup>-1</sup></br> u<sub>x</sub> = 15cos60=13ms<sup>-1</sup></br>u<sub>y</sub> = 15sin60 = 7.5ms<sup>-1</sup></br><br>
using v<sup>2</sup> = u<sup>2</sup> + 2as</br>0=13<sup>2</sup> + 2(-9.81)s<sub>y</sub></br>s<sub>y</sub> = 8.6m</br></br></p>''',
'''<h4>Step 4</h4> <p><b>To find the total time of flght, apply suitable formula with <b>vertical component</b> of initial velocity. </br> When the object finishes its flight, vertical displacement equals zero</b></br></br>
A ball is thrown with an initial velocity of 15ms<sup>-1</sup> at an angle of 60 degrees to the horizontal.</br></br>
Take upwards as positive</br> u = 15ms<sup>-1</sup></br> u<sub>x</sub> = 15cos60=13ms<sup>-1</sup></br>u<sub>y</sub> = 15sin60 = 7.5ms<sup>-1</sup></br><br>
using v<sup>2</sup> = u<sup>2</sup> + 2as</br>0=13<sup>2</sup> + 2(-9.81)s<sub>y</sub></br>s<sub>y</sub> = 8.6m</br></br>
using v = u + at</br> - 13 = 13 + (-9.81)t</br> t = 2.7s</p> ''',
'''<h4>Step 5</h4> <p><b>To find the horizontal displacement when the object stops its flight, multiply the total time taken and horizontal component of initial velocity. </br>Horizontal component of velocity stays constant throughout the projectile motion. </br></br></b>
Take upwards as positive</br> u = 15ms<sup>-1</sup></br> u<sub>x</sub> = 15cos60=13ms<sup>-1</sup></br>u<sub>y</sub> = 15sin60 = 7.5ms<sup>-1</sup></br><br>
using v<sup>2</sup> = u<sup>2</sup> + 2as</br>0=13<sup>2</sup> + 2(-9.81)s<sub>y</sub></br>s<sub>y</sub> = 8.6m</br></br>
using v = u + at</br> - 13 = 13 + (-9.81)t</br> t = 2.7s</br></br>
s<sub>x</sub> = 2.7 * 13 = 35m
</p> ''']

def generate():
        index = random.randint(0,len(ques_index)-1)
        done.append(ques_index[index])
        ques_index.remove(ques_index[index])

#generate the order of question
while i < 12:
        generate()
        i = i + 1
        
top1 = '''<!DOCTYPE html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Kinematics</title>
<link rel="stylesheet" type="text/css" href="http://code.jquery.com/mobile/1.0.1/jquery.mobile-1.0.1.min.css" />
<script type="text/javascript" src="http://code.jquery.com/jquery-1.6.4.min.js"></script> 
<script type="text/javascript" src="http://code.jquery.com/mobile/1.0.1/jquery.mobile-1.0.1.min.js"></script>
<style type="text/css">
.num, .denom { font-size: 70%; }
.num { position: relative; bottom: 0.6ex; left: 0.2em; }
.denom { position: relative; left: -0.05em; }
</style>
Content-Type: text/html
<script language="JavaScript">
var correct = 0;
var shortsol = ['1.5','90','-9.81','displacement','35.1','6000','125','10.7','0.8','0.37','a','30'];
</script>

</head>'''

top2 = '''
<div data-role="page" id="top" data-theme="b">
			<div data-role="header" data-theme="b">
			<a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
				<h1>Kinematics!</h1>
			<a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
			</div>
			<div data-role="content">'''
				
bottom = '''			<div data-role="footer" data-position="fixed" data-theme="b">
     	        <h1>&copy; Copyright</h1>
			</div>
        </div> '''

class Student(db.Expando):
	pid = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
#	a = db.FloatProperty
#	u = db.FloatProperty
#	s = db.FloatProperty
#	v = db.FloatProperty
#	t = db.FloatProperty
	
class Homepage(webapp2.RequestHandler):
	''' Home page handler '''
	def get(self):
		''' Show home page '''
		# check if valid Google account
		user = users.get_current_user()
        
		if user:	# if valid logged in user
			# logout link
			url = users.create_logout_url(self.request.uri)
			# logout text
			url_linktext = 'logout'
			# retrieve user record
			query = Student.gql('WHERE pid = :1', user.nickname())
			# get 1 record
			result = query.fetch(1)
			if result:	# if user record found
				student = result[0]
				self.response.out.write(top1+top2)
				self.response.out.write('''<a href="/startlearning" data-role="button" data-ajax="false">Start Learning</a>
<a href="/calculator" data-role="button" data-ajax="false">Calculator</a>
<a href="/quiz" data-role="button" data-ajax="false">Quiz</a>''')
				self.response.out.write(bottom)
			else:		# not found
				self.response.out.write(top1+top2)
				self.response.out.write('''
			<a href="/startlearning" data-role="button" data-ajax="false">Start Learning</a>
			<a href="/calculator" data-role="button" data-ajax="false">Calculator</a>
<a href="/quiz" data-role="button" data-ajax="false">Quiz</a>''')
				self.response.out.write(bottom)

		else: 		# not logged in
			# login link
			url = users.create_login_url(self.request.uri)
			self.response.out.write(top)
			self.response.out.write('''<body>
<div data-role="page" id="top" data-theme="b">
			<div data-role="header" data-theme="b">
				<h1>Kinematics!</h1>
			</div>
			<div data-role="content">You have to login''' + url)
			self.response.out.write(bottom)


			
class QuizHandler(webapp2.RequestHandler):
	'''quiz handler'''
	def get(self):

		#now, all the question indexes are in the done list

		def display():
                    self.response.out.write(top1)
                    # prepare code for all questions except last question (which is different because its link leads to a different page)
                    for a in range(0, 7):                                    
                                    self.response.out.write('''<div data-role="page" id="q''')
                                    self.response.out.write(str(a))
                                    self.response.out.write('''">
                                <div data-role="header">
                                <a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
                                        <h1>Kinematics</h1>
                                        <a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
                                </div>
                                <div data-role="content" >''')
                                    self.response.out.write(question[done[a]])
                                    self.response.out.write('''<form method="post">
                                                    <label for="ans">Answer:</label><br /><input type="text" name="ans" id="ans"><br />''')
                                    self.response.out.write('''<p><a href="#s''')
                                    self.response.out.write(str(a))
                                    self.response.out.write('''" data-role="button" data-rel="dialog" data-transition="pop">Next</a></p>
                       </form> </div>''')
                                    self.response.out.write(bottom)
						#ans = self.request.get('ans')
									
                                    
                                    self.response.out.write('''<div data-role="page" id="s''')
                                    self.response.out.write(str(a))
                                    self.response.out.write('''" data-theme="b">

                                <div data-role="header">
                                        <h1>Kinematics</h1>
                                </div>
                                
                                <div data-role="content" data-theme="b">''')
#                                    if ans == shortsol[done[a]]:
#                                       self.response.out.write('''You got it right! <br><br>''')
#										correct = correct + 1
#                                    else:
#                                        self.response.out.write('''You got it wrong. <br><br>''')
                                    self.response.out.write("Solution:" + solution[done[a]])
                                    self.response.out.write('''<p><a href="#q''')
                                    self.response.out.write(str(a + 1))
                                    self.response.out.write('''" data-role="button" data-inline="true">Next Question</a></p>''')
                                    self.response.out.write('''</div>''')
                                    self.response.out.write('''<div data-role="footer" data-theme="b">
                                    <h1>&copy; Copyright</h1>
                                    </div>
                                    </div>''')

									
                    # code for final question, leading to score page
                    self.response.out.write('''<div data-role="page" id="q7">
                                <div data-role="header">
                                <a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
                                <h1>Kinematics</h1>
                                <a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
                                </div>
                                <div data-role="content">''')
                    self.response.out.write(question[done[7]])
                    self.response.out.write('''<form method="post">
                                                    <label for="ans">Answer:</label><br />
                            <input type="text" name="ans" id="ans"><br />
                            </form>''')
                    self.response.out.write('''<p><a href="#s''')
                    self.response.out.write(str(7))
                    self.response.out.write('''" data-role="button" data-rel="dialog" data-transition="pop">Next</a></p>
                        </div>''')
                    self.response.out.write(bottom)
                    self.response.out.write('''<div data-role="page" id="s''')
                    self.response.out.write(str(7))
                    self.response.out.write('''" data-theme="b">

                        <div data-role="header">
                                <h1>Kinematics</h1>
                        </div>
                        
                        <div data-role="content" data-theme="b">''')
##                    if answer == solution[done[a]]:
##                        self.response.out.write('''You got it right! <br><br>''')
##                    else:
##                        self.response.out.write('''You got it wrong. <br><br>''')
                    self.response.out.write(solution[done[7]])
                    self.response.out.write('''<p><a href="/" data-role="button" data-inline="true">Finish</a></p>''')
                    self.response.out.write('''</div>''')
                    self.response.out.write('''<div data-role="footer" data-theme="b">
                    <h1>&copy; Copyright</h1>
			</div>
                    </div>''')
                    

		display()
        def post(self):
            answer = self.request.get('ans')
            if answer == shortsol[done[a]]:
                   correct = correct + 1
            
# score page after finishing quiz
##class SolutionHandler(webapp2.RequestHandler):
##        '''solution page handler'''
##        
##        def get(self):
##            self.response.out.write(top1+top2)
##            self.response.out.write('''<h4>Your score: ''' + str(correct) + '''<br /></h4>''')
##            self.response.out.write('''<a href="/" data-role="button" data-ajax="false">Home</a>''')
##            self.response.out.write(bottom)

class LearnHandler(webapp2.RequestHandler):
	'''learn page handler'''
	def get(self):
		self.response.out.write(top1+top2)
		self.response.out.write('''<a href="/startlearning/linear" data-role="button" data-ajax="false">Linear Motion</a>''')
		self.response.out.write('''<a href="/startlearning/projectile" data-role="button" data-ajax="false">Projectile Motion</a>''')
		self.response.out.write(bottom)

class LearnLinearHandler(webapp2.RequestHandler):
	'''learn linear motion'''
	def get(self):	
		def display():
                        self.response.out.write(top1)                                 
                        self.response.out.write('''<div data-role="page" id="l1">
                                                <div data-role="header">
                                                <a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
                                                                <h1>Kinematics</h1>
                                                                <a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
                                                </div>
                                                <div data-role="content" >''')
                        self.response.out.write(linear[0])

                        self.response.out.write('''<a href="#l2" data-role="button" data-ajax="false">Next step</a>''')
                        self.response.out.write('''</div>''')
                        self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')
                                                        
                        self.response.out.write('''<div data-role="page" id="l2">
                                                <div data-role="header">
                                                <a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
                                                                <h1>Kinematics</h1>
                                                </div>
                                                <div data-role="content" >''')
                        self.response.out.write(linear[1])
                        self.response.out.write('''<a href="/" data-role="button" data-ajax="false">Home</a>''')
                        self.response.out.write('''</div>''')
                        self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')
			

		display()


class LearnProjectileHandler(webapp2.RequestHandler):
	'''learn linear motion'''
	def get(self):	
		self.response.out.write(top1)
		def display():
                        self.response.out.write(top1)
                        for a in range(0, 4):                                    
                                        self.response.out.write('''<div data-role="page" id="p''')
                                        self.response.out.write(str(a))
                                        self.response.out.write('''">
                                <div data-role="header">
                                <a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
                                                <h1>Kinematics</h1>
                                                <a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
                                </div>
                                <div data-role="content" >''')
                                        self.response.out.write(projectile[a])

                                        self.response.out.write('''<a href="#p''')
                                        self.response.out.write(str(a + 1))
                                        self.response.out.write('''" data-role="button" data-ajax="false">Next step</a>''')
                                        self.response.out.write('''</div>''')
                                        self.response.out.write('''<div data-role="footer" data-theme="b">
                                        <h1>&copy; Copyright</h1>
                                        </div>
                                        </div>''')

                        #last step
                        self.response.out.write('''<div data-role="page" id="p4">
                                                <div data-role="header">
                                                <a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
                                                                <h1>Kinematics</h1>
                                                                <a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
                                                </div>
                                                <div data-role="content" >''')
                        self.response.out.write(projectile[4])
                        self.response.out.write('''<a href="/" data-role="button" data-ajax="false">Home</a>''')
                        self.response.out.write('''</div>''')
                        self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')
                                
		display()
		

class CalculatorHandler(webapp2.RequestHandler):
	'''calculator handler'''
	def get(self):
		self.response.out.write(top1+top2)
		self.response.out.write('''<a href="/cal/lin" data-role="button" data-ajax="false">Linear</a>''')
		self.response.out.write('''<a href="/cal/pro" data-role="button" data-ajax="false" >Projectile</a>''')
		self.response.out.write('''<a href="#" data-role="button" onClick="parent.history.back()">Back</a>''')
		self.response.out.write(bottom)

class CalLinHandler(webapp2.RequestHandler):

	def get(self):
		self.response.out.write(top1)
		self.response.out.write('''<div data-role="page" id="maincal">
				<div data-role="header">
				<a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
							<h1>Kinematics</h1>
							<a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
					</div>
					<div data-role="content" >''')
		self.response.out.write('''
		<form action="/linresult" method="post">
									<label for="slider-1">u(ms<sup>-1</sup>)= </label>
									<input type="range" name="u" id="u" value="0" min="-100" max="100" data-highlight="true"/></br>
									<label for="slider-1">a(ms<sup>-2</sup>) = </label>
									<input type="range" name="a" id="a" value="0" min="-100" max="100" data-highlight="true"/></br>
									<input type="submit" id="linresult" name="linresult" value="Calculate"></form>''')

		self.response.out.write('''<a href="#" data-role="button"  onClick="parent.history.back()">Back</a>''')
		self.response.out.write('''</div>''')

		self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')

class CalLinResult(webapp2.RequestHandler):		
	def post(self):
		
		a = self.request.get('a')
		u = self.request.get('u')
		t = (-2) * int(u) / int(a)
		
		self.response.out.write('''<div data-role="page" id="result">
				<div data-role="header">
				<a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
							<h1>Kinematics</h1>
							<a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
					</div>
					<div data-role="content" >''')
		
		self.response.out.write('''a = ''' + a + '''</br>u = ''' + u)
		self.response.out.write('''</br> using s = ut + <font class=num>1</font>&#x2044;<font class=denom>2</font>at<sup>2</sup></br> t = ''' + str(round(t,1)))
		
		self.response.out.write('''<a href="#" data-role="button"  onClick="parent.history.back()">Back</a>''')
		self.response.out.write('''</div>''')

		self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')


class CalProjHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(top1)
		self.response.out.write('''<div data-role="page" id="maincal">
				<div data-role="header">
				<a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
							<h1>Kinematics</h1>
							<a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
					</div>
					<div data-role="content" >
					<form action="/projresult" method="post">
									<label for="slider-1">u(ms<sup>-1</sup>)= </label>
									<input type="range" name="u" id="u" value="0" min="-100" max="100" data-highlight="true"/></br>
									<label for="slider-1">a(ms<sup>-2</sup>) = </label>
									<input type="range" name="a" id="a" value="0" min="-100" max="100" data-highlight="true"/></br>
									<label for="slider-1">angle to horizontal(degrees) = </label>
									<input type="range" name="angle" id="angle" value="45" min="0" max="90" data-highlight="true"/></br>
									<input type="submit" id="projresult" name="projresult" value="Calculate"></form>''')

		self.response.out.write('''<a href="#" data-role="button" onClick="parent.history.back()">Back</a>''')
		self.response.out.write('''</div>''')

		self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')
		
class CalProjResult(webapp2.RequestHandler):		
	def post(self):
		a = self.request.get('a')
		u = self.request.get('u')
		angle = self.request.get('angle')
		uy = math.sin(int(angle)) * int(u)
		ux = math.cos(int(angle)) * int(u)
		sy = (-(float(uy))**2) * 0.5 / int(a)
		t = (-2) * int(uy) / int(a)
		sx = t * ux
		
		self.response.out.write('''<div data-role="page" id="result">
				<div data-role="header">
				<a href="/reference" data-rel="dialog" data-transition="slideup" data-icon="info" data-iconpos="notext">Formula Page</a>
							<h1>Kinematics</h1>
							<a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
					</div>
					<div data-role="content" >''')
		
		self.response.out.write('''a = ''' + a + '''</br>u = ''' + u +'''<br/>angle = '''+angle)
		self.response.out.write('''</br></br>u<sub>x</sub> = '''+str(round(ux,1)) +'''</br>u<sub>y</sub> = '''+str(round(uy,1)))
		self.response.out.write('''</br></br>using v<sup>2</sup> = u<sup>2</sup> + 2as<sub>y</sub></br>s<sub>y</sub> = ''' + str(round(sy,1)))
		self.response.out.write('''</br></br>using s<sub>y</sub> = u<sub>y</sub>t + <font class=num>1</font>&#x2044;<font class=denom>2</font>at<sup>2</sup></br> t = ''' + str(round(t,1)))
		self.response.out.write('''</br>s<sub>x</sub> = ''' + str(round(ux,1)))

		self.response.out.write('''<a href="#" data-role="button"  onClick="parent.history.back()">Back</a>''')
		self.response.out.write('''</div>''')

		self.response.out.write('''<div data-role="footer" data-theme="b">
                                                        <h1>&copy; Copyright</h1>
                                                        </div>
                                                        </div>''')		
         
		
class ReferenceHandler(webapp2.RequestHandler):
	'''quiz handler'''
	def get(self):
		self.response.out.write(top1)
		self.response.out.write('''<div data-role="page" id="top" data-theme="b">
			<div data-role="header" data-theme="b">
				<h1>Kinematics!</h1>
				<a href="#" data-role="button" data-icon="back" data-iconpos="notext" onClick="parent.history.back()">Back</a>
			</div>
			<div data-role="content">''')
		self.response.out.write('''<h2>Definitions and Formulas</h2>
		<p><b>Distance, d</b>: The total length of path covered by a moving object irrespective of the direction of motion. </br></br>
		<b>Displacement, s</b>: The linear distance of the position of the moving object from a given reference point. </br></br>
		<b>Equations of motion</b>:</br> 
		v = u + at</br>
		s = ut + <font class=num>1</font>&#x2044;<font
                class=denom>2</font>at<sup>2</sup></br>
		v<sup>2</sup> = u<sup>2</sup> + 2as
		
		<h5>u = initial velocity</br>
		v = final velocity</br>
		a = accleration</br>
		t = time</br>
		s = displacement</h5>''')
		
#main
app = webapp2.WSGIApplication([('/', Homepage),
                                ('/quiz',QuizHandler),
                                ('/startlearning',LearnHandler),
                                ('/calculator',CalculatorHandler),
                                ('/reference',ReferenceHandler),
                                ('/startlearning/linear',LearnLinearHandler),
                                ('/startlearning/projectile',LearnProjectileHandler),
##                                ('/solution',SolutionHandler),
								('/cal/lin',CalLinHandler),
								('/cal/pro',CalProjHandler),
								('/linresult',CalLinResult),
								('/projresult',CalProjResult)
                                ]
                                ,debug=True)
student1 = Student(pid='liu.yunzhu',name='LIU YUNZHU', email='liu.yunzhu@dhs.sg')
student1.put()
	
def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
