/* To define the verdict of your oracle, 
   use one of the following macros (and then return) :

     pathcrawler_verdict_success();
     pathcrawler_verdict_unknown();
     pathcrawler_verdict_failure();

  For formal parameter of array, pointer or struct type of the tested function, there are two
  parameters in the oracle function: one with the Pre_ prefix and one without
  In each case, the oracle parameter with the Pre_ prefix stores
  a copy of the value of the corresponding parameter of the tested function
  before the tested function was called.
  The oracle parameter without the Pre_ prefix holds
  the current value (after the call of the tested function)
  of the corresponding parameter of the tested function.

  If you need to reference the value of a global variable before the
  tested function was called, prefix its name with Pre_.

  If the tested function returns a value, then it is stored in the
  last oracle function parameter.

  You may change the body of the oracle function but do NOT change its name and signature.
*/

void oracle_Tritype(double i, double j, double k, 
  int pathcrawler__retres__Tritype)
{
  pathcrawler_verdict_unknown();
}
