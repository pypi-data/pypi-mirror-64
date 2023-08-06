'''
Expected features:
QUERY
- Query all
- Query some
- Query one
- Filters
-- per field value (exact match, regex)
-- Null attribute
-- Comparison numerical (>, >=, <, <=...)
-- Comparison dates (after, before)
- Ordering
-- Asc, Desc, per field
- Limit
- Pagination
-- ?
MUTATION
- Create
- Update
- Upsert
- Single mutation
- Multiple mutation
-- Sequential
-- Batch (Multiple mutations in single Mutation tag)
-- Parallel/Batch (Multiple mutations multi-threaded, each mutation may be batched)
SUBSCRIPTION # NOT PRIORITY
'''

# # ! old way [No additional libraries]:
# import requests
# import json
# @dataclass
# class Line():
#   id: str
#   name: str
#   speed: float

# LINE = '''
#   query getLine($name: String!){
#     line(findBy:{ name: $name }){
#       id
#       name
#       speed
#     }
#   }
# '''
# url = 'https://test.valiot.app/'
# content = {
#   'query': LINE,
#   'variables': {'name': 'LINEA001'}
# }
# response = requests.post(url, json=content)
# line_data = json.loads(str(response.content))
# line = Line(**line_data)
# line.name # * >> LINEA001
# # ! current way [pygqlc]:
# gql = GraphQLClient()
# @dataclass
# class Line():
#   id: str
#   name: str
#   speed: float

# LINE = '''
#   query getLine($name: String!){
#     line(findBy:{ name: $name }){
#       id
#       name
#       speed
#     }
#   }
# '''
# line_data, _ = gql.query_one(LINE, {'name': 'LINEA001'})
# line = Line(**line_data)
# line.name # * >> LINEA001

# # * New way (TBD):
# gql = GraphQLClient()
# orm = GStorm(client=gql, schema=SCHEMA_PATH)
# Line = orm.getType('Line')
# line = Line.find_one({'name': 'LINEA001'})
# line.name # * >> LINEA001

def main():
  print('Hello, GSTORM!')

if __name__ == "__main__":
  main()