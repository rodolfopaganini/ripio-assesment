from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from datetime import date
import MySQLdb


class Transactions(Resource):
    @staticmethod
    def get(user_id):
        """
        This method allows to retrieve the sum of the amounts of the transactions for a given user id

        usage example:
        requests.get('http://127.0.0.1:5002/10')

        :param user_id: the ID of the user whose information is requested
        :return: the sum of the amounts of the transactions of the user whose ID is passed
        """

        # Connect to the database
        db = MySQLdb.connect(
            host='localhost',
            user='newUser',
            passwd='newUserPass',
            db='ripioDb',
        )

        # Get the sum of the transactions for the given id
        cur = db.cursor()
        query = f'SELECT SUM(total_amount) FROM transactions WHERE user_id = {user_id} GROUP BY user_id'
        cur.execute(query)

        # Close connection to db and return the requested value
        db.close()
        return float(cur.fetchall()[0][0])

    @staticmethod
    def put():
        """
        This method is used for adding entries to the database

        usage example:
        requests.put(
            'http://127.0.0.1:5002',
            json={"total_amount":10, "product":"socks_red", "txn_type":"BUY", "user_id":12},
        )

        :return: the data inserted in the database
        """

        # Get the data to insert
        data = request.get_json()

        # Connect to the database
        db = MySQLdb.connect(
            host='localhost',
            user='newUser',
            passwd='newUserPass',
            db='ripioDb',
        )

        # Get the highest id used in the table, in order to find an available one
        cur = db.cursor()
        cur.execute('SELECT MAX(id) FROM transactions')
        new_id = int(cur.fetchall()[0][0]) + 1

        # Get today's date as string
        current_date = date.today().strftime('%Y-%m-%d')

        # Insert the new values in the database
        cur = db.cursor()
        query = f"""INSERT INTO transactions
            VALUES (
                {new_id},
                {data["total_amount"]},
                "{data["product"]}",
                "{data["txn_type"]}",
                "{current_date}",
                {data["user_id"]}
            )"""
        cur.execute(query)
        db.commit()

        # Close connection to db and return the inserted value
        db.close()
        return jsonify(data)


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Transactions, '/<user_id>', '/')
    app.run(port='5002')
