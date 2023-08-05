#==============================================================================
#
"""
    A web form rendering/parsing library.
"""
#
#   Copyright (C) 2010 Michael A. Muller
#
#   This file is part of spug.web.
#
#   spug.web.forms is free software: you can redistribute it and/or modify it under
#   the terms of the GNU Lesser General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   spug.web.forms is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with spug.web.forms.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================

from htmlo import Div, H2, Input, TD, TextArea, XNull, XUL, XTable
from xmlo import encodeChars

class Field:
    """
        A field in a form.
    """
    
    def __init__(self, name, label, emptyOk = False, strip = True,
                 password = False,
                 size = 16,
                 regex = None,
                 converter = None,
                 unconverter = None
                 ):
        """
            parms:
                name: [str] field name.  Should be suitable for use as a 
                    python variable name, leading underscores are not allowed.
                label: [str] label that is displayed to the user.
                emptyOk: [bool] if true, the field value may be empty.
                strip: [bool] if true, trailing and leading whitespace will be 
                    stripped from the field.
                password: [bool] if true, the field contents should be 
                    concealed during entry.
                size: [int] the width of the field in characters.
                regex: [re.SRE_Pattern] if provided, this is a regular 
                    expression that the field should match.
                converter: [callable<str> or None] a function to convert the 
                    value from a string to any other type.  If the converter 
                    raises ValueError, this will be taken as a validation 
                    failure and an error will be set.
                unconverter: [callable<any> or None] a function to convert the 
                    value from the outut of the converter back to a value
                    suitable for form population.
        """
        self.name = name
        self.label = label
        self.emptyOk = emptyOk
        self.strip = strip
        self.password = password
        self.size = size
        self.regex = regex
        self.converter = converter
        self.unconverter = unconverter
    
    class __Fail(Exception):
        "Raised when field validation fails."
        def __init__(self, name, error):
            self.name = name
            self.error = error
    
    def set(self, formData, value):
        """
            Validate and set the field in the form data.  If the value is 
            valid, the attribute corresponding to the field name will be set 
            in the formData object.  If there was an error, an error will be 
            added to the formData object.
            
            parms:
                formData: [Data]
                value: [str] the value obtained from the request query params.
        """
        if self.strip:
            value = value.strip()
        
        try:
            if not self.emptyOk and not value:
                raise self.__Fail(self.name, 
                                  '%s may not be empty.' % self.label
                                  )
            
            
                raise self.__Fail(self.name, '%s is badly formed' % self.label)
            
            try:
                value = self.convert(value)
            except ValueError as ex:
                raise self.__Fail(self.name,
                                  'invalid value for %s: %s' %
                                   (self.label, ex)
                                  )

        except self.__Fail as ex:
            formData.addError(ex.name, ex.error)
            value = None
        
        formData.set(self.name, value)
    
    def convert(self, value):
        """
            Convert from the input type to the data type.
            
            Raises ValueError if the value cannot be converted.
        """
        if self.converter:
            return self.converter(value)
        else:
            return value
    
    def validate(self, value, errors):
        """
            Perform initial validation on a value.  Returns true if valid, 
            false if not.
            
            parms:
                value: [str] the original value.
                errors: [list<str>] an empty list to be populated with the 
                    error messages.
                    
        """
        if self.regex and not self.regex.match(value):
            return False
        else:
            return True

    def extract(self, query, formData):
        """
            Extract the field from the query and insert it into the form data 
            object.
            
            parms:
                query: [dict<str, list<str>>] query values.
                formData: [Data]
        """
        # make sure that a value was provided for the field
        value = query.get(self.name)
        if not value:
            formData.addError(self.name, '%s is missing.' % self.label)
            formData.set(self.name, None)
            return

        # pass the rest of the validations to the set method.
        self.set(formData, value[0])
    
    def createInput(self):
        """
            Creates the and return input element for the form (an Input 
            instance).
        """
        input = Input(name = self.name, size = self.size)
        if self.password:
            input['type'] = 'password'
        return input
    
    @property
    def visible(self):
        "Property which is true if the field is visible."
        return True

class BoolField(Field):
    """
        A form field for entering boolean values (a checkbox).
    """
    
    def extract(self, query, formData):
        "Overrides Field.extract(), for bool fields no value means false."
        value = query.get(self.name)
        if not value:
            formData.set(self.name, False)
        else:
            formData.set(self.name, True)
    
    def createInput(self):
        return Input(name = self.name, type = 'checkbox', value = 'true')

class HiddenField(Field):
    """
        A form field to store hidden values.
    """

    def __init__(self, name, *args, **kwargs):
        Field.__init__(self, name, 'Hidden field %s' % name, *args, 
                       **kwargs
                       )

    @property
    def visible(self):
        return False

    def createInput(self):
        return Input(name = self.name, type = 'hidden')    

class TextField(Field):
    """
        A form field for multi-line text.
    """

    def __init__(self, name, label, emptyOk = False, strip = True,
                 rows = 25,
                 cols = 80,
                 regex = None,
                 converter = None,
                 unconverter = None
                 ):
        Field.__init__(self, name, label, emptyOk, strip, regex = regex,
                       converter = converter,
                       unconverter = unconverter
                       )
        self.rows = rows
        self.cols = cols
    
    def createInput(self):
        return TextArea(name = self.name, rows = self.rows, cols = self.cols)

class Data:
    """
        A form data object.
        
        You can access form fields as attributes.
    """

    def __init__(self):
        self.__errors = []
        self.__dict = {}

    def addError(self, field, error):
        self.__errors.append((field, error))
    
    def hasErrors(self):
        return self.__errors
    
    def getErrorReport(self):
        tab = XUL()        
        for field, error in self.__errors:
            tab.append(encodeChars(error))
        return Div(H2('There were Errors'), tab)
    
    def getDict(self, schema):
        """
            Returns the field value dictionary with the fields for None 
            values removed.
            
            parms:
                schema: [Schema]
        """        
        # store a dictionary of the fields that "unconvert" their values 
        # (converting them back to a form that is acceptable for field 
        # population)
        convertingFields = {}
        for field in schema.fields:
            if field.unconverter:
                convertingFields[field.name] = field.unconverter

        # create the dictionary of values to be used for field population
        d = {}
        for key, val in self.__dict.iteritems():
            if val is not None and key in convertingFields:
                val = convertingFields[key](val)
            if val is not None:    
                d[key] = val
        return d

    def set(self, field, value):
        self.__dict[field] = value
    
    def __getattr__(self, attr):
        try:
            return self.__dict[attr]
        except KeyError as ex:
            raise AttributeError(ex[0])

class Schema:
    
    def __init__(self, *fields):
        self.fields = fields

    def render(self, formData = None):
        """
            Returns an XNull containing the contents of the form.
            
            parms:
                formData: [Data or None]
        """
        tab = XTable()
        contents = XNull('xnull', tab)
        for field in self.fields:
            input = field.createInput()
            if field.visible:
                tab.append([field.label + ':', input])
            else:
                # add invisible inputs to form contents after the table
                contents.append(input)
        tab.append(TD(Input(type = 'submit', value = 'Submit')))

        # populate with data if a data object was given
        if formData:
            contents.populate(formData.getDict(self))
        return contents
    
    def extract(self, req):
        """
            Returns a Data object which contains the field values 
            extracted from the request.
            
            parms:
                req: [spug.web.mgi.Request]
        """
        
        obj = Data()
        for field in self.fields:
            field.extract(req.query, obj)

        return obj

