from chains import repair_chain, model


program = """/* run.config_analyzer
   STDOPT: +"-lib-entry -main=\\"testme\\""
*/
/* run.config_generator_deter
   DEPS: params.pl
   STDOPT: +"-lib-entry -main=\\"testme\\" -pc-test-params=\\"params.pl\\""
*/
/* run.config*
   DONTRUN:
*/

/* A little example from test generation literature containing arrays with fixed dimensions and loops with fixed limits but the oracle is more complicated than the implementation !
   Returns 0 if at least one element of array a
                and all elements of array b
                are equal to target
   and 1 otherwise */
int testme(int a[4], int b[4], int target) {
  int i, fa, fb;

  i=0;
  fa=0;  /* found at least one occurrence of target in array a */
  fb=0;  /* found at least one occurrence of target in array a
            and all elements of array b are equal to target */

  /*@
    @ loop invariant i >= 0 && i <= 3;
    @ loop variant 3 - i;
    @ loop assigns fa;
  */
  while(i<=3){                    /* line 19 */
    if(a[i]==target) fa=1;        /* line 20 */
    ++i;
  }
  if(fa==1){                      /* line 23 */
    i=0;
    fb=1;
    /*@
      @ loop invariant i >= 0 && i <= 3;
      @ loop variant 3 - i;
      @ loop assigns fb;
    */
    while(i<=3){                  /* line 26 */
      if(b[i]!=target) fb=0;      /* line 27 */
      ++i;
    }
  }
  if(fb==1) return 0;             /* line 31 */
  else return 1;
}"""

wp = """[kernel] Parsing /var/folders/gd/zlz1_ptj22lbpxsxbb02t1h40000gn/T/tmpv6w725fa.c (with preprocessing)
[kernel:annot-error] /var/folders/gd/zlz1_ptj22lbpxsxbb02t1h40000gn/T/tmpv6w725fa.c:28: Warning:
  loop assigns is not allowed after loop variant.
[kernel] User Error: warning annot-error treated as fatal error.
[kernel] User Error: stopping on
  file "/var/folders/gd/zlz1_ptj22lbpxsxbb02t1h40000gn/T/tmpv6w725fa.c" that
  has errors. Add '-kernel-msg-key pp' for preprocessing command.
[kernel] Frama-C aborted: invalid user input."""

# out = repair_chain.invoke({"wp": wp, "program": program})
print(model.model_name)
