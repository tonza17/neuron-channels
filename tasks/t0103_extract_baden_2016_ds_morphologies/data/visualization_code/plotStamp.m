function f = plotStamp(data,clus,groups)
% f = plotStamp(data)
%   Plot the cluster/group stamps as shown in Fig. S2.
%
%   Left figure:
%   Upper panels show all cells allocated to a certain group or
%   cluster. Lower panels shows means and 1SD error bars.
%
%   Right figure:
%   Grey lines show density estimate from entire population, blue lines for
%   group/cluster selected. Density estimates were produced with optimal
%   kernel width as estimated by ksdensity. Dashed lines indicate medians.
%   For DSi/OSi, the percentage indicates the fraction of significantly
%   tuned cells.
%
%   Input:
%       data    data structure
%       clus    group or cluster idx
%       groups  if 1, groups are shown (default)
%               if 0, clusters are shown
%
%   Output:
%       f       figure handle
%
%   Code for: Baden et al, Nature, 2016
%
%   Philipp Berens, 10.12.2015
%   www.retinal-functomics.org

%% preliminaries

if nargin<2 || groups==1
    cI = data.group_idx;
    gs = 'Group';
    names = {'OFF local, OS', 'OFF DS', 'OFF step', 'OFF slow', 'OFF alpha sust.', '(ON-)OFF JAM-B mix', 'OFF sust.', ...
    'OFF alpha trans.', 'OFF mini alpha trans.', 'ON_OFF local-edge W3', 'ON-OFF local', 'ON-OFF DS 1', 'ON-OFF DS 2', ...
    '(ON-)OFF local, OS', 'ON step', 'ON DS trans.', 'ON local trans.', 'ON trans.', 'ON trans., large', 'ON high freq.', ...
    'ON low freq.', 'ON sust.', 'ON mini alpha', 'ON alpha', 'ON DS sust. 1', 'ON slow', 'ON contrast suppr.', 'ON DS sust. 3', ...
    'ON local sust. OS', 'OFF suppr. 1', 'OFF suppr. 2'};

    if clus<33
        groupname = names{clus};
    else
        groupname = 'AC';
    end


elseif groups==0
    cI = data.cluster_idx;
    gs = 'Cluster';

end

idx = find(cI == clus);

N = length(idx);

%% set up figure panels
f1 = figure;
f1.Position = [25 50 800 700];

f2 = figure;
f2.Position = [850 50 700 400];

figure(f1);


%% figure 1: functional data

subplot(2,5,1:2) % chirp
imagesc(data.chirp_time,1:N,data.chirp_avg(:,idx)',[-1 1])

chirp_events = [2 5 8 10 18 20 28 30 31.5];
for i=1:length(chirp_events)
    line([chirp_events(i) chirp_events(i)],[0 N],'color','k','linestyle',':')
end
set(gca,'xtick',[0 10 20 30])
title('Chirp')
ylabel('RGCs')

axis normal

subplot(2,5,6:7)
shadedErrorBar(data.chirp_time,mean(data.chirp_avg(:,idx),2), std(data.chirp_avg(:,idx),[],2))
axis normal
xlim([data.chirp_time(1) data.chirp_time(end)])
ylim([-1.1 1.1])
for i=1:length(chirp_events)
    line([chirp_events(i) chirp_events(i)],[-1 1],'color','k','linestyle',':')
end
line([data.chirp_time(1) data.chirp_time(end)], [0 0],'linestyle',':','color','k')
xlabel('Time (s)')
ylabel('Amplitude')
set(gca,'xtick',[0 10 20 30])
set(gca,'ytick',[-1 0 1])
set(gca,'box','off')


% moving bar
subplot(2,5,3)  % all traces
imagesc(data.bar_time,1:N,data.bar_tc(:,idx)',[-1 1])
axis normal
bar_events = [1 2];
for i=1:length(bar_events)
    line([bar_events(i) bar_events(i)],[0 N],'color','k','linestyle',':')
end
set(gca,'xtick',[0 2 4])
title('Moving Bar')


subplot(2,5,8)  % average
shadedErrorBar(data.bar_time,mean(data.bar_tc(:,idx),2),std(data.bar_tc(:,idx),[],2))
line([data.bar_time(1) data.bar_time(end)], [0 0],'linestyle',':','color','k')

for i=1:length(bar_events)
    line([bar_events(i) bar_events(i)],[-1.1 1.1],'color','k','linestyle',':')
end

set(gca,'xtick',[0 2 4])
set(gca,'ytick',[-1 0 1])

ylim([-1.1 1.1])
xlim([data.bar_time(1) data.bar_time(end)])
axis normal
xlabel('Time (s)')
set(gca,'box','off')


% receptive field
subplot(2,5,4)
imagesc(data.rf_time,1:N,data.rf_tc(:,idx)',[-3 3])
axis normal
bar_events = [0];
for i=1:length(bar_events)
    line([bar_events(i) bar_events(i)],[0 N],'color','k','linestyle',':')
end
set(gca,'xtick',[0 .5 1 1.5])
title('RF kernel')

subplot(2,5,9)
shadedErrorBar(data.rf_time,mean(data.rf_tc(:,idx),2),std(data.rf_tc(:,idx),[],2))
line([data.rf_time(1) data.rf_time(end)], [0 0],'linestyle',':','color','k')

for i=1:length(bar_events)
    line([bar_events(i) bar_events(i)],[-3 3],'color','k','linestyle',':')
end

set(gca,'xtick',[0 .5 1 1.5])
ylim([-3.5 3.5])
xlim([data.rf_time(1) data.rf_time(end)])
axis normal
xlabel('Time (s)')
set(gca,'box','off')


% color stimulus
subplot(2,5,5)
imagesc(data.color_time,1:N,data.color_avg(:,idx)',[-1 1])
axis normal
bar_events = [1 4 7 10];
for i=1:length(bar_events)
    line([bar_events(i) bar_events(i)],[0 N],'color','k','linestyle',':')
end
set(gca,'xtick',[0 4 8 12])
title('Color')

subplot(2,5,10)
shadedErrorBar(data.color_time,mean(data.color_avg(:,idx),2),std(data.color_avg(:,idx),[],2))
line([data.color_time(1) data.color_time(end)], [0 0],'linestyle',':','color','k')

for i=1:length(bar_events)
    line([bar_events(i) bar_events(i)],[-3 3],'color','k','linestyle',':')
end

set(gca,'xtick',[0  4  8 12])
set(gca,'ytick',[-1 0 1])

ylim([-1.1 1.1])
xlim([data.color_time(1) data.color_time(end)])
axis normal
xlabel('Time (s)')
set(gca,'box','off')

% headline
annotation('textbox', [0 0.9 1 0.1], ...
    'String', sprintf('%s %d: %s',gs,clus, groupname), ...
    'EdgeColor', 'none', ...
    'HorizontalAlignment', 'center','FontSize', 14, 'FontWeight', 'bold')

%% figure 2: additional information

figure(f2)

% roi size
subplot(2,4,1)
xi = 0:1000;
h_all = ksdensity(data.cell_area,xi);
h = ksdensity(data.cell_area(idx),xi);

p = plot(xi,[h;h_all]);
m = median(data.cell_area(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')
set(p(2),'Color',[0.7 .7 .7])
xlabel('Area [mu^2]')
ylabel('Density')
xlim([0 350])
set(gca,'xtick',[0 150 300])
set(gca,'box','off')
set(gca,'ytick',[])
axis square
ylim([l(1) 1.1*l(2)])

% soma volume
subplot(2,4,2)
xi = 0:1500;
h_all = ksdensity(data.cell_volume,xi);
h = ksdensity(data.cell_volume(idx),xi);

p = plot(xi,[h;h_all]);
m = nanmedian(data.cell_volume(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')

set(p(2),'Color',[0.7 .7 .7])
xlabel('Volume [mu^3]')
xlim([0 1500])
set(gca,'xtick',[0 500 1000 1500])
set(gca,'box','off')
set(gca,'ytick',[])
axis square
ylim([l(1) 1.1*l(2)])


% rf size
subplot(2,4,3)
xi = 0:600;
h_all = ksdensity(data.rf_size,xi);
h = ksdensity(data.rf_size(idx),xi);

p = plot(xi,[h;h_all]);
m = median(data.rf_size(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')

set(p(2),'Color',[0.7 .7 .7])
xlabel('RF diameter (mu)')
xlim([0 500])
set(gca,'xtick',[0 250 500])
set(gca,'box','off')
set(gca,'ytick',[])
axis square
ylim([l(1) 1.1*l(2)])

% full field index
subplot(2,4,5)
xi = -1:0.01:1;
h_all = ksdensity(data.cell_ff_idx,xi);
h = ksdensity(data.cell_ff_idx(idx),xi);

p = plot(xi,[h;h_all]);
m = median(data.cell_ff_idx(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')

set(p(2),'Color',[0.7 .7 .7])
xlabel('FFi')
ylabel('Density')

xlim([-.2 1])
set(gca,'xtick',[0 0.5 1])
set(gca,'box','off')
set(gca,'ytick',[])
axis square
ylim([l(1) 1.1*l(2)])

% on off index
subplot(2,4,6)
xi = -1:0.01:1;
h_all = ksdensity(data.cell_oo_idx,xi);
h = ksdensity(data.cell_oo_idx(idx),xi);

p = plot(xi,[h;h_all]);
m = median(data.cell_oo_idx(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')

set(p(2),'Color',[0.7 .7 .7])
xlabel('OOi')
ylabel('Density')

xlim([-1 1])
set(gca,'xtick',[-1 0 1])
set(gca,'box','off')
set(gca,'ytick',[])
axis square
ylim([l(1) 1.1*l(2)])

subplot(2,4,7)
xi = 0:0.01:1;
h_all = ksdensity(data.cell_dsi,xi);
h = ksdensity(data.cell_dsi(idx),xi);

p = plot(xi,[h;h_all]);
m = median(data.cell_dsi(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')

set(p(2),'Color',[0.7 .7 .7])
xlabel('DSi')
xlim([0 1])
set(gca,'xtick',[0 0.5 1])
set(gca,'box','off')
set(gca,'ytick',[])
axis square

text(0.7,l(2),sprintf('%d%%',round(mean(data.cell_dp(idx)<0.05)*100)))
ylim([l(1) 1.1*l(2)])


subplot(2,4,8)
xi = 0:0.01:1;
h_all = ksdensity(data.cell_osi,xi);
h = ksdensity(data.cell_osi(idx),xi);

p = plot(xi,[h;h_all]);
m = median(data.cell_osi(idx));
l = get(gca,'ylim');
line([m m], [l(1) 1.1*l(2)],'color','k','linestyle',':')

set(p(2),'Color',[0.7 .7 .7])
xlabel('OSi')
xlim([0 1])
set(gca,'xtick',[0 0.5 1])
set(gca,'box','off')
set(gca,'ytick',[])
axis square

text(0.7,l(2),sprintf('%d%%',round(mean(data.cell_op(idx)<0.05)*100)))
ylim([l(1) 1.1*l(2)])

subplot(2,4,4)

h = zeros(2,4);

np(1) = sum(data.immuno_smi(idx)>0);
nn(1) = sum(data.immuno_smi(idx)==0);
n(1) = sum(~isnan(data.immuno_smi(idx)));
h(1,1) = np(1)/n(1);
h(2,1) = nn(1)/n(1);


np(2) = sum(data.immuno_melanopsin(idx)>0);
nn(2) = sum(data.immuno_melanopsin(idx)==0);
n(2) = sum(~isnan(data.immuno_melanopsin(idx)));
h(1,2) = np(2)/n(2);
h(2,2) = nn(2)/n(2);


np(3) = sum(data.genetics_pv(idx)>0);
nn(3) = sum(data.genetics_pv(idx)==0);
n(3) = sum(~isnan(data.genetics_pv(idx)));
h(1,3) = np(3)/n(3);
h(2,3) = nn(3)/n(3);


np(4) = sum(data.immuno_gad(idx)>0.5);
nn(4) = sum(data.immuno_gad(idx)<0.5);
n(4) = sum(~isnan(data.immuno_gad(idx)));
h(1,4) = np(4)/n(4);
h(2,4) = nn(4)/n(4);

b =  barh(h');
set(b(1),'FaceColor',[0 0.4470 0.7410],'EdgeColor','none')
set(b(2),'FaceColor',[0.7 .7 .7],'EdgeColor','none')
set(gca,'yticklabel',{'SMI','Mel','PV', 'GAD'})
axis square
xlim([0 1.5])
ylim([0 5])
set(gca,'xtick',[0 0.5 1])
set(gca,'box','off')

text(1.05,1,sprintf('%d/%d',np(1),n(1)),'fontsize',8)
text(1.05,2,sprintf('%d/%d',np(2),n(2)),'fontsize',8)
text(1.05,3,sprintf('%d/%d',np(3),n(3)),'fontsize',8)
text(1.05,4,sprintf('%d/%d',np(4),n(4)),'fontsize',8)





% headline
annotation('textbox', [0 0.9 1 0.1], ...
    'String', sprintf('%s %d: %s',gs,clus, groupname), ...
    'EdgeColor', 'none', ...
    'HorizontalAlignment', 'center','FontSize', 14, 'FontWeight', 'bold')
