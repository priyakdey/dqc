from ast import arg
import psycopg2
from yaml import load, CLoader as Loader

import functions
from template import Template, Type, TypeAttr, Validation


def fn_name():
    print("Hello World")


def main() -> int:
    with open(".\\resources\\templates.yaml", mode="r", errors="ignore") as fd:
        yaml_data = load(fd, Loader=Loader)     # yaml_data has the whole yaml loaded
    
    # lets try and get each template
    temp_list = yaml_data["templates"]
    templates = list()      # Master list of supported templates
    
    for item in temp_list:
        _name  = item["name"]
        _type  = Type[item["type"].upper()]
        _desc  = item["description"]
        _attrs = list()
        for attr in item["attrs"]:
            _attrs.append(TypeAttr[attr.upper()])

        template = Template(_name, _type, _desc, _attrs)
        templates.append(template)

    for template in templates:
        print(template)


    

    print("-----------------------------------------------------------------")

    
    with open(".\\resources\\validations.yaml", errors="ignore") as fd:
        data = load(fd, Loader=Loader)
    
    validations = list()
    temp_list = data["validations"]

    for item in temp_list:
        _name  = item["name"]
        _type  = Type[item["type"].upper()]
        _desc  = item["description"]
        _attrs = { TypeAttr[k.upper()]: v for k, v in item["attrs"].items() }
        validation = Validation(_name, _type, _desc, _attrs)
        validations.append(validation)

    for validation in validations:
        if validation.type == Type.SQL:
            print(f"INFO : Currently running validation {validation.name}")
            attrs = validation.attrs
            # because this is a sql, we absolutely know that it should have query and input args
            query = attrs[TypeAttr.QUERY]                  # This is mandatory so we use third brackets
            print(f"INFO : We are trying to execute the query: {query}")
            input_args = attrs.get(TypeAttr.INPUT_ARGS, None)   # This is optional so we use default
            conn = psycopg2.connect("dbname=postgres user=postgres password=password")
            cur  = conn.cursor()
            if input_args is None:
                cur.execute(query)
            else:
                cur.execute(query, tuple(input_args))
            records = cur.fetchall()
            print(records)
            cur.close()
            conn.close()
            

        if validation.type == Type.FUNCTION:
            print("INFO  : Currently trying to run a function")
            attrs = validation.attrs
            # because this is a function call, function name is a mandatory
            fn_name    = attrs[TypeAttr.FUNCTION]
            input_args = attrs.get(TypeAttr.INPUT_ARGS, None)
            if input_args is None:
                functions.execute(fn_name)
            else:
                functions.execute(fn_name, *input_args)
        
        print("----------------------------------------------------------")
    
    return 0


if __name__ == "__main__":
    exit(main())
