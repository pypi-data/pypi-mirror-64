** FlaskTrytonWTF
This project is intend to be used for extendig the capabilities of flask in order to read and write data directely to tryton

issiue/info: info@omniasolutions.eu

You can use this extention like a normal FlaskForm 
Just remember to add trytonObject and the field that you like to see in your input form
we also inser the subbit button in and if its pressed we write date into tryton 

```python
from FlaskTrytonWTF import FTWTF
...
...
...
class MyTrytonForm(FTWTF.TFlaskForm):
    trytonObject = tryton.pool.get('my.tryton.object')
    tryton_fields = {'field_1': {},
                     'field_2': {},
                     'field_3': {}
                     }
    submitLable = "Submit"
```

```python
@app.route('/input_form', methods=['GET', 'POST'])
@tryton.transaction()
def input_form():
    form = MyTrytonForm()
    if form.validate_on_submit():
        data_submitted = form.trytonSubmit() # DO NOT FORGET TO CALL THE TRYTON SUBMIT IN ORDER DO FLUSH THE DATA
                                             # ALSO THE DATA SUBMITTED IS RETURNED AS DICTIONAY OF VALUES 
                                             # SO YOU CAN USE IF !!
        return render_template('show_input_confirmation.html', title='Conferma', form=data_submitted)
    return render_template('input_form.html', form=form)
    
```