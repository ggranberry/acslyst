:- module(infoFile).

:- heading:setval_file_name('TriType.c').
:- heading:setval_base_name('TriType').
:- heading:setval_pathcrawler_directory('pathcrawler_TriType').
:- heading:setval_trace_directory('pathcrawler_trace_TriType').

:- export user_type/3.
:- export type_name/2.
:- export local_var/3.
:- export formal_param/4.
:- export global_var/2.

type_name(0,0).

user_type(0,0,0).

local_var('trityp', 'Tritype', i(si(4))).
local_var('__retres', 'Tritype', i(si(4))).
local_var(0,0,0).

formal_param('c', '__FC_assert', 1, i(si(4))).
formal_param('file', '__FC_assert', 2, p(i(si(1)))).
formal_param('line', '__FC_assert', 3, i(si(4))).
formal_param('cond', '__FC_assert', 4, p(i(si(1)))).
formal_param('return value', 'Tritype', 0, i(si(4))).
formal_param('i', 'Tritype', 1, r(fl(8))).
formal_param('j', 'Tritype', 2, r(fl(8))).
formal_param('k', 'Tritype', 3, r(fl(8))).
formal_param(0,0,0,0).

global_var(0,0).

