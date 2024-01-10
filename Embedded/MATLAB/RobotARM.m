%% setting variables as symbols 
syms th2 th3
syms R Z 

%% making constant symbols 
a1 = 149.12e-3;
a2 = 14.19e-3;
a3 = 153.53e-3;
b1 = 14.25e-3;
b2 = 122.4e-3;
b3 = 31.26e-3;
r1 = 136e-3;
r2 = 146e-3;
%R = 374.89e-3;
%Z = 47.5e-3;

%% making equations
eqn1 = a1 + (r1 * sin(th2)) + a2 + (r2* cos(th3)) - a3 == Z;
eqn2 = (-b1) + (r1 *cos(th2)) + b2 + (r2*sin(th3)) + b3 == R;
eqns = [eqn1, eqn2];
vars = [th2 th3];

%% solving for variables 
solved = solve(eqns, vars, 'Real', true, 'IgnoreAnalyticConstraints', true); % , 'Real', true, 'IgnoreAnalyticConstraints', true

%% output formating
format shortEng

%% output equations
TH2 = solved.th2;
TH3 = solved.th3;

%% symbolic assumptions
assume( R<500e-3 & R>25e-3);
assume( Z<500e-3 & Z>40e-3);
assume( th2<pi & th2>0);
assume( th2<pi & th2>0);

%% simplify expretion
TH2_simp = simplify(TH2(2));
TH3_simp = simplify(TH3(2));

TH2_simp
TH3_simp

%% substituting in equations
Z = 47.5e-3;
R = 374.89e-3;
TH2 = double(subs(TH2(2)))/pi*180;
TH3 = double(subs(TH3(2)))/pi*180;

TH2_simp = double(subs(TH2_simp))/pi*180;
TH3_simp = double(subs(TH3_simp))/pi*180;

disp(TH2);
disp(TH3);

disp(TH2_simp);
disp(TH3_simp);