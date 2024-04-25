valid_assigns= """/*@assigns x[0]; */
void foo(int[] x){
  x[0] = 1;
  return;
}"""

invalid_assigns="""/*@assigns x[0]; */
void foo(int y){
  int x[0] = {y}
  return;
}
"""
