:- module(ast_node).
:- export ast_node/3.
:- export ast_supernode/4.
:- export topleveldec/3.
:- export ltest_start_branch/2.
:- export ltest_end_branch/2.
:- export immediate_dom_branch_loop_iter/4.
:- export recursive_func/1.
:- export neg_immediate_dom_branch_recur_call/3.
:- export syntactically_inconsistent_branches_mcdc_path/3.
:- export dec_path_and_coverage/3.
:- export syntactically_infeasible_dec_path_and_coverage/5.
:- export syntactically_unreachable_cond_node/1.
:- export syntactically_unreachable_uncond_node/1.
:- export stmt_location/4.
ast_node(n(11), ite, [n(13), n(12), empty]).
ast_node(n(1), ite, [n(3), n(2), empty]).
ast_node(271, cond, [egal, i, j]).
ast_node(281, cond, [egal, j, k]).
ast_node(fun(179), func, ['Tritype', 3, 0, 1, 241]).
ast_node(251, cond, [inf, k, c(0.0, r(fl(8)))]).
ast_node(274, assign, [trityp, +(i(si(4)), trityp, c(1, i(si(4))))]).
ast_node(279, assign, [trityp, +(i(si(4)), trityp, c(1, i(si(4))))]).
ast_node(289, assign, [trityp, c(2, i(si(4)))]).
ast_node(243, cond, [inf, i, c(0.0, r(fl(8)))]).
ast_node(262, cond, [infegal, +(r(fl(8)), j, k), i]).
ast_node(257, cond, [infegal, +(r(fl(8)), i, j), k]).
ast_node(276, cond, [egal, i, k]).
ast_node(248, cond, [inf, j, c(0.0, r(fl(8)))]).
ast_node(265, cond, [infegal, +(r(fl(8)), k, i), j]).
ast_node(284, assign, [trityp, +(i(si(4)), trityp, c(1, i(si(4))))]).
ast_node(242, assign, [trityp, c(0, i(si(4)))]).
ast_node(286, cond, [supegal, trityp, c(2, i(si(4)))]).
ast_node(n(6), lor, [243, 248]).
ast_node(n(13), lor, [n(16), 265]).
ast_node(n(3), lor, [n(6), 251]).
ast_node(n(16), lor, [257, 262]).
ast_node(n(26), ite, [276, 279, empty]).
ast_node(n(36), ite, [286, 289, empty]).
ast_node(n(31), ite, [281, 284, empty]).
ast_node(n(21), ite, [271, 274, empty]).
ast_node(255, setres, [c(3, i(si(4)))]).
ast_node(291, setres, [trityp]).
ast_node(269, setres, [c(3, i(si(4)))]).
ast_node(fun(170), func, ['__FC_assert', 4, 0, 0, empty]).
ast_node(256, cflow, [return]).
ast_node(n(2), seqg, [255, 256]).
ast_node(preprocess_node(2), seqg, [242, n(1)]).
ast_node(270, cflow, [return]).
ast_node(n(12), seqg, [269, 270]).
ast_node(preprocess_node(3), seq, [n(21), n(26), n(31), n(36), 291]).
ast_node(241, set, [preprocess_node(2), n(11), preprocess_node(3)]).
ast_supernode(241, fun(179), 0, fun(179)).
ast_supernode(276, n(26), cond, fun(179)).
ast_supernode(281, n(31), cond, fun(179)).
ast_supernode(286, n(36), cond, fun(179)).
ast_supernode(271, n(21), cond, fun(179)).
ast_supernode(n(13), n(11), cond, fun(179)).
ast_supernode(n(16), n(13), 0, fun(179)).
ast_supernode(n(3), n(1), cond, fun(179)).
ast_supernode(n(6), n(3), 0, fun(179)).
ast_supernode(243, n(6), 0, fun(179)).
ast_supernode(251, n(3), 1, fun(179)).
ast_supernode(257, n(16), 0, fun(179)).
ast_supernode(262, n(16), 1, fun(179)).
ast_supernode(248, n(6), 1, fun(179)).
ast_supernode(265, n(13), 1, fun(179)).
ast_supernode(279, n(26), then, fun(179)).
ast_supernode(289, n(36), then, fun(179)).
ast_supernode(284, n(31), then, fun(179)).
ast_supernode(274, n(21), then, fun(179)).
ast_supernode(preprocess_node(2), 241, 0, fun(179)).
ast_supernode(242, preprocess_node(2), 0, fun(179)).
ast_supernode(n(1), preprocess_node(2), 1, fun(179)).
ast_supernode(n(21), preprocess_node(3), 0, fun(179)).
ast_supernode(n(26), preprocess_node(3), 1, fun(179)).
ast_supernode(n(31), preprocess_node(3), 2, fun(179)).
ast_supernode(n(36), preprocess_node(3), 3, fun(179)).
ast_supernode(291, preprocess_node(3), 4, fun(179)).
ast_supernode(preprocess_node(3), 241, 2, fun(179)).
ast_supernode(n(11), 241, 1, fun(179)).
ast_supernode(n(12), n(11), then, fun(179)).
ast_supernode(n(2), n(1), then, fun(179)).
ast_supernode(255, n(2), 0, fun(179)).
ast_supernode(256, n(2), 1, fun(179)).
ast_supernode(269, n(12), 0, fun(179)).
ast_supernode(270, n(12), 1, fun(179)).
topleveldec(n(13), n(11), [257, 262, 265]).
topleveldec(n(3), n(1), [243, 248, 251]).
topleveldec(276, n(26), [276]).
topleveldec(281, n(31), [281]).
topleveldec(286, n(36), [286]).
topleveldec(271, n(21), [271]).
ltest_start_branch(0, 0).
ltest_end_branch(0, 0).
immediate_dom_branch_loop_iter(0, 0, 0, 0).
recursive_func(0).
neg_immediate_dom_branch_recur_call(0, 0, 0).
syntactically_inconsistent_branches_mcdc_path(0, 0, 0).
dec_path_and_coverage(n(13), true(or(true(or(true(257))))), [257]).
dec_path_and_coverage(n(13), true(or(true(or(false(257), true(262))))), [-257, 262]).
dec_path_and_coverage(n(13), true(or(false(or(false(257), false(262))), true(265))), [-257, -262, 265]).
dec_path_and_coverage(n(13), false(or(false(or(false(257), false(262))), false(265))), [-257, -262, -265]).
dec_path_and_coverage(n(3), true(or(true(or(true(243))))), [243]).
dec_path_and_coverage(n(3), true(or(true(or(false(243), true(248))))), [-243, 248]).
dec_path_and_coverage(n(3), true(or(false(or(false(243), false(248))), true(251))), [-243, -248, 251]).
dec_path_and_coverage(n(3), false(or(false(or(false(243), false(248))), false(251))), [-243, -248, -251]).
syntactically_infeasible_dec_path_and_coverage(0, 0, 0, 0, 0).
syntactically_unreachable_cond_node(0).
syntactically_unreachable_uncond_node(0).
stmt_location(n(21), 'TriType.c', 14, 0).
stmt_location(n(31), 'TriType.c', 16, 0).
stmt_location(n(36), 'TriType.c', 17, 0).
stmt_location(n(11), 'TriType.c', 12, 0).
stmt_location(n(26), 'TriType.c', 15, 0).
stmt_location(n(13), 'TriType.c', 12, 1).
stmt_location(n(16), 'TriType.c', 12, 2).
stmt_location(n(1), 'TriType.c', 10, 0).
stmt_location(n(3), 'TriType.c', 10, 1).
stmt_location(n(6), 'TriType.c', 10, 2).
stmt_location(n(2), 'TriType.c', 11, 0).
stmt_location(271, 'TriType.c', 14, 0).
stmt_location(281, 'TriType.c', 16, 0).
stmt_location(fun(179), 'TriType.c', 8, 0).
stmt_location(241, 'TriType.c', 9, 0).
stmt_location(274, 'TriType.c', 14, 0).
stmt_location(255, 'TriType.c', 11, 0).
stmt_location(279, 'TriType.c', 15, 0).
stmt_location(n(12), 'TriType.c', 13, 0).
stmt_location(fun(170), 'FRAMAC_SHARE/pc/lib/lanceur_deb.h', 79, 0).
stmt_location(256, 'TriType.c', 11, 0).
stmt_location(270, 'TriType.c', 13, 0).
stmt_location(291, 'TriType.c', 19, 0).
stmt_location(289, 'TriType.c', 18, 0).
stmt_location(243, 'TriType.c', 10, 1).
stmt_location(257, 'TriType.c', 12, 1).
stmt_location(262, 'TriType.c', 12, 2).
stmt_location(276, 'TriType.c', 15, 0).
stmt_location(248, 'TriType.c', 10, 2).
stmt_location(251, 'TriType.c', 10, 3).
stmt_location(265, 'TriType.c', 12, 3).
stmt_location(284, 'TriType.c', 16, 0).
stmt_location(269, 'TriType.c', 13, 0).
stmt_location(242, 'TriType.c', 9, 0).
stmt_location(286, 'TriType.c', 17, 0).
stmt_location(preprocess_node(2), 'TriType.c', 9, 0).
stmt_location(preprocess_node(3), 'TriType.c', 9, 0).
