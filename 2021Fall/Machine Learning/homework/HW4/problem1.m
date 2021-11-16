clear all;
clc;

load('teapots.mat')

miu_image = mean(teapotImages);

covariance_mat = cov(teapotImages);
[Q, lamda] = eig(covariance_mat);
top_three_eigenvectors = Q(:, end - 2: end);

% subplot(2, 2, 1)
% imagesc(reshape(miu_image, 38, 50));
% title("data mean");
% 
% subplot(2, 2, 2)
% imagesc(reshape(top_three_eigenvectors(:, end), 38, 50));
% title("top 1 eigenvector image");
% 
% subplot(2, 2, 3)
% imagesc(reshape(top_three_eigenvectors(:, end - 1), 38, 50));
% title("top 2 eigenvector image");
% 
% subplot(2, 2, 4)
% imagesc(reshape(top_three_eigenvectors(:, end - 2), 38, 50));
% title("top 3 eigenvector image");

[num, img_len] = size(teapotImages);
random_id = [2;95;58;24;36;14;5;96;6;83];
selected_img = teapotImages(random_id, :);

% for i = 1:10
%     current_img = reshape(selected_img(i,:), 38, 50);
%     subplot(2, 5, i);
%     imagesc(current_img);
%     
%     title("Image\_" + num2str(i));
% end
% sgtitle("Image before reconstructed");

for i = 1:10
    current_img = selected_img(i,:);
    
    coef_1 = dot((current_img - miu_image), Q(: ,end));
    coef_2 = dot(current_img - miu_image, Q(: ,end - 1));
    coef_3 = dot(current_img - miu_image, Q(: ,end - 2));
    
    recovered_img = miu_image' + coef_1 * Q(: ,end) + coef_2 * Q(: ,end - 1) + coef_3 * Q(: ,end - 2);
    recovered_img = reshape(recovered_img, 38, 50);
    subplot(2, 5, i);
    imagesc(recovered_img);
    title("Recovered Image\_" + num2str(i));
end
sgtitle("Image after recovered");