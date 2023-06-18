clear all;
clc;

drawArrow = @(x,y,varargin) quiver3( x(:,1),x(:,2),x(:,3), y(:,1)-x(:,1),y(:,2)-x(:,2),y(:,3)-x(:,3),0,varargin{:} )

%Load the Octreee map
map3D = importOccupancyMap3D("../single_obstacle_map.ot")
% map3D = importOccupancyMap3D("octomap_from_file.ot")

filename = "path_raw.txt";

fileID = fopen(filename,'r');
if fileID == -1
    warningMessage = sprintf('Cannot open file %s', filename);
    uiwait(warndlg(warningMessage));
end

formatSpec = '%f %f %f';
sizeStart_Node = [3 1];

StartPose = fscanf(fileID,formatSpec,sizeStart_Node);
StartPose = StartPose';
GoalPose = fscanf(fileID,formatSpec,sizeStart_Node);
GoalPose = GoalPose';

formatSpec = '%f %f %f %f %f %f';
size_Node = [6 Inf];

Nodes = fscanf(fileID,formatSpec,size_Node);
Nodes = Nodes';

fclose(fileID);

%Read Path.txt for path/way points
filename = "path.txt";

fileID = fopen(filename,'r');
if fileID == -1
    warningMessage = sprintf('Cannot open file %s', filename);
    uiwait(warndlg(warningMessage));
end

formatSpec = '%f %f %f';
size_Node = [3 Inf];

PathNodes = fscanf(fileID,formatSpec,size_Node);
PathNodes = PathNodes';

fclose(fileID);

% Visualize the 3-D map
figure("Name","Path Plot")

show(map3D);

hold on
scatter3(StartPose(1),StartPose(2),StartPose(3),100,"red","filled","^")
scatter3(GoalPose(1),GoalPose(2),GoalPose(3),100,"yellow","filled","^")

% Plot all the parent-node combimation space that was explored by the Algortihm
hExplored = drawArrow(Nodes(:,4:6),Nodes(:,1:3),'linewidth',3,'color','c');

% Plot the interpolated path based on UAV Dubins connections
% hReference = plot3(PathNodes(:,1), PathNodes(:,2), PathNodes(:,3),"LineWidth",2,"Color","g");
hReference = scatter3(PathNodes(:,1), PathNodes(:,2), PathNodes(:,3),"magenta","filled");
legend([hReference,hExplored],"Reference","Explored Nodes", "Location","best")

hold off

view([-31 63])
