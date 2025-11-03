% CHOICE: each cell of a thermometer may be filled or not.
{ fill(R,C) } :- cell(R,C).

% Forbid filling cells that are not part of a thermometer.
:- fill(R,C), not cell(R,C).

% if you fill (R,C) and it has a predecessor (PR,PC), the predecessor must be filled.
% This forces each thermometer to be filled as a PREFIX starting from its bulb.
:- fill(R,C), prev(R,C,PR,PC), not fill(PR,PC).

% EXACT SUM RESTRICTIONS by ROW and COLUMN
:- row_target(R,K), K != #count { C : fill(R,C) }.
:- col_target(C,K), K != #count { R : fill(R,C) }.

% Show only the interpretation of interest for decode.py:
#show fill/2.
#show dim/1.