
close all;
clear all;

load('C:\Users\usuario\Documents\Mission Planner\logs\QUADROTOR\1\seg_1ms_e005\2019-06-30 20-41-46.log-119381.mat','ATT','POS')

range = 400:1:3000;

roll = ATT(:,4);
pitch = ATT(:,6);
yaw = ATT(:,8);

Lat = POS(:,3);
Lng = POS(:,4);
Alt = POS(:,5);

Org = [42.395969 -8.708963];

% lla2flat(lla, llo, psio, href)
% lla:  geodetic coordinates (latitude, longitude, and altitude), in [degrees, degrees, meters]
% llo:  Reference location, in degrees, of latitude and longitude, 
%       for the origin of the estimation and the origin of the flat Earth coordinate system
% psio: Angular direction of flat Earth x-axis (degrees clockwise from north), 
%       which is the angle in degrees used for converting flat Earth x and y coordinates 
%       to the North and East coordinates.
pos = lla2flat([Lat Lng Alt], Org, 180, 0);

%roll  = 45*ones(1,size(roll,1));
%pitch = 45*ones(1,size(pitch,1));
%yaw   = 45*ones(1,size(yaw,1));

fv_tr  = [1;0];
fv_rcv = [1;0];

% The position of the transmitting antenna is at the origin and 
% its local axes align with the global coordinate system.
pos_tr = [0;0;0];
axes_tr = azelaxes(0,0);

% The position of the receiving antenna is 100 meters along the global x-axis. 
% However, its local x-axis points towards the transmitting antenna.
axes_rcv0 = rotz(180)*azelaxes(0,0); % inicialmente las antenas se miran una a la otra

% Rotate the receiving antenna around its local x-axis in one-degree increments. 
% Compute the loss for each angle.
axes_rcv = [];


rollsubset  = roll(range);
pitchsubset = pitch(range);
possubset   = pos(range,:);

possubset   = [pos(range,1), pos(range,2), ones(size(range,2),1)]; % metemos 1 m de altura (eje z)

figure
plot(possubset(:,1),possubset(:,2))

%rollsubset  = [0 15 30 45]';
%pitchsubset = [0 15 15 15]';
%possubset   = [1 0 0; 2 0 0; 3 0 0; 4 0 0];

pos_rcv = [];
n = size(rollsubset,1);
for k = 1:n
    pos_rcv = [pos_rcv; possubset(k,1) possubset(k,2) possubset(k,3)];
end
pos_rcv=pos_rcv'; % esto es una chapuza


rho = zeros(1,n); % Initialize space
for k = 1:n
    axe_rot = roty(pitchsubset(k))*rotx(rollsubset(k))*axes_rcv0;
    axes_rcv = [axes_rcv; axe_rot];    
    rho(k) = polloss(fv_tr,fv_rcv,pos_rcv(:,k),axe_rot,pos_tr,axes_tr) ;
end

figure
subplot(3,1,1);
plot(rollsubset)
grid
title('Roll angle evolution')
ylabel('\phi\circ');

subplot(3,1,2);
plot(pitchsubset)
grid
title('Pitch angle evolution')
ylabel('\theta\circ');

subplot(3,1,3);
% Plot the polarization loss
hp = plot(rho);
% hax = hp.Parent;
% hax.XLim = [0,360];
% xticks = (0:(n-1))*45;
% hax.XTick = xticks;
grid;
title('Polarization loss during flight')
ylabel('Loss (dB)');

figure

global ColorOrder, ColorOrder='rbk';
arrow3(repelem(pos_rcv',1,1), axes_rcv(3:3:3*n,:)+repelem(pos_rcv',1,1),'k',1); % solo z
%arrow3(repelem(pos_rcv',3,1), axes_rcv+repelem(pos_rcv',3,1),'o',1); %x,y,z
xlabel('X','fontweight','bold','fontsize',12)
ylabel('Y','fontweight','bold','fontsize',12)
zlabel('Z','fontweight','bold','fontsize',12)
grid
hZLabel = get(gca,'ZLabel');
set(hZLabel,'rotation',0,'VerticalAlignment','middle')
axis equal

max(abs(rollsubset))
max(abs(pitchsubset))
max(abs(rho))
