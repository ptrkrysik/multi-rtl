#!/usr/bin/env octave
#octave script for checking if the multi_rtl works

clear all
close all
pkg load signal
addpath('utils');

fs=1625000/6*4;

%run python script recording data from two channel multi_rtl receiver
system('python ./test_sync.py');
%load recorded data
x1=read_complex_binary('temp1');
x2=read_complex_binary('temp2');

N=625*8*10; %length of correlations
NN=floor(length(x1)/N)-2;

xcorrs=zeros(NN,2*N+1);

time=[];
x1_pow=[];
x2_pow=[];
for ii=1:NN
    start=(ii-1)*N+1;
    stop=ii*N+2*N;
    xcorrs(ii,:)=xcorr(x1(start:stop),x2(start:stop), N);
    time(ii)=start/fs;
    x1_pow(ii) = var(x1(start:stop));
    x2_pow(ii) = var(x2(start:stop));
end

figure
imagesc(vec2mat(20*log10(abs(x1(1:end))),625),[-50,0])
title('Amplitude of the signal at the input 1')
colorbar
figure
imagesc(vec2mat(20*log10(abs(x2(1:end))),625),[-50,0])
colorbar
title('Amplitude of the signal at the input 2')

%figure
%plot(10*log10(abs(xcorrs([2,end-20],:))).')

%plot the delay
figure(10)
[m,p]=max((abs(xcorrs(:,:).')));
xy = [];
for ii=1:length(p)
  xy(ii) = xcorrs(ii,50001);
end
plot(time, (angle(xy))/pi*180);
figure
plot(time,p-N-1)
title('Delay between two inputs');
ylabel('delay [samples]');
xlabel('time [s]');

N=floor(N/2);
NN=floor(length(x1)/N)-2;
xcorrs=zeros(NN,2*N+1);
for ii=1:NN
    start=(ii-1)*N+1;
    stop=ii*N+2*N;
    xcorrs(ii,:)=xcorr(x1(start:stop),x2(start:stop), N, 'biased');
    time(ii)=start/fs;
end
[m,p2]=max((abs(xcorrs(:,:).')));
figure(10)
#hold all
#xy = xcorrs(:,25001);
#plot(time, (angle(xy))/pi*180);
title('relative phase of the receivers')

%delete('temp1')
%delete('temp2')
%pause
figure
hold all
plot(x1_pow)
plot(x2_pow)
title('power')
pause
