#!/usr/bin/env octave
#octave script for checking if the multi_rtl works

clear all
close all
pkg load signal
addpath('utils');

fs=1625000/6*4;

%run python script recording data from two channel multi_rtl receiver
system(['python ./mutlirtl_rx_to_cfile_2chan.py --sync-gain-ch0 25 --sync-gain-ch1 25  --freq-ch0=939.4e6 --freq-ch1=939.4e6 --sync-freq=939.4e6  --samp-rate ' num2str(1625000/6*4,'%.12f') ' -p -7 --fname-ch0 "temp1" --fname-ch1 "temp2" -N ' num2str(round(5*fs))]);

%load recorded data
x1=read_complex_binary('temp1');
x2=read_complex_binary('temp2');

N=625*8*10; %length of correlations
NN=floor(length(x1)/N)-2; %number of cross correlations for the signal

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

%plot amplitudes
figure(1)
imagesc(vec2mat(20*log10(abs(x1(1:end))),625),[-50,0])
title('Amplitude of the signal at the input 1')
colorbar
figure(2)
imagesc(vec2mat(20*log10(abs(x2(1:end))),625),[-50,0])
colorbar
title('Amplitude of the signal at the input 2')

%plot the phase
figure(3)
[m,p]=max((abs(xcorrs(:,:).')));
xy = [];
for ii=1:length(p)
  xy(ii) = xcorrs(ii,50001);
end
plot(time, (angle(xy))/pi*180);
title('relative phase of the receivers')

%plot the delay
figure(4)
plot(time,p-N-1)
title('Delay between two inputs');
ylabel('delay [samples]');
xlabel('time [s]');

%delete('temp1')
%delete('temp2')

figure(5)
hold all
plot(time,x1_pow)
plot(time,x2_pow)
title('Signal power')
pause
