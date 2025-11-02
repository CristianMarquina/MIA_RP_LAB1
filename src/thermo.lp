% =========================================================
% Thermometers — Step 3 (thermo.lp)
% Necesita domain.lp con los hechos: dim/1, cell/2, bulb/2, prev/4, row_target/2, col_target/2
% Salida: fill(R,C) para celdas llenas de mercurio.
% =========================================================

% 1) ELECCIÓN: cada celda de un termómetro puede estar llena o no.
{ fill(R,C) } :- cell(R,C).

% (opcional, por seguridad) Prohibir llenar celdas que no sean de termómetro.
:- fill(R,C), not cell(R,C).

% 2) CONTINUIDAD: si llenas (R,C) y tiene predecesor (PR,PC), el predecesor debe estar lleno.
%    Esto fuerza que todo termómetro se llene como PREFIJO desde su bulbo.
:- fill(R,C), prev(R,C,PR,PC), not fill(PR,PC).

% 3) RESTRICCIONES DE SUMAS EXACTAS por FILA y COLUMNA
:- row_target(R,K), K != #count { C : fill(R,C) }.
:- col_target(C,K), K != #count { R : fill(R,C) }.

% 4) (opcional) Si quisieras mostrar también otras cosas, añade más #show.
% Mostrar sólo la interpretación de interés para decode.py:
#show fill/2.
#show dim/1.