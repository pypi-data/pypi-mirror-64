#==============================================================================
#
#  $Id: form.py 837 2003-09-25 00:43:45Z mike $
#
"""
   Contains classes for building web forms.
"""
#
#  Copyright (C) 2003 Michael A. Muller
#
#  Permission is granted to use, modify and redistribute this code,
#  providing that the following conditions are met:
#
#  1) This copyright/licensing notice must remain intact.
#  2) If the code is modified and redistributed, the modifications must 
#  include documentation indicating that the code has been modified.
#  3) The author(s) of this code must be indemnified and held harmless
#  against any damage resulting from the use of this code.
#
#  This code comes with ABSOLUTELY NO WARRANTEE, not even the implied 
#  warrantee of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
#
#==============================================================================

import weakref
import htmlo
from wof import Node, DocWrapper

class FormControl(htmlo.XNull):
   pass

class DefaultFormEntry(FormControl):

   def __init__(self, request):
      FormControl.__init__(self, '', ': ', htmlo.Input(type = 'entry'))

   def setName(self, name):
      self[2]['name'] = name

   def setValue(self, value):
      self[2]['value'] = value
   
   def setWidth(self, width):
      self[2]['maxlength'] = `width`
   
   def setLabel(self, label):
      self[0] = label
   
   def setSecret(self, secret):
      if secret:
         self[2]['type'] = 'password'
      else:
         self[2]['type'] = 'entry'

class DefaultFormChoice(FormControl):
   
   def __init__(self, request):
      FormControl.__init__(self, '', ': ', htmlo.XSelect())

   def setName(self, name):
      self[2]['name'] = name
   
   def setValue(self, value):
      # go through the options, select the one that matches the value and
      # deselect everything else
      for item in self[2]:
         if item[0] == value:
            item['selected'] = 'on'
         else:
            if item.has_key('selected'):
               del item['selected']

   def setLabel(self, label):
      self[0] = label
   
   def addOption(self, option):
      self[2].append(option)

class FormButton(FormControl):

   def setLabel(self, label):
      self[0]['value'] = label

class DefaultSubmitButton(FormButton):
   
   def __init__(self, request):
      FormButton.__init__(self, htmlo.Input(type = 'submit'))

class DefaultResetButton(FormButton):

   def __init__(self, request):
      FormButton.__init__(self, htmlo.Input(type = 'reset'))

class FormGroup(FormControl):
   """
      This elemlet is a layout object that corresponds to a group of
      controls.
   """

   def __init__(self, request, *parms):
      FormControl.__init__(self, *parms)
      self._req = request
      self.__fields = None
      self.__parent = None
   
   def setFields(self, fields):
      """
         Sets the "fields" dictionary.  This is used to lookup field
         parameters that are not specified in the control methods.
         
         parms:
            fields::
               [dict<string, @FieldInfo>]  Dictionary mapping field names
               to field information objects.
      """
      self.__fields = fields
   
   def _getFieldInfo(self, fieldName):
      """
         Returns the field information object associated with the field
         name (a @FieldInfo instance) or *None* if information for the field
         does not exist.
         
         parms:
            fieldName::
               [string]
      """
      if self.__fields and self.__fields.has_key(fieldName):
         return self.__fields[fieldName]
      elif self.__parent:
         return self.__parent._getFieldInfo(fieldName)
      else:
         return None

   def _setParent(self, parent):
      """
         Sets the parent context.  Should be called by all implementations
         of @addGroup()
         
         parms:
            parent::
               [@FormGroup]
      """
      self.__parent = weakref.proxy(parent)
   
   def addControl(self, control):
      """
         Adds a form control to the group.
         
         Muet be implemented by derived class.
         
         parms:
            control::
               [@FormControl] control to be added.
      """
      raise NotImplementedError()
   
   def addEntry(self, name, width = None, label = None, required = 1, 
                secret = 0
                ):
      """
         Adds an entry control to the group.  The entry control is obtained
         from the "form.entry.required" or "form.entry.optional" method,
         depending on whether the entry is required or optional.
         
         parms:
            name::
               [string] entry name.  This is the name by which the entry
               control will be accessed.
            width::
               [int or None] if not *None*, this is the field width.
            label::
               [string or None] if specified, this is the entry field label.
            required::
               [boolean] if true, this entry is a required field, and will
               be annotated as such.
            secret::
               [boolean] if true, the entry is a "password" entry (input
               is obscured).
      """
      # get field information for the field
      fieldInfo = self._getFieldInfo(name)
      if fieldInfo:
         label = label or fieldInfo.label
         width = width or fieldInfo.maxLength
         required = required or fieldInfo.required or fieldInfo.minLength
         secret = secret or fieldInfo.secret
         
      if required:
         entry = self._req.getProperty('form.entry.required', DefaultFormEntry)
      else:
         entry = self._req.getProperty('form.entry.optional', DefaultFormEntry)
      entry.setName(name)
      if width:
         entry.setWidth(width)
      if label:
         entry.setLabel(label)
      if secret:
         entry.setSecret(1)
      
      # prefill the value if it is present in the query
      if self._req.query.has_key(name):
         entry.setValue(self._req.query[name])
      
      # add the entry
      self.addControl(entry)

   def addChoice(self, name, label = None, options = [], value = None):
      """
         Adds a new "choice" control to the form.
         
         parms:
            name::
               [string] choice control name.
            label::
               [string or None] label associated with the choice
            options::
               [list<string>] list of options
            value::
               [string or None] selected item in the list of options.
      """
      # try to get field information for the field
      fieldInfo = self._getFieldInfo(name)
      if fieldInfo:
         label = label or fieldInfo.label
         options = options or fieldInfo.options
      
      # create the choice control
      choice = self._req.getProperty('form.choice', DefaultFormChoice)
      
      # fill it with info
      choice.setName(name)
      if options:
         for opt in options:
            choice.addOption(opt)
      if label:   
         choice.setLabel(label)
      
      # prefill if present in the query
      if self._req.query.has_key(name):
         choice.setValue(self._req.query[name])
      
      # add the control
      self.addControl(choice)

   def addSubmitButton(self, label = None):
      """
         Adds a submit button to the group.  The submmit button is obtained
         from the "form.submit" property, a @DefaultSubmitButton instance
         by default.
         
         parms:
            label::
               [string or None] if not *None*, this is the label to be placed
               on the button.  This can also be obtained from the value
               of the "form.submit.label" property, and "Done" is used
               by default.
      """
      button = self._req.getProperty('form.submit', DefaultSubmitButton)
      
      if not label:
         label = self._req.getProperty('form.submit.label', 'Done')
      
      button.setLabel(label)
      
      # add the button
      self.addControl(button)
   
   def addResetButton(self, label = None):
      """
         Adds a reset button to the group.  The reset button is obtained
         from the "form.reset" property, a @DefaultResetButton instance
         is used by default.
         
         parms:
            label::
               [string or None] if not *None*, this is the label to be
               placed on the button.  This can also be obtained from the
               value of the "form.reset.label" property, and "Reset" is
               used by default.
      """
      button = self._req.getProperty('form.reset', DefaultResetButton)
      
      if not label:
         label = self._req.getProperty('form.reset.label', 'Reset')
      
      button.setLabel(label)

      self.addControl(button)

   def addGroup(self, style = 'form'):
      """
         Adds a new "control group".  This can be used to group a set of
         controls together.  The new group object is returned.

         The new group object is obtained from the "form.group./style/"
	 property if defined, then the "form.group" property, and
         finally @DefaultFormGroup is used by default.

         parms::
            style::
               [string] group display style.  Generally accepted styles
               are:
               
                  form::
                     Outer form.
                  buttons::
                     button panel.
               
               Other styles may be defined for richer forms.
      """
      group = self._req.getProperty('form.group.' + style)
      if group is None:
         group = self._req.getProperty('form.group', DefaultFormGroup)
      self.addControl(group)
      group._setParent(self)
      return group
   
class Form(FormGroup):
   
   def __init__(self, request, *parms):
      FormGroup.__init__(self, request, *parms)

   def setMethod(self, method):
      """
         Defines the form's submission method.
         
         Must be implemented by derived class.
         
         parms:
            method::
               [string] the form submission method, normally "GET" or "POST".
      """
      raise NotImplementedError()
      
   def setAction(self, action):
      """
         Defines the form's action URL.
         
         Must be implemented by derived class.
         
         parms:
            action::
               [string] the action URL.
      """
      raise NotImplementedError()

   def setLastPage(self, lastPage):
      """
         Creates a hidden "_lastPage" input on the form to allow the 
         submission page to display the last location.
         
         parms:
            lastPage::
               [string] last page URL.
      """
      raise NotImplementedError()   

class DefaultForm(Form):
   """
      Default form elemlet.  Implements a form as an HTML form with elements
      layed out in a table.  The table element is of class "formTable".
   """
   
   def __init__(self, request):
      self.__table = htmlo.Table()
      self.__table['class'] = 'formTable'
      self.__form = htmlo.Form(self.__table)
      Form.__init__(self, request, self.__form)
   
   def setMethod(self, method):
      self.__form['method'] = method
   
   def setAction(self, action):
      self.__form['action'] = action

   def setLastPage(self, lastPage):
      # check to see it the _lastPage input is already in the form.
      if isinstance(self.__form[0], htmlo.Input) and \
         self.__form[0]['name'] == '_lastPage':
         self.__form[0]['value'] = lastPage
      else:
         # if not, add it
         input = htmlo.Input(value = lastPage, type = 'hidden')
         input['name'] = '_lastPage'
         self.__form.insert(0, input)
   
   def addControl(self, control):
      # add the control as a table row
      self.__table.append(htmlo.TR(htmlo.TD(control)))   

class DefaultFormGroup(FormGroup):
   """
      Default implementation of a form control group.  No special HTML
      formatting is added: it remains a null group, so therefore
      flow layout should take effect.
   """
   
   def addControl(self, control):
      self.append(control)

#class FormNode(Node):
#   
#   def getPage(self, request, response):
#      path = request.context['path']
#      base, ext = os.path.splitext(path)
#      if ext == '.cxml':
#         parser = ElementParser(open(path))
#         parser.parse()
#         root = parser.getRootElem()
#      elif ext == '.xml':
#         parser = xml.sax.make_parser()
#         handler = xmlom.ContentHandler()
#         parser.setContentHandler(handler)
#         parser.setFeature(xml.sax.handler.feature_namespaces, 1)
#         root = parser.getDocNode()
#      
#      if root.getActualNamespace() != 'http://www.mindhog.net/

class FieldValidationError(Exception):
   """
      Raised when the value of the field is illegal.  Exception text
      is a good standard description of the error.
      
      Public-vars:
         fieldId::
            [string] Name of the field that failed validation.
         fieldLabel::
            [string] Text label of the field that failed validation.
         errorId::
            [string] Coded label specifying the error.  This should be a
            property name so that the error string can be looked up.
         extra::
            [any] Extra parameter for error string generation.  This varies
            depending on the nature of the error, if the value is not long
            enough, it is the minimum length.  If it it too long, it is the
            maximum length.
   """
   
   def __init__(self, fieldId, fieldLabel, errorId, text, extra = None):
      Exception.__init__(self, text)
      self.fieldId = fieldId
      self.fieldLabel = fieldLabel
      self.errorId = errorId
      self.extra = extra

class FieldError(htmlo.XNull):
   """
      An elemlet for field validation errors.  This is an abstract base
      class to allow these errors to be implemented as something other
      than a simple string.
   """
   
   def setLabel(self, label):
      """
         Sets the field label to be used in the error message.
         
         Must be implemented by derived class.
         
         parms:
            label::
               [string] the field label
      """
      raise NotImplementedError()
   
   def setExtra(self, extra):
      """
         Sets the "extra parameter" to be used in the error message.
         
         Must be implemented by derived class.
         
         parms:
            extra::
               [any] extra parameter
      """
      raise NotImplementedError()

class FieldInfo:
   """
      Provides information about a field definition.
      
      Public-vars:
         name::
            [string] field name.  This is the name used for the field
            in the form.
         label::
            [string] field label.  This is the human recognizable name of
            the field, and may vary in the representation of the form
            in other languages.
         minLength::
            [int] minimum field length.  If 0, this is ignored.
         maxLength::
            [int] maximum field length.  If 0, this is ignored.
         ignoreWS::
            [boolean] if true, leading and trailing whitespace is ignored
            for the field and its value.
         options::
            [list<string> or None]  If not *None*, this is a list of
            valid value options for this field.
         required::
            [boolean] if true, this is a required field
         secret::
            [boolean] if true, this is a secret field (its contents is 
            unreadable)
   """
   
   def __init__(self, name, label = None, minLength = 0, maxLength = 0,
                ignoreWS = 0, 
                options = None,
                required = 0,
                secret = 0,
                ):
      self.name = name
      self.label = label
      self.minLength = minLength
      self.maxLength = maxLength
      self.ignoreWS = ignoreWS
      self.options = options
      self.required = required
      self.secret = secret
   
   def validate(self, value):
      """
         Validates the field and returns the field value with any necessary
         transforms applied.  Raises a @FieldValidationError on failure.
      """
      
      # make sure we got a value
      if value is None:
         if self.minLength or self.required:
            raise FieldValidationError(self.name, self.label, 
                                       'form.field.error.empty',
                                       'You must specify a value for %s' % 
                                        self.label
                                       )
         else:
            # nothing further to validate
            return
      
      # strip whitespace if it is to be ignored
      if self.ignoreWS:
         value = value.strip()
      
      # if we have a set of options, check to see if the value is one of them,
      # if not, we fail, if so, we succeed
      if self.options:
         if value in self.options:
            return value
         else:
            raise FieldValidationError(self.name, self.label,
                                       'form.field.error.choice',
                                       'Illegal value specified for %s' %
                                        self.label
                                       )
      
      # generate one kind of error for an empty field
      valueLen = len(value)
      if (self.minLength or self.required) and not valueLen:
         raise FieldValidationError(self.name, self.label, 
                                    'form.field.error.empty',
                                    'You must specify a value for %s' % 
                                     self.label
                                    )
      
      # ... and another kind for a field that is not of the minimum length
      if self.minLength and valueLen < self.minLength:
         raise FieldValidationError(self.name, self.label,
                                    'form.field.error.short',
                                    '%s must be at least %d characters' %
                                     (self.label, self.minLength),
                                    self.minLength
                                    )
      
      # check for maximum length
      if self.maxLength and valueLen > self.maxLength:
         raise FieldValidationError(self.name, self.label,
                                    'form.field.error.long',
                                    '%s must be no more than %d characters in '
                                     'length' % (self.label, self.maxLength)
                                    )
      
      # return the (possibly transformed) value
      return value

class SubmissionResult:
   """
      Abstract base class for objects returned from the @FormModel.submit()
      method.
   """
   
   def getErrors(self):
      """
         Returns all of the errors as a list of strings or @FieldError
         instances (list<string or @FieldError>).  Returns *None* if
         no errors occurred.
         
         Must be implemented by derived class.
      """
      raise NotImplementedError()
   
   def getResult(self):
      """
         Returns the result object (which can be of any type).
         The caller should first have checked for errors with @getErrors().
         
         Must be implemented by derived class.
      """
      raise NotImplementedError()
   
   def getActionsCompleted(self):
      """
         Returns a list of actions completed (list<string or @htmlo.Element>)
         identifying the actions completed by the form.
      """
      raise NotImplementedError()

class DefaultSubmissionResult(SubmissionResult):
   """
      Simple implementation of @SubmissionResult.
   """
   def __init__(self, result = None, errors = None, exception = None,
                actionsCompleted = None
                ):
      """
         Callers will usuallly want to pass in either the /result/ or 
         /errors/ parameter, but using all default parameters is acceptable.
         If /errors/ is not-None, it means that there was an error and
         /result/ should be *None*.
         
         parms:
            result::
               [any or None] python data object to use as a result.
            errors::
               [list<string or @FieldError> or None] list of displayable errors
            exception::
               [Exception or None] a python exception object.  This should
               be used to transmit an exception if there were errors resulting
               from an exception.
            actionsCompleted::
               [list<string or @htmlo.Element> or None] list of completed
               actions (normally displayed on submission page.
      """
      self.__result = result
      self.__errors = errors
      self.__exception = exception
      self.__actionsCompleted = actionsCompleted
   
   def getErrors(self):
      "Implements @SubmissionResult.getErrors()"
      return self.__errors
   
   def getResult(self):
      "Implements @SubmissionResult.getResult()"
      return self.__result
   
   def getException(self):
      """
         Returns the python Exception instance associated with the errors
         or *None*.
         
         XXX might want to make this part of @SubmissionResult, but not yet.
      """
      return self.__exception
   
   def getActionsCompleted(self):
      """
         Returns the actions completed.  If this value is not passed in
         during constructed, a list containing the standard string,
         "Request Submitted" is returned.
      """
      if self.__actionsCompleted:
         return self.__actionsCompleted
      else:
         return ['Request Submitted']

class FormModel:
   """
      Base class for Form "model objects" - these are objects that define
      the data processing aspects of the form without any page 
      emission/rendering code.
      
      Derived classes should provide a "fields" class variable associated
      with a dict<string, @FieldInfo> mapping field names to field 
      information.
   """
   
   def validate(self, request, errorList):
      """
         Used to validate form submissions.  This is called prior to 
         @submit().  If it returns false, there was at least
         one validation error and @emitErrorPage() will be called instead.
         
         This method iterates over the field set (as defined by the
         /fields/ instance variable) and calls the @FieldInfo.validate()
         method for each field in it.
         
         May be overriden by derived classes, if so, you probably want
         to call this method first.
         
         parms:
            request::
               [@spugweb.Request] the initial request object
            errorList::
               [list<string or @spug.web.htmlo.HTMLElement>] This is an
               output parameter: an empty list should be passed in.
               If there are validation errors, they will be added to this
               list.
      """
      gotErrors = 0
      for field in self.getFields(request).values():
         value = request.query.get(field.name)
         try:
            request.query[field.name] = field.validate(value)
         except FieldValidationError, ex:
            # check for a property defining the error string
            errStr = request.context.get(ex.errorId)
            if errStr:
               if issubclass(errStr, FieldError):
                  # instatiate and populate
                  errStr = errStr()
                  errStr.setLabel(field.label)
                  errStr.setExtra(field.extra)
               elif type(errStr) is str:
                  if ex.extra is not None:
                     errStr = errStr % (ex.fieldLabel, ex.extra)
                  else:
                     errStr = errStr % ex.fieldLabel
            else:
               errStr = ex[0]
            
            # add the error to the list
            errorList.append(errStr)
            gotErrors = 1
      return not gotErrors

   def submit(self, request):
      """
         Called when a form is submitted.  All data processing should be
         done here.  This method must return an instance of @SubmissionResult.
         
         Must be implemented by derived classes.
         
         parms:
            request::
               [@spug.web.wof.Request]
      """
      raise NotImplementedError()

   def getFields(self, request):
      """
         Returns the set of fields for the form.  The "fields" instance
         variable is returned by default.

         Must be implemented by derived classes.
         
         parms:
            request::
               [@spug.web.wof.Request]
      """
      raise NotImplementedError()

class DefaultModel(FormModel):
   """
      Simple @FormModel which delegates all processing back to the @FormNode
      instance.  This will be used if no model object is specified.
   """
   
   def __init__(self, formNode):
      """
         parms:
            formNode::
               [@FormNode] window to use as a source.
      """
      self.__formNode = formNode
   
   def submit(self, request):
      "Implements @FormModel.submit()"
      return self.__formNode.submit(request)
   
   def getFields(self, request):
      "Implements @FormModel.getFields()"
      return self.__formNode.getFields(request)

class FormNode(Node):
   """
      Provides a nice framework for providing form processing.
      
      There are two ways to work with this node, you can either create a
      model object and specify it as the "form.model" property (thereby
      allowing maximum flexibility in the separation of rendering and
      business practice) or derive from this class and implement @submit()
      (and optionally @validate()).
      
      In any case, derived classes must override @emitSubmissionPage() and
      @emitFormPage() to implement form submission and generation.
      
      When these nodes are invoked with a remaining path of "submit",
      the form submission routine is called.  When invoked with any
      other remaining path, the form display routine is called.
      
      Instances of derived classes should have a "fields" variable which
      should be a dictionary implementation mapping field names
      to @FieldInfo instances defining the field information.
      
      Properties:
         form.model::
            [@FormModel] model object for the form.
   """

   def validate(self, request, errorList):
      """
         See @FormModel.validate() for docs.
         
         Derived classes may override this and call the base class
         version of the function.
      """
      model = request.getProperty('form.model', DefaultModel(self))
      return model.validate(request, errorList)
   
   def submit(self, request):
      """
         See @FormModel.submit() for docs.
         
         Derived classes not defining their own model object may override this.
      """
      model = request.getProperty('form.model', DefaultModel(self))
      return model.submit(request)
   
   def getFields(self, request):
      """
         See @FormModel.submit() for docs.
         
         Derived classes not defining their own model objects may override 
         this.
      """
      return self.fields
      
   def getContentType(self, request):
      return 'text/html'
   
   def emitPage(self, request, response):

      # check for whether there was any additional path info provided
      if request.remainingPath == ['submit']:
         
         # this is a "submit" request - process the form results
         
         # do form validation, check for errors.  If we're ok, do the submit()
         errors = []
         if self.validate(request, errors):
            
            # do the submit, check for errors
            result = self.submit(request)
            errors = result.getErrors()
         
         # emit the error page or submission page depending on whether or
         # not there were errors
         if errors:
            self.emitErrorPage(request, response, errors)
         else:
            self.emitSubmissionPage(request, response, result)

      else:
      
         # no recognized additional path information, just emit the form
         # page
         self.emitFormPage(request, response)

   def isStatic(self, request):
      if request.remainingPath == ['submit']:
         # submit page must be dynamic
         return 0
      else:
         # form page defaults to static
         return 1
   
   def getFormElem(self, request):
      """
         Returns the form element - this is the top level element used to
         contain the form.
         
         Must be implemented by derived classes unless both @emitFormPage() and
         @emitErrorPage() are implemented and this method is not used by them.
      """
      raise NotImplementedError()

   def getCompleteFormElem(self, request):
      """
         Utility method which returns the form element (result of
	 @getFormElem()) and adds the "method" and "action" (submit path)
	 attributes to the form (and the `_lastPage` hidden input field,
         if there is a `_lastPage` attribute).

         Compound pages wishing to include a form should use this instead of
	 calling @getFormElem() directly.

         parms:
            request::
               [@Request]
      """
      # get the form
      form = self.getFormElem(request)
      
      # set the method and action path
      form.setMethod('POST')
      submitPath = request.getAbsolutePath('submit', '.cur')
      form.setAction(submitPath)
      
      # add the _lastPage input if it is part of the query
      if request.query.has_key('_lastPage'):
         form.setLastPage(request.query['_lastPage'])
      
      return form
   
   def emitFormPage(self, request, response):
      """
         Generates the form.  Creates the page from the return value
         of @getFormElem() wrapped in the value of the "wrapper"
         property.
         
         May be overriden by derived classes: if not, @getFormElem() must
         be overriden.
      """
      # get the form page
      form = self.getCompleteFormElem(request)
      
      # build the wrapper
      wrapper = request.getProperty('wrapper', DocWrapper)
      wrapper.setParcel(form)
      
      # write the response
      wrapper.writeTo(response)

   def emitErrorPage(self, request, response, errorList):
      """
         Generates an error page suitable for displaying the validation
         errors for the form.  Creates the page from an unordered list 
         of validation errors followed by the return value of
         @getFormElem() wrapped in the value of the "form.wrapper"
         property.

         May be overriden by derived classes: if not, @getFormElem() must
         be overriden.
      """
      # get the form page
      form = self.getCompleteFormElem(request)
      
      # create the error element
      if len(errorList) > 1:
         errors = htmlo.XUL(*errorList)
      else:
         errors = errorList[0]
      
      # build the wrapper
      wrapper = request.getProperty('form.wrapper', DocWrapper)
      wrapper.setParcel(htmlo.XNull(errors, form))
      
      # write the response
      wrapper.writeTo(response)      

   def delegateSubmissionPage(self, request, response, actionsCompleted):
      """
         Delegates emission of the submission page to the URL specified
         in the #`_lastPage`# query parm (if any).  Returns true if the
         request was successfully delegated.
         
         parms:
            request::
               [@wof.Request]
            response::
               [@wof.Response]
            actionsCompleted::
               [list<@htmlo.Element or string>] list of actions to pass on
               to the delegate page through the "form.actionsCompleted"
               local request key.
      """
      # if there is a "_lastPage" variable, delegate page processing
      # to that URL.
      if request.query.has_key('_lastPage'):
         try:
            vreq = request.getVirtualRequest(request.query['_lastPage'])
         except Exception, ex:
            # XXX should be logging this
            print 'FormNode.delegateSubmissionPage(): got exception: %s' % ex
            return 0
         vreq.locals['form.actionsCompleted'] = actionsCompleted
         vreq.context.getNode().emitPageInContext(vreq, response)
         return 1
      else:
         print '  no _lastPage'
         return 0

   def emitSubmissionPage(self, request, response, submitResult):
      """
         Processes form parameters and generates response page.  Default
         version of this method calls @delegateSubmissionPage() to
         attempt to delegate processing, and just displays "Request 
         Submitted" if the request was not delegated.
         
         May be overriden by derived class.

         parms:
            request::
               [@wof.Request]
            response::
               [@wof.Response]
            submitResult::
               [@SubmissionResult] value returned from the @FormModel.submit()
               method.
      """
      actions = submitResult.getActionsCompleted()
      if not self.delegateSubmissionPage(request, response, actions):
         self.emitSimpleSubmissionPage(request, response, actions)
   
   def emitSimpleSubmissionPage(self, request, response, actionsCompleted):
      """
         Utility method which can be used to display a simple message
         acknowledging the submission of a form for pages that don't really
         have anything to display and no "_lastPage" field as been passed.
         
         parms:
            request::
               [@wof.Request]
            response::
               [@wof.Response]
            actionsCompleted::
               [list<string or @htmlo.Element>] list of actions completed
               for display.
      """
      # if there's only one thing in the list and it's a string, use it
      # as title and level one header
      if len(actionsCompleted) == 1 and isinstance(actionsCompleted[0], str):
         title = actionsCompleted[0]
         doc = htmlo.XNull(htmlo.H1(title), title = title)
      else:
         doc = htmlo.XNull(actionsCompleted, title = 'Request Submitted')
      
      # get the default wrapper
      wrapper = request.getProperty('wrapper', DocWrapper)
      wrapper.setParcel(doc)

      wrapper.writeTo(response)

class TestNode(FormNode):

   fields = { 'name': FieldInfo('name', 'Name', 1, 30, ignoreWS = 1),
              'email': FieldInfo('email', 'E-Mail Address', 1, 30, ignoreWS = 1),
             }

   def getFormElem(self, request):
      form = request.getProperty('form.outer', DefaultForm)
      form.setFields(self.fields)
      
#      form.addEntry('name', label = 'Name')
#      form.addEntry('email', label = 'E-Mail Address')
      form.addEntry('name')
      form.addEntry('email')
      buttons = form.addGroup('buttons')
      buttons.addSubmitButton()
      buttons.addResetButton()
      
      return form

   def emitSubmissionPage(self, request, response, submitResult):
      docFact = request.context.get('wrapper', DocWrapper)
      page = docFact(request)
      content = htmlo.XNull(
         htmlo.H1('Test Form Results'),
         htmlo.P('name = ', request.query['name'], ' email = ', 
                request.query['email']
                )
         )
      page.setTitle('test form result')
      page.setParcel(content)

      page.writeTo(response)

def submitAdapter(unused, request, response):
   spugwebPage.getPage(request, response)
