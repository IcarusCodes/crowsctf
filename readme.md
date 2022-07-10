Local setup:
- Make sure to activate crowsctfvenv with:  
`` source crowsctfvenv/bin/activate``  
You can exit the venv by running anywhere the `deactivate` command.
- In order to run the server we must run the following command:
``export FLASK_APP=__init__.py``
- Now to run the local server just use
``flask run``

For coding efficiency you can enable the debug mode by running
``export FLASK_DEBUG=1`` this will apply any code changes when
reloading the web page.