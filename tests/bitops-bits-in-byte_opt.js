var a=0,b,c,d=0;for(b=0;350>b;b++)for(c=0;256>c;c++){for(var e=d,f=1,g=0;256>f;)c&f&&g++,f<<=1;d=e+g}a=d;if(358400!=a)throw"ERROR: bad result: expected 358400 but got "+a;
