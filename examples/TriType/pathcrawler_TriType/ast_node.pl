:- module(ast_node).

:- export ast_node/3.
:- export atomic_cond/2.
:- export stmt_location/3.

ast_node(n(21), ite, [cond(atomic_cond(n(24))), then(n(22)), else(empty)]). % TriType.c: l.14
ast_node(n(16), lor, [l_op(atomic_cond(n(19))),r_op(atomic_cond(n(17)))]). % TriType.c: l.12
ast_node(n(31), ite, [cond(atomic_cond(n(34))), then(n(32)), else(empty)]). % TriType.c: l.16
ast_node(n(36), ite, [cond(atomic_cond(n(39))), then(n(37)), else(empty)]). % TriType.c: l.17
ast_node(n(11), ite, [cond(n(13)), then(n(12)), else(empty)]). % TriType.c: l.12
ast_node(n(26), ite, [cond(atomic_cond(n(29))), then(n(27)), else(empty)]). % TriType.c: l.15
ast_node(n(13), lor, [l_op(n(16)),r_op(atomic_cond(n(14)))]). % TriType.c: l.12
ast_node(n(1), ite, [cond(n(3)), then(n(2)), else(empty)]). % TriType.c: l.10
ast_node(n(3), lor, [l_op(n(6)),r_op(atomic_cond(n(4)))]). % TriType.c: l.10
ast_node(n(6), lor, [l_op(atomic_cond(n(9))),r_op(atomic_cond(n(7)))]). % TriType.c: l.10
ast_node(n(2), seq, [255,256]). % TriType.c: l.11
ast_node(271, cond, [egal, 'i', 'j']). % TriType.c: l.14
ast_node(281, cond, [egal, 'j', 'k']). % TriType.c: l.16
ast_node(fun(179), func, ['Tritype', 3, 0, 1, 241]). % TriType.c: l.8
ast_node(251, cond, [inf, 'k', c(0.0,r(fl(8)))]). % TriType.c: l.10
ast_node(241, seq, [242,n(1),n(11),n(21),n(26),n(31),n(36),291,292]). % TriType.c: l.9
ast_node(274, assign, ['trityp', +(i(si(4)),'trityp',c(1,i(si(4))))]). % TriType.c: l.14
ast_node(255, assign, ['__retres', c(3,i(si(4)))]). % TriType.c: l.11
ast_node(279, assign, ['trityp', +(i(si(4)),'trityp',c(1,i(si(4))))]). % TriType.c: l.15
ast_node(n(12), seq, [269,270]). % TriType.c: l.13
ast_node(fun(170), func, ['__FC_assert', 4, 0, 0, 237]). % FRAMAC_SHARE/pc/lib/lanceur_deb.h: l.79
ast_node(256, return, ['__retres']). % TriType.c: l.11
ast_node(270, return, ['__retres']). % TriType.c: l.13
ast_node(n(38), seq, []). % : l.0
ast_node(291, assign, ['__retres', 'trityp']). % TriType.c: l.19
ast_node(289, assign, ['trityp', c(2,i(si(4)))]). % TriType.c: l.18
ast_node(n(27), seq, [279]). % TriType.c: l.15
ast_node(243, cond, [inf, 'i', c(0.0,r(fl(8)))]). % TriType.c: l.10
ast_node(262, cond, [infegal, +(r(fl(8)),'j','k'), 'i']). % TriType.c: l.12
ast_node(257, cond, [infegal, +(r(fl(8)),'i','j'), 'k']). % TriType.c: l.12
ast_node(237, seq, []). % FRAMAC_SHARE/pc/lib/lanceur_deb.h: l.83
ast_node(276, cond, [egal, 'i', 'k']). % TriType.c: l.15
ast_node(248, cond, [inf, 'j', c(0.0,r(fl(8)))]). % TriType.c: l.10
ast_node(265, cond, [infegal, +(r(fl(8)),'k','i'), 'j']). % TriType.c: l.12
ast_node(292, return, ['__retres']). % TriType.c: l.19
ast_node(n(37), seq, [289]). % TriType.c: l.18
ast_node(n(33), seq, []). % : l.0
ast_node(284, assign, ['trityp', +(i(si(4)),'trityp',c(1,i(si(4))))]). % TriType.c: l.16
ast_node(269, assign, ['__retres', c(3,i(si(4)))]). % TriType.c: l.13
ast_node(242, assign, ['trityp', c(0,i(si(4)))]). % TriType.c: l.9
ast_node(n(23), seq, []). % : l.0
ast_node(n(28), seq, []). % : l.0
ast_node(n(32), seq, [284]). % TriType.c: l.16
ast_node(286, cond, [supegal, 'trityp', c(2,i(si(4)))]). % TriType.c: l.17
ast_node(n(22), seq, [274]). % TriType.c: l.14
ast_node(239, return, []). % FRAMAC_SHARE/pc/lib/lanceur_deb.h: l.85
atomic_cond(n(29), [empty, 276]).
atomic_cond(n(34), [empty, 281]).
atomic_cond(n(7), [empty, 248]).
atomic_cond(n(39), [empty, 286]).
atomic_cond(n(9), [empty, 243]).
atomic_cond(n(14), [empty, 265]).
atomic_cond(n(24), [empty, 271]).
atomic_cond(n(4), [empty, 251]).
atomic_cond(n(17), [empty, 262]).
atomic_cond(n(19), [empty, 257]).
stmt_location(n(21), 'TriType.c', 14).
stmt_location(n(16), 'TriType.c', 12).
stmt_location(n(31), 'TriType.c', 16).
stmt_location(n(36), 'TriType.c', 17).
stmt_location(n(11), 'TriType.c', 12).
stmt_location(n(26), 'TriType.c', 15).
stmt_location(n(13), 'TriType.c', 12).
stmt_location(n(1), 'TriType.c', 10).
stmt_location(n(3), 'TriType.c', 10).
stmt_location(n(6), 'TriType.c', 10).
stmt_location(n(2), 'TriType.c', 11).
stmt_location(271, 'TriType.c', 14).
stmt_location(281, 'TriType.c', 16).
stmt_location(fun(179), 'TriType.c', 8).
stmt_location(251, 'TriType.c', 10).
stmt_location(241, 'TriType.c', 9).
stmt_location(274, 'TriType.c', 14).
stmt_location(255, 'TriType.c', 11).
stmt_location(279, 'TriType.c', 15).
stmt_location(n(12), 'TriType.c', 13).
stmt_location(fun(170), 'FRAMAC_SHARE/pc/lib/lanceur_deb.h', 79).
stmt_location(256, 'TriType.c', 11).
stmt_location(270, 'TriType.c', 13).
stmt_location(n(38), '', 0).
stmt_location(291, 'TriType.c', 19).
stmt_location(289, 'TriType.c', 18).
stmt_location(n(27), 'TriType.c', 15).
stmt_location(243, 'TriType.c', 10).
stmt_location(262, 'TriType.c', 12).
stmt_location(257, 'TriType.c', 12).
stmt_location(237, 'FRAMAC_SHARE/pc/lib/lanceur_deb.h', 83).
stmt_location(276, 'TriType.c', 15).
stmt_location(248, 'TriType.c', 10).
stmt_location(265, 'TriType.c', 12).
stmt_location(292, 'TriType.c', 19).
stmt_location(n(37), 'TriType.c', 18).
stmt_location(n(33), '', 0).
stmt_location(284, 'TriType.c', 16).
stmt_location(269, 'TriType.c', 13).
stmt_location(242, 'TriType.c', 9).
stmt_location(n(23), '', 0).
stmt_location(n(28), '', 0).
stmt_location(n(32), 'TriType.c', 16).
stmt_location(286, 'TriType.c', 17).
stmt_location(n(22), 'TriType.c', 14).
stmt_location(239, 'FRAMAC_SHARE/pc/lib/lanceur_deb.h', 85).
