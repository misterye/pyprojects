Flask-Whooshee
--------------

Adds Whoosh integration to Flask-SQLAlchemy.


Setup
`````

Flask-Whooshee supports two different methods of setting up the extension.
You can either initialize it directly, thus binding it to a specific
application instance:

.. code:: python

    app = Flask(__name__)
    whooshee = Whooshee(app)

and the second is to use the factory pattern which will allow you to
configure whooshee at a later point:

.. code:: python

    whooshee = Whooshee()
    def create_app():
        app = Flask(__name__)
        whooshee.init_app(app)
        return app

Now you can create a basic whoosheer:

.. code:: python

    @whooshee.register_model('title', 'content')
    class Entry(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String)
        content = db.Column(db.Text)

and finally you can search the model:

.. code:: python

    Entry.query.whooshee_search('chuck norris').order_by(Entry.id.desc()).all()


Links
`````

* `Documentation <https://flask-whooshee.readthedocs.io>`_
* `Source Code <https://github.com/bkabrda/flask-whooshee>`_
* `Issues <https://github.com/bkabrda/flask-whooshee/issues>`_


