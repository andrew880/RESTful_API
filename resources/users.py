from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import json
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def __read(self):
        return pd.read_json('resources/users.json')
    def __save(self, data_):
        data_.to_json('resources/users.json')
        # data_.to_csv('users.json', index=False) 
        return data_
    def get(self):
        print("get")
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=False)  # add args
        parser.add_argument('name', required=False)
        parser.add_argument('city', required=False)
        args = parser.parse_args()  # parse arguments to dictionary

        data = self.__read()  # read local json
        data = data.to_dict()  # convert dataframe to dict
        ret_data = {}
        # print(args)
        
        if args['userId']==None and args['name']==None and args['city']==None:
            # print("OAO")
            return {'data': data}, 200  # return data and 200 OK
        else: 
            if args['userId'] in list(data['userId'].values()):
                index = list(data['userId'].keys())[list(data['userId'].values()).index(args['userId'])]
                for i in data:
                    ret_data[i] = {}
                    ret_data[i][index] = data[i][index]
                return {'data': ret_data}, 200  # return data and 200 OK
            else:
                # otherwise the userId does not exist
                return {
                    'message': f"'{args['userId']}' user not found."
                }, 404

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        print("posting")
        # read our CSV
        data = self.__read()

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'userId': [args['userId']],
                'name': [args['name']],
                'city': [args['city']],
                'locations': [[]]
            })
            print(new_data)
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            print(data)
            # data.to_csv('users.csv', index=False)  # save back to CSV
            self.__save(data)
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = self.__read()
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists !!! never put something like this in prod
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])
            
            # save back to CSV
            self.__save(data)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = self.__read()
        
        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]
            
            # save back to CSV
            self.__save(data)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404


api.add_resource(Users, '/users')  # add endpoints

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app