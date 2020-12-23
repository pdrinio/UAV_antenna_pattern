
close all;
clear all;

load('C:\Users\usuario\Documents\Mission Planner\logs\QUADROTOR\1\seg_1ms_e005\2019-06-30 20-41-46.log-119381.mat','ATT','POS')

roll = ATT(:,4);
pitch = ATT(:,6);
TimeUS = ATT(:,2);

refTime = datenum([2019,07,01,12,00,00]);
times = refTime + TimeUS/(86400*1e6);
timestr=datestr(times,'yyyy-mm-dd HH:MM:SS.FFF');

t=datenum(timestr);  % convert date into a number to plot it


m = size(roll,1);
range = 1:1:m;

rollsubset  = roll(range);
pitchsubset = pitch(range);

figure
plot(t,pitchsubset)
datetick('x','MM:mm')   % give the a xaxis time label ticks..
grid
title('Pitch angle evolution')
ylabel('\theta\circ');

figure
plot(t,rollsubset)
datetick('x','MM:mm')   % give the a xaxis time label ticks..
grid
title('Roll angle evolution')
ylabel('\phi\circ');

max(abs(rollsubset))
max(abs(pitchsubset))

