% =========================================================
% Thermometers — Step 3 (thermo.lp)
% Requires domain.lp with the facts: dim/1, cell/2, bulb/2, prev/4, row_target/2, col_target/2
% Output: fill(R,C) for cells filled with mercury.
% =========================================================

% 1) CHOICE: each cell of a thermometer may be filled or not.
{ fill(R,C) } :- cell(R,C).

% (optional, for safety) Forbid filling cells that are not part of a thermometer.
:- fill(R,C), not cell(R,C).

% 2) CONTINUITY: if you fill (R,C) and it has a predecessor (PR,PC), the predecessor must be filled.
%    This forces each thermometer to be filled as a PREFIX starting from its bulb.
:- fill(R,C), prev(R,C,PR,PC), not fill(PR,PC).

% 3) EXACT SUM RESTRICTIONS by ROW and COLUMN
:- row_target(R,K), K != #count { C : fill(R,C) }.
:- col_target(C,K), K != #count { R : fill(R,C) }.

% 4) (opcional) Show only the interpretation of interest for decode.py:
#show fill/2.
#show dim/1.