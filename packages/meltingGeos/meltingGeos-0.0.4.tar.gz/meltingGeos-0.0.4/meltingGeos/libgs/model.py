
class Province:
    def __init__(self, code: str, name: str, shortName: str):
        self.type = "province"
        self.code = code
        self.name = name
        self.shortName = shortName
    
    def __str__(self) ->str:
        return f"type: ‘{self.type}', code: '{self.code}', name: '{self.name}', shortName: '{self.shortName}'"
    
    def __repr__(self) ->str:
        return f"type: '{self.type}'', code: '{self.code}', name: '{self.name}', shortName: '{self.shortName}'"
    

class City:
    def __init__(self, code: str, name: str, shortName: str):
        self.type = "city"
        self.code = code
        self.name = name
        self.shortName = shortName
    
    def __str__(self) ->str:
        return f"type: '{self.type}', code: '{self.code}', name: '{self.name}', shortName: '{self.shortName}'"
    
    def __repr__(self) ->str:
        return f"type: '{self.type}', code: '{self.code}', name: '{self.name}', shortName: '{self.shortName}'"


class Area:
    def __init__(self, code: str, name: str, shortName: str):
        self.type = "area"
        self.code = code
        self.name = name
        self.shortName = shortName
    
    def __str__(self) ->str:
        return f"type: '{self.type}', code: '{self.code}'', name: '{self.name}', shortName: '{self.shortName}'"
    
    def __repr__(self) ->str:
        return f"type: '{self.type}', code: '{self.code}'', name: '{self.name}', shortName: '{self.shortName}'"


class Street:
    def __init__(self, code: str, name: str, shortName: str):
        self.type = "street"
        self.code = code
        self.name = name
        self.shortName = shortName
    
    def __str__(self) ->str:
        return f"type: '{self.type}', code: '{self.code}', name: '{self.name}', shortName: '{self.shortName}'"
    
    def __repr__(self) ->str:
        return f"type: '{self.type}', code: '{self.code}', name: '{self.name}', shortName: '{self.shortName}'"


class Village:
    def __init__(self, code: str, name: str, shortName: str):
        self.type = "villages"
        self.code = code
        self.name = name
        self.shortName = shortName
    
    def __str__(self) ->str:
        return f"type: '{self.type}'', code: '{self.code}'', name: '{self.name}', shortName: '{self.shortName}'"
    
    def __repr__(self) ->str:
        return f"type: '{self.type}'', code: '{self.code}'', name: '{self.name}', shortName: '{self.shortName}'"