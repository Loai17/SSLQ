from flask import *
from flask import session as login_session
from sqlalchemy.exc import IntegrityError
from model import *
# from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import locale, os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LOCAL
engine = create_engine('sqlite:///database.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
	return render_template('main.html')

@app.route('/shop', methods=['GET'])
def shop():
	items = session.query(shopItems).all()
	return render_template('shopHomepage.html' , items=items)

@app.route('/shop/<itemId>',methods=['GET'])
def shopItem(itemId):
	item=session.query(shopItems).filter_by(id=itemId).one()
	return render_template('shopItem.html' , item=item)

@app.route('/admin', methods=['GET','POST'])
def admin():
	# Show login panel for admin only
	return render_template('admin.html')

@app.route('/admin/addItem',methods=['GET','POST'])
def addItem():
	if request.method == 'POST':
		newItem=shopItems(
			name=request.form['name'],
			price=request.form['price'],
			smallDesc=request.form['smallDesc'],
			desc=request.form['desc'],
			thumb=request.files['thumb'].filename,
			cover=request.files['cover'].filename
			)

		thumb=request.files['thumb']
		cover=request.files['cover']

		if (thumb and allowed_file(thumb.filename)) and (cover and allowed_file(cover.filename)):
			# session.add(newItem)
			# session.commit()
			thumb_name = "1_" + secure_filename(thumb.filename)
			cover_name = "1_" + secure_filename(cover.filename)
			thumb.save(os.path.join(app.config['UPLOAD_FOLDER'],thumb_name))
			cover.save(os.path.join(app.config['UPLOAD_FOLDER'],cover_name))
			# newItem.set_thumbnail(thumb)
			# newItem.set_cover(cover)
			session.add(newItem)
			session.commit()
			flash(newItem.name + " added to store sucessfully!")
			return redirect(url_for('admin'))

	else:
		return render_template('addItem.html')
	# Add if null statements. 

if __name__ == '__main__':
    app.run(debug=True)
