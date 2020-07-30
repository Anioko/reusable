from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
import commonmark
from app import db

payment = Blueprint('payment', __name__)

''' Edit these and re-use to enable paystack and stripe for users depending on
user locations. 

'''

'''

from app.paystack import Paystack, create_transaction_ref


@app.route('/private/group/courses/<course_title>/<int:course_id>/apply')
@login_required
def course_apply(course_id, course_title):
    """
    Applying for courses by applicants.

    THIS VIEW IS FOR APPLICANTS
    :param course_id: id of course to apply/join
    :return: nothing
    """
    course = db.session.query(Course).get(course_id)
    if course is None:
        abort(404)
    elif current_user.id is None:
        abort(403)
    else:
        if current_user in course.users:
            flash("You have <strong>already applied</strong> for {0}.".format(course.course_title), 'warning')
            return redirect(url_for('course_list'))
        else:
            rent_per_hour_count = course.rent_per_hour 
	    total_cost_teacher = course.cost_per_hour * course.hours_per_month
	    total_cost_rent = course.rent_per_hour * course.hours_per_month
            first_cost = total_cost_teacher + total_cost_rent
            all_cost = first_cost/course.min_students
            amount = 0
            amount1 = all_cost * 1.2
            amount2 = all_cost * 1.4
            amount3 = all_cost * 1.1 
            if course.min_students == len(course.users):
                amount = amount1
            elif course.min_students > len(course.users):
                amount = amount2
            elif course.min_students < len(course.users):
                amount = amount3
            return render_template('course/payment.html', course=course, amount=amount,
                                   key=app.config.get('STRIPE_PUBLISHABLE_KEY'))



@app.route('/courses/<course_title>/<int:course_id>/charge', methods=['POST'])
@login_required
def st_charge(course_id, course_title):
    course = db.session.query(Course).get(course_id)
    rent_per_hour_count = course.rent_per_hour / course.min_students
    total_cost_teacher = course.cost_per_hour * course.hours_per_month
    total_cost_rent = course.rent_per_hour * course.hours_per_month
    first_cost = total_cost_teacher + total_cost_rent
    all_cost = first_cost/course.min_students
    amount = 0
    #amount1 = course.cost_per_hour * 0.5 + course.cost_per_hour * course.hours_per_month / course.min_students + rent_per_hour_count
    #amount2 = course.cost_per_hour * 0.4 + course.cost_per_hour * course.hours_per_month / course.min_students + rent_per_hour_count
    #amount3 = course.cost_per_hour * 0.6 + course.cost_per_hour * course.hours_per_month  / course.min_students + rent_per_hour_count
    amount1 = all_cost * 1.2
    amount2 = all_cost * 1.4
    amount3 = all_cost * 1.1 
    if course.min_students == len(course.users):
        amount = amount1
    elif course.min_students > len(course.users):
        amount = amount2
    elif course.min_students < len(course.users):
        amount = amount3
    amount = amount * 100  # calculate the amount

    customer = stripe.Customer.create(
         email=current_user.email,
         card=request.form['stripeToken']
     )
    st_charge = stripe.Charge.create (
        customer=customer.id,
        amount=int(amount),
        currency='GBP',
        description='GBP {amount} Payment for {course_name}'.format(amount=amount, course_name=course.course_title)
    )
    if st_charge.to_dict()['status'] == "succeeded":
        course.users.append(current_user)
        db.session.add(course)
        db.session.commit()
        flash("You have <strong>successfully applied</strong> for {0}.".format(course.course_title), 'success')
        send_course_signup_mail(current_user)  
    else:
        flash("Some error occured. Please try again", 'warning')
    return redirect(url_for('course_list'))


    #try:
	#message = Message(subject="Class signup successfully!",
                             #sender='postmaster@teachera.co.uk',
                             #reply_to='support@teachera.co.uk',
                            #recipients=[current_user.email])
    	#body = "Hello:\t{0}\nYou have signed up to a class successfully."\
                         #"\nCongratulations on successfully applying to join the class. Please check with the course organizer or the teacher for more details\n"\
                         #"\n\n"\
                         #"Regards,\n"\
                         #"Teachera.org team"
    	#message.body= body.format(current_user.name)
    	#mail.send(message)
    	#except:
        	#pass
    #return redirect(url_for('course_list'))



@app.route('/private/group/courses/<course_title>/<int:course_id>/charge', methods=['POST'])
@login_required
def charge(course_id, course_title):
    course = db.session.query(Course).get(course_id)
    rent_per_hour_count = course.rent_per_hour / course.min_students
    total_cost_teacher = course.cost_per_hour * course.hours_per_month
    total_cost_rent = course.rent_per_hour * course.hours_per_month
    first_cost = total_cost_teacher + total_cost_rent
    all_cost = first_cost/course.min_students
    amount = 0
    #amount1 = course.cost_per_hour * 0.5 + course.cost_per_hour * course.hours_per_month / course.min_students + rent_per_hour_count
    #amount2 = course.cost_per_hour * 0.4 + course.cost_per_hour * course.hours_per_month / course.min_students + rent_per_hour_count
    #amount3 = course.cost_per_hour * 0.6 + course.cost_per_hour * course.hours_per_month  / course.min_students + rent_per_hour_count
    amount1 = all_cost * 1.2
    amount2 = all_cost * 1.4
    amount3 = all_cost * 1.1 
    if course.min_students == len(course.users):
        amount = amount1
    elif course.min_students > len(course.users):
        amount = amount2
    elif course.min_students < len(course.users):
        amount = amount3
    amount = amount * 100  # calculate the amount

    # =================  UNCOMMENT THIS LINE TO ENABLE PAYSTACK :--: IMPLEMENT CONDITION FOR REDIRECTION ============
    # Set conditional payment channel based on user location
    # if user.location == "Nigeria": # OR any other suitable condition you decide to use
    # If condition is true, return payWithPaystack()

    ############## UNCOMMENT THE LINE BELOW ##################################
    return payWithPaystack(amount, current_user.email, course_id)

    customer = stripe.Customer.create(
         email=current_user.email,
         card=request.form['stripeToken']
     )
    charge = stripe.Charge.create (
        customer=customer.id,
        amount=int(amount),
        currency='GBP',
        description='GBP {amount} Payment for {course_name}'.format(amount=amount, course_name=course.course_title)
    )
    if charge.to_dict()['status'] == "succeeded":
        course.users.append(current_user)
        db.session.add(course)
        db.session.commit()
        flash("You have <strong>successfully applied</strong> for {0}.".format(course.course_title), 'success')
        send_course_signup_mail(current_user)  # Edited by James
    else:
        flash("Some error occured. Please try again", 'warning')
    return redirect(url_for('course_list'))
    # try:
    #     message = Message(subject="Class signup successfully!",
    #                         sender='support@teachera.eu',
    #                         reply_to='support@teachera.eu',
    #                        recipients=[current_user.email])
    #     body = "Hello:\t{0}\nYou have signed up to a class successfully."\
    #                     "\nYou need to make an paymemt for this course. Contact the organizers or the teacher for more details\n"\
    #                     "\n\n"\
    #                     "Regards,\n"\
    #                     "Teachera.org team"  
    #     message.body= body.format(current_user.name)      
    #     mail.send(message)
    # except:
    #     pass
    # return redirect(url_for('course_list'))




# **************** PAY WITH PAYSTACK ***********************
def payWithPaystack(amount, user_email, course_id):
    """
    Initiate payment processing using abstracted Paystack API class, on successful connection, returns
    Paystack authorization url (which can be loaded using javascript on the user end, or redirected to) 
    to provide user card details input interface
    
    Params:
        amount: amount in naira to be paid 
        user_email: payers email address
    return: none
    """
    response_dict    =       {}
    reference        =       create_transaction_ref("payment", 10)
    callback_url     =       "www.teachera.org" + url_for('verify_pay', trx_ref=reference, course_id=course_id) 
    ps               =       Paystack()
    response_dict    =       ps.initiate_transaction(reference, amount, user_email, callback_url)
    if response_dict['status'] == "success":
        return redirect(response_dict['auth_url'])
    else:
        try:
            if response_dict['error_response']  ==  "Duplicate Transaction Reference":
                new_ref            =     create_transaction_ref("payment", 10)
                callback_url       =     "www.teachera.org" + url_for('verify_pay', trx_ref=new_ref, course_id=course_id)
                print "re-attempting payment with reference number %s" %(new_ref)
                response_dict      =      ps.initiate_transaction(new_ref, amount, user_email, callback_url)
                return redirect(response_dict['auth_url'])
        except Exception as e:
            print "Encountered error: %s" %(e)
    return redirect(response_dict['auth_url'])



# Verify paystack payment
@app.route('/paystack_api/verify_pay/<trx_ref>/<course_id>')
def verify_pay(trx_ref, course_id):
    course = db.session.query(Course).get(course_id)
    ps = Paystack()
    pay_status    =  ps.verify_transaction(trx_ref)
    if pay_status == "success":
        course.users.append(current_user)
        db.session.add(course)
        db.session.commit()
        flash("You have <strong>successfully applied</strong> for {0}.".format(course.course_title), 'success')
        #  SEND MAIL TO USER 
        send_course_signup_mail(current_user)
    else:
        flash("Some error occured. Please try again", 'warning')
    return redirect(url_for('course_list'))

'''

