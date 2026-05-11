function f = plotOverview(data,groups)
% f = plotOverview(data)
%   Plot the cluster/group overview as shown in Fig. E2
%
%   Input:
%       data    data structure
%       groups  if 1, groups are shown (default)
%               if 0, clusters are shown
%               if 2, only RGC groups are shown
%
%   Output:
%       f       figure handle
%
%   Code for: Baden et al, Nature, 2016
%
%   Philipp Berens, 8.12.2015
%   www.retinal-functomics.org


SortedTraces = [];
SortedRFs = [];
SortedDS = [];

if nargin<2 || groups==1
    cI = data.group_idx;
elseif groups==0
    cI = data.cluster_idx;
elseif groups==2
    cI = data.group_idx;
    cI(cI>32)=-1;
end

uC = unique(cI);
uC = uC(2:end);

K = length(uC);

nCellsPerClust = zeros(K,1);

for i = 1:K
    SortedTraces = [SortedTraces data.chirp_avg(:,cI==uC(i))]; %#ok<AGROW>
    SortedRFs = [SortedRFs data.rf_tc(:,cI==uC(i))]; %#ok<AGROW>
    SortedDS = [SortedDS data.bar_tc(:,cI==uC(i))]; %#ok<AGROW>
    nCellsPerClust(i) = sum(cI==i);

    dsFraction(i) = round(mean(data.cell_dp(cI==uC(i))<0.05)*100);
end

% create new figure and resize
f = figure;
f.Position = [50 50 700 900];


% plot chirp responses
subplot(1,4,1:2)
last = [0; cumsum(nCellsPerClust)];
imagesc(data.chirp_time,1:sum(nCellsPerClust),SortedTraces',[-1 1])

for i=2:length(nCellsPerClust)
    if nCellsPerClust(i)>0
        line([0 data.chirp_time(end)],[last(i) last(i)],'color','k')
    end
end

chirp_events = [2 5 8 10 18 20 28 30 31.5];
for i=1:length(chirp_events)
    line([chirp_events(i) chirp_events(i)],[0 sum(nCellsPerClust)],'color','k')
end

xlabel('Time (s)')
title('Chirp')
axis normal
tick = unique(ceil(last(1:end-1) + diff(last)/2));
set(gca,'ytick',tick,'yticklabel',1:K)

% plot time kernels
subplot(1,4,3)
imagesc(data.rf_time,1:sum(nCellsPerClust),SortedRFs',[-4 4])

for i=2:length(nCellsPerClust)
    if nCellsPerClust(i)>0
        line([data.rf_time(1) data.rf_time(end)],[last(i) last(i)],'color','k')
    end
end

xlabel('Time (s)')
title('Time kernel')
set(gca,'ytick',tick,'yticklabel',[])
axis normal

% plot bar responses
subplot(1,4,4)
imagesc(data.bar_time,1:sum(nCellsPerClust),SortedDS',[-.5 1])

for i=2:length(nCellsPerClust)
    if nCellsPerClust(i)>0
        line([data.bar_time(1) data.bar_time(end)],[last(i) last(i)],'color','k')
    end
end

xlabel('Time (s)')
title('Moving bar')
set(gca,'ytick',tick,'yticklabel',[])
axis normal
