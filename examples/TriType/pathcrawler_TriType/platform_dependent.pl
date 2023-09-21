:- module(platform_dependent).

:- export endianness/1.
:- export sizeof_function/1.
:- export sizeof_pointer/1.
:- export sizeof_bool/1.
:- export sizeof_void/1.
:- export type_of_char/1.
:- export sizeof_int/2.
:- export sizeof_real/2.

endianness(little).
sizeof_function(-1).
sizeof_pointer(8).
sizeof_bool(_).
sizeof_void(-1).
type_of_char(signed).
sizeof_int(char,1).
sizeof_int(short,2).
sizeof_int(int,4).
sizeof_int(long,8).
sizeof_int('long long',8).
sizeof_real(float,4).
sizeof_real(double,8).
sizeof_real('long double',16).
