:- module(test_parameters).

:- import create_input_val/3 from substitution.

:- export dom/4.
:- export ptr_in_base/2.
:- export type_base/2.
:- export create_input_vals/2.
:- export unquantif_preconds/2.
:- export quantif_preconds/2.
:- export strategy/2.
:- export precondition_of/2.
:- export val_existing_case/4.

:- export existing_coverage/4.

val_existing_case(0,0,0,0).
existing_coverage(0,0,0,0).
type_base(0,0).

ptr_in_base(0,0).

dom(0,0,0,0).
% add new array domain e.g.:
%  dom('yourFunName',e('yourArray',_),[],int([min..max])).

create_input_vals('Tritype',Ins):-
  create_input_val('k',double([-1.7976931348623157e+308..1.7976931348623157e+308]),Ins),
  create_input_val('j',double([-1.7976931348623157e+308..1.7976931348623157e+308]),Ins),
  create_input_val('i',double([-1.7976931348623157e+308..1.7976931348623157e+308]),Ins),
  true.
% add new variable domain e.g.:
%  create_input_val(yourVarName,int([min..max]),Ins), 


unquantif_preconds('Tritype',[]).

quantif_preconds('Tritype',[]).

strategy('Tritype',[]).

precondition_of(0,0).


