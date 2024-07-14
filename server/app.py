#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api

# Add your model imports
from models import Customer

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    
    if request.method == 'GET':
        customers = []
        for customer in Customer.query.all():
            customer_dict = customer.to_dict()
            customers.append(customer_dict)

        response = make_response(
            customers,
            200
        )

        return response

    elif request.method == 'POST':
        new_customer = Customer(
            name = request.form.get('name'),
            email = request.form.get('email'),
            number = request.form.get('number'),
        )

        db.session.add(new_customer)
        db.session.commit()

        customer_dict = new_customer.to_dict()

        response = make_response(
            customer_dict,
            201
        )

        return response

@app.route('/customers/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def customer_by_id(id):
    customer = Customer.query.filter(Customer.id == id).first()

    if customer == None:
        response_body = {
            'message': 'This customer does not exist in our database. Please try again'
        }

        response = make_response(
            response_body,
            404
        )

        return response

    else:
        if request.method == 'GET':
            customer_dict = customer.to_dict()

            response = make_response(
                customer_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(customer, attr, request.form.get(atr))

            db.session.add(customer)
            db.session.commit()

            customer_dict = customer.to_dict()

            response = make_response(
                customer_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(customer)
            db.session.commit()

            response_body = {
                'delete_successful': True,
                'message': 'Review deleted'
            }

            response = make_response(
                response_body,
                200
            )

            return response

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    pass

@app.route('transactions/<int:id>', methods=['GET'])
def transaction_by_id():
    pass

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    pass

@app.route('/inventory/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def inventory_by_id():
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)

