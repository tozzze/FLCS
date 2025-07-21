% Load CSV
[filename, pathname] = uigetfile('*.csv', 'Select Histogram CSV File');
if isequal(filename,0)
    error('No file selected.');
end
data = readmatrix(fullfile(pathname, filename));

time_ps = data(:,1);
counts = data(:,2);

% Original and target sizes
original_bins = length(counts);
target_bins = 4096;

% Resample counts to 4096 points
x_original = linspace(min(time_ps), max(time_ps), original_bins);
x_target = linspace(min(time_ps), max(time_ps), target_bins);
counts_resampled = interp1(x_original, counts, x_target, 'linear');
IRF_Counts_PT = counts_resampled';
% Plot
figure;
plot(1:target_bins, counts_resampled);
xlabel('Bin number');
ylabel('Counts');
title('Binned to 4096 bins (index)');
