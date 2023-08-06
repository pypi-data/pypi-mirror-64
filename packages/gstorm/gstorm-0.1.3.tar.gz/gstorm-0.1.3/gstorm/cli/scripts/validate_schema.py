import os
from pprint import pprint
import click
from .cleanup import inmemory_cleanup

def scalar_map(field_typename):
  return {
    'Boolean': 'Boolean',
    'Integer': 'Int',
    'Float': 'Float',
    'String': 'String',
    'Text': 'Text',
    'Json': 'map',
    'Date': 'Date',
    'Time': 'Time',
    'Datetime': 'DateTime'
  }[field_typename]

def get_field_kind(field_typename):
  scalar_types = [
    'Boolean',
    'Integer',
    'Float',
    'String',
    'Text',
    'Json',
    'Date',
    'Time',
    'Datetime'
  ]
  if field_typename in scalar_types:
    return 'SCALAR'
  else:
    return 'OBJECT'

'''
Syntactic analizer for a graphql schema

things to consider:

# ! 1. general structure of a type
type TYPE_NAME @opts {
  ...
}
# ! 2. general structure of an enum
enum ENUM_TYPE @opts {
  ...
}
# ! 3. All basic types
type MyType {
  enabled: Boolean
  quantity: Int
  weight: Float
  name: String
  description: Text
  config: Json
  shipAt: Datetime
}
# ! 4. Complex type relations
# ? 4.1 ComplexType1.ListOf.ComplexType2 (Cannot be a list of BasicType)
# ? 4.2 ComplexType1.hasOne.ComplexType2 (Cannot be a hasOne of BasicType)
# ? 4.3 ComplexType1.ComplexType2 (ComplexType2 Must exist)
type User {
  name: String!
  address: Address @has_one
  posts: [Blogpost]
}

type Address {
  street: String
  city: String
  number: Integer
}

type Blogpost {
  author: User
  title: String @unique
}

type UserSkill {
  user: User
  skill: Skill
  level: Integer!
}

type Skill {
  name: String
}
'''
def gql_schema_parse(schema_file_lines):
  state = 'TYPE_SEARCH'
  schema = {} # dict of typenames
  # context
  current_type = None
  current_field = None
  for line in schema_file_lines:
    line = line.strip()
    tokens = line.split()
    if (state == 'TYPE_SEARCH'):
      if len(tokens) == 0:
        continue
      if tokens[0] == 'type':
        state = 'PARSING_TYPE'
        current_type = {}
        current_type['name'] = tokens[1]
        current_type['kind'] = 'TYPE'
        current_type['fields'] = []
      elif tokens[0] == 'enum':
        state = 'PARSING_ENUM'
        current_type = {}
        current_type['name'] = tokens[1]
        current_type['kind'] = 'ENUM'
        current_type['enumValues'] = []
      else:
        continue
    elif (state == 'PARSING_TYPE'):
      if len(tokens) == 0:
        # blank line inside the type
        continue
      elif tokens[0] == '}':
        # end of type definition
        state = 'TYPE_SEARCH'
        schema[current_type['name']] = current_type
        current_type = None
      else:
        # type body (should be a field definition)
        field_name = tokens[0].strip(':')
        field_is_required = '!' in tokens[1]
        field_is_list = '[' in tokens[1] and ']' in tokens[1]
        field_typename = tokens[1].strip('!').strip('[]').strip('!')
        field_kind = get_field_kind(field_typename)
        field_has_one = False if len(tokens) < 3 else '@has_one' == tokens[2]
        field_is_unique = False if len(tokens) < 3 else '@unique' == tokens[2]
        current_field = {}
        # current_field['required'] = field_is_required
        # current_field['is_unique'] = field_is_unique
        current_field['unique'] = field_is_unique
        current_field['has_one'] = field_has_one
        current_field['name'] = field_name
        current_field['type'] = {
          'name': field_typename if field_kind == 'OBJECT' else scalar_map(field_typename),
          'kind': 'LIST' if field_is_list else field_kind
        }
        current_type['fields'].append(current_field)
        current_field = None
    elif (state == 'PARSING_ENUM'):
      if len(tokens) == 0:
        # blank line inside the enum
        continue
      elif tokens[0] == '}':
        # end of enum definition
        state = 'TYPE_SEARCH'
        schema[current_type['name']] = current_type
        current_type = None
      else:
        # enum body (should be a EnumValue definition)
        current_type['enumValues'].append(tokens[0].strip())
  # we now know every schema type, we need to update the fields type kind to ENUM if needed:
  for typename, item in schema.items():
    if item['kind'] == 'ENUM':
      continue
    for index, field in enumerate(item['fields']):
      if not field['type']['name'] in schema:
        # may be an error, but leave it to the validation function
        continue
      if (
        field['type']['kind'] == 'OBJECT'
        and schema[field['type']['name']]['kind'] == 'ENUM'
      ):
        schema[typename]['fields'][index]['type']['kind'] = 'ENUM'
  return schema

def gql_schema_validate(schema):
  errors = []
  for typename, item in schema.items():
    print(f'\nvalidating type {typename}')
    # ! Style validation
    if typename[0].islower() or '_' in typename:
      # * No lowercasing Types
      errors.append({
        'type': item['name'],
        'field': field['name'],
        'message': f'Typename "{typename}" should be in CapitalCase'
      })
    if item['kind'] == 'TYPE':
      # ! validate every field
      for field in item['fields']:
        print(f'\tvalidating field {field["name"]}')
        # ! Style validation
        if field['name'][0].isupper():
          # * NO Capitalizing fields
          errors.append({
            'type': item['name'],
            'field': field['name'],
            'message': f'Field "{field["name"]}" should not be capitalized'
          })
        elif '_' in field['name']:
          errors.append({
            'type': item['name'],
            'field': field['name'],
            'message': f'Field "{field["name"]}" should be in camelCase'
          })
        # ! Schema validation
        if field['type']['kind'] == 'SCALAR':
          # u all right, fam
          continue
        elif field['type']['kind'] == 'LIST':
          # first of all, this type exists?
          if not field['type']['name'] in schema:
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': f'LIST type "{field["type"]["name"]}" does not exist'
            })
            continue
          # validate List Referring type has a field with corresponding type
          referred_type = schema[field['type']['name']]
          referred_fields = [
            ref_field for ref_field in referred_type['fields']
            if ref_field['type']['name'] == typename
            and not ref_field['has_one']
          ]
          if len(referred_fields) == 0:
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': 'LIST Has no corresponding object in referred type'
            })
          # elif len(referred_fields) > 1:
          #   errors.append({
          #     'type': item['name'],
          #     'field': field['name'],
          #     'message': 'LIST has too many referred types (Should be only one)'
          #   })
        elif field['type']['kind'] == 'OBJECT' and field['has_one']:
          # first of all, this type exists?
          if not field['type']['name'] in schema:
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': f'OBJECT type "{field["type"]["name"]}" does not exist'
            })
            continue
          # validate Object Referring type has a field with corresponding type
          referred_type = schema[field['type']['name']]
          referred_fields = [
            ref_field for ref_field in referred_type['fields']
            if ref_field['type']['name'] == typename
            and not ref_field['has_one']
          ]
          if len(referred_fields) == 0:
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': 'HAS_ONE has no corresponding object in referred type'
            })
          # elif len(referred_fields) > 1:
          #   errors.append({
          #     'type': item['name'],
          #     'field': field['name'],
          #     'message': 'HAS_ONE has too many referred types (Should be only one)'
          #   })
        elif field['type']['kind'] == 'OBJECT' and not field['has_one']:
          # first of all, this type exists?
          if not field['type']['name'] in schema:
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': f'Object field type "{field["type"]["name"]}" does not exist'
            })
            continue
          # validate List Referring type has a field with corresponding type
          referred_type = schema[field['type']['name']]
          referred_fields_has_one = [
            ref_field for ref_field in referred_type['fields']
            if ref_field['type']['name'] == typename
            and ref_field['has_one']
          ]
          referred_fields_list = [
            ref_field for ref_field in referred_type['fields']
            if ref_field['type']['name'] == typename
            and ref_field['type']['kind'] == 'LIST'
          ]
          if (
            len(referred_fields_has_one) > 0
            and len(referred_fields_list) > 0
          ):
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': 'OBJECT reference is both HAS_ONE and LIST in referred type'
            })
          elif (
            len(referred_fields_has_one) == 0
            and len(referred_fields_list) == 0
          ):
            errors.append({
              'type': item['name'],
              'field': field['name'],
              'message': f'field {field["name"]} has no corresponding LIST or HAS_ONE'
            })
    elif item['kind'] == 'ENUM':
      # ! validate Enumeration usage
      schema_object_types = {tn2: i2 for tn2, i2 in schema.items() if i2['kind'] == 'TYPE'}
      referring_types = [
        1 for typename2, item2 in schema_object_types.items()
        if len([
          1 for field in item2['fields']
          if field['type']['name'] == item['name']
        ]) > 0
      ]
      if len(referring_types) == 0:
        errors.append({
              'type': item['name'],
              'field': '',
              'message': 'ENUM does not have any referring type (should be at least one)'
            })
  return errors

@click.command()
@click.option('--src', default=None, help='Graphql schema file to analyze')
def validate_schema(src):
  clean_schema_lines = inmemory_cleanup(src)
  schema = gql_schema_parse(clean_schema_lines)
  validation_errors = gql_schema_validate(schema)
  if len(validation_errors) > 0:
    print(f'\n\n{len(validation_errors)} ERROR FOUND INSPECTING THE SCHEMA:')
    pprint(validation_errors)
    print('\n\n')
  else:
    print('\n\nNo errors found in the schema :)\n\n')
