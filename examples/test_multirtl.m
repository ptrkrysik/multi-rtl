#!/usr/bin/env octave
#octave script checking if the multi_rtl works and debugginh

clear all
close all
pkg load signal
addpath('utils');

fs=1625000/6*4;

#run python script recording data from two channel multi_rtl receiver
system('python ./record_multi_rtl.py');
#load recorded data
x1=read_complex_binary('temp1');
x2=read_complex_binary('temp2');

#split into 
N=625*8*10;
NN=floor(length(x1)/N)-2;

xcorrs=zeros(NN,2*N+1);

time=[];
for ii=1:NN
    start=(ii-1)*N+1;
    stop=ii*N+2*N;
    xcorrs(ii,:)=xcorr(x1(start:stop),x2(start:stop), N);
    time(ii)=start/fs;
end

figure
imagesc(vec2mat(abs(x1),625))
title('amplitude of the signal at the input 1')
figure
imagesc(vec2mat(abs(x2),625))
title('amplitude of the signal at the input 2')

%figure
%plot(10*log10(abs(xcorrs([2,end-20],:))).')

figure
[m,p]=max((abs(xcorrs(:,:).')));
ylabel('delay [samples]');
xlabel('time [s]');
plot(time,p-N-1)
delete('temp1')
delete('temp2')
pause

