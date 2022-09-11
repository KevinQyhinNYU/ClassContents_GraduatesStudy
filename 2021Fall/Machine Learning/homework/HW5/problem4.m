p_test = cell(4,1);
p_test{1} = [0.1, 0.7; 0.8, 0.3];
p_test{2} = [0.5, 0.1; 0.1, 0.5];
p_test{3} = [0.1, 0.5; 0.5, 0.1];
p_test{4} = [0.9, 0.3; 0.1, 0.3];
[m_test, m_origin] = junction_tree(p_test);


plot(x, y);
grid on;
xlabel("Percent Encryption");
ylabel("Net Speedup");
xtickformat("percentage");