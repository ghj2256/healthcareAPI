from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, TEXT, INTEGER, DATE, BigInteger


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://USER:PASSWORD@HOST:PORT/DATABASE"

api = Api(app)
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "person"

    person_id = Column(BigInteger, primary_key=True)
    gender_source_value = Column(TEXT)
    race_source_value = Column(TEXT)
    ethnicity_source_value = Column(TEXT)


class Death(db.Model):
    __tablename__ = "death"

    person_id = Column(BigInteger, primary_key=True)


class PersonCheck(Resource):
    def get(self):
        rows = Person.query.all()
        data = [{
            'id': row.person_id,
            'gender': row.gender_source_value,
            'race': row.race_source_value,
            'ethnicity': row.ethnicity_source_value
        } for row in rows]

        male = [x for x in range(len(data)) if data[x]['gender'] == 'M']
        female = [x for x in range(len(data)) if data[x]['gender'] == 'F']
        asian = [x for x in range(len(data)) if data[x]['race'] == 'asian']
        white = [x for x in range(len(data)) if data[x]['race'] == 'white']
        black = [x for x in range(len(data)) if data[x]['race'] == 'black']
        native = [x for x in range(len(data)) if data[x]['race'] == 'native']
        other = [x for x in range(len(data)) if data[x]['race'] == 'other']
        DeathCheck.get(self)

        total_n_death = 'Total patients: ' + str(len(data)) + ', ' + 'Death patients: ' + str(DeathCheck.get(self)) + ', '
        gender = 'Male patients: ' + str(len(male)) + ', ' + 'Female patients: ' + str(len(female)) + ', '
        race = 'Asian patients: ' + str(len(asian)) + ', ' + 'White patients: ' + str(len(white)) + ', ' \
               + 'Black patients: ' + str(len(black)) + ', ' + 'native patients: ' + str(len(native)) + ', ' \
               + 'other patients: ' + str(len(other))

        result = total_n_death + gender + race
        return result


class DeathCheck(Resource):
    def get(self):
        rows = Death.query.all()
        result = [{
            'id': row.person_id
        } for row in rows]
        return len(result)


api.add_resource(PersonCheck, '/person')
api.add_resource(DeathCheck, '/death')


if __name__ == "__main__":
    app.run(debug=True)
