from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask.ext.mail import Message, Mail
from redis import Redis
from rq import Queue
from sendingmail import send_email

# mail = Mail()
redis_con = Redis('localhost', 6379)
q = Queue('foo', connection=redis_con)


app = Flask(__name__)
app.secret_key = 'development key'


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'don@pigstycoders.com'
app.config["MAIL_PASSWORD"] = 'your-password'


# mail.init_app(app)


# def send_email(msg):
#     print("hallo world")
#     # mail.send(msg)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All Field Required')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@example', recipients=['your_email@example.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            result = q.enqueue_call(func=send_email, args=(msg,), result_ttl=5000)
            # result = q.enqueue(send_email, 'msg')
            print(result.result)
            # send_email(msg)
            return 'Form Posted'

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)