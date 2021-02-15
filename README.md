# sb_19-01-12_Flask_Intro_Exercises

## Flask Greet and Calc  

## Assignment Details
#### ASSIGNMENT INVOLVED ####:
- Familiarization with Flask, setup of Flask environment, project setup, git setup.


### Greet ###
Application file is greet/app.py. Application has 3 possible routes:

**/welcome** 
- returns "welcome"
**/welcome/home**
- returns "welcome home"
**/welcome/back**
- returns "welcome back"


### Calc ###
Application is file calc/app.py. Calc supports 4 basic arithmetic functions -- add, sub, mult, and div. The required operands are a and b and the operands are passed in with a query string. All operations return a float value. Helpful error messages are displayed when operands are missing, are the incorrect type, and when the arithmetic operation returned an error. 

Two versions of **calc** exist:
#### Version 1 #### 
Routes and functions exist for each arithmetic operation. Routes are:
**/add?a=:a&b=:b** 
**/sub?a=:a&b=:b**
**/mult?a=:a&b=:b**
**/div?a=:a&b=:b**


#### Version 2 #### routes:
One route exists for all four arithmetic operations. The operation is passed into the function with a routes parameter. Routes are:
**/math/add?a=:a&b=:b**
**/math/sub?a=:a&b=:b**
**/math/mult?a=:a&b=:b**
**/math/div?a=:a&b=:b**


**TIMING**:
- 4.5 hours.


**ENHANCEMENTS**:
Error detection and handling. A website should provide meaningful messages when errors occur.
