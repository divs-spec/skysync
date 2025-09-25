% RRTstar.m (reference)
function path = RRTstar(start_pt, goal_pt, obstacle_list, bounds)
max_iter = 1500; step = 1.0;
nodes = start_pt; parent = zeros(max_iter,1); parent(1)=0;
for i=1:max_iter
    if rand < 0.1, sample = goal_pt; else
        sample = [(bounds(1) + rand*(bounds(2)-bounds(1))), (bounds(3) + rand*(bounds(4)-bounds(3))), (bounds(5) + rand*(bounds(6)-bounds(5)))];
    end
    dists = sum((nodes - sample).^2,2); [~, idx] = min(dists);
    nearest = nodes(idx,:); vec = sample - nearest; normv = norm(vec);
    if normv==0, continue; end
    newp = nearest + (vec / normv) * min(step, normv);
    nodes = [nodes; newp]; parent(size(nodes,1)) = idx;
    if norm(newp - goal_pt) < step
        path = [goal_pt]; cur = size(nodes,1);
        while cur > 0
            path = [nodes(cur,:); path]; cur = parent(cur);
        end
        return;
    end
end
path = [];
end
